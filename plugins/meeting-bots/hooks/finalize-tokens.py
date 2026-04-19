#!/usr/bin/env python3
"""
Stop hook: when a meeting just finished a synthesis (or iteration),
aggregate the ledger, append a Token report section to the transcript,
delete the ledger, and surface a one-line systemMessage to the user.

Triggers only when the latest transcript in cwd has more synthesis-like
sections than existing Token report sections. In every other case
(mid-meeting, no meeting at all, already reported), exits silently.
"""

import json
import os
import pathlib
import re
import sys


PRICING = {
    "opus-4.7":   {"in": 15.0, "cache_w": 18.75, "cache_r": 1.50, "out": 75.0},
    "sonnet-4.6": {"in":  3.0, "cache_w":  3.75, "cache_r": 0.30, "out": 15.0},
}

SYNTHESIS_RE = re.compile(r'^## (Synthesis by|Iteration \d+, synthesis)', re.MULTILINE)
TOKEN_REPORT_RE = re.compile(r'^## Token report', re.MULTILINE)


def model_for(raw: str) -> str:
    name = raw.split(":", 1)[-1] if ":" in raw else raw
    return "opus-4.7" if name.endswith("-boss") else "sonnet-4.6"


def cost_for(model: str, fresh: int, cw: int, cr: int, out: int) -> float:
    p = PRICING[model]
    return (fresh * p["in"] + cw * p["cache_w"] + cr * p["cache_r"] + out * p["out"]) / 1_000_000


def find_transcript(cwd: pathlib.Path) -> pathlib.Path | None:
    candidates = sorted(cwd.glob("meeting-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    for path in candidates:
        try:
            text = path.read_text()
        except Exception:
            continue
        synthesis_count = len(SYNTHESIS_RE.findall(text))
        token_count = len(TOKEN_REPORT_RE.findall(text))
        if synthesis_count > token_count:
            return path
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    cwd = pathlib.Path(payload.get("cwd") or os.getcwd())
    ledger = cwd / ".meeting-bots-tokens.jsonl"
    if not ledger.exists():
        return 0

    transcript = find_transcript(cwd)
    if transcript is None:
        return 0

    rows = []
    for line in ledger.read_text().splitlines():
        s = line.strip()
        if not s:
            continue
        try:
            rows.append(json.loads(s))
        except Exception:
            pass

    if not rows:
        ledger.unlink(missing_ok=True)
        return 0

    transcript_text = transcript.read_text()
    existing_reports = len(TOKEN_REPORT_RE.findall(transcript_text))
    heading = "Token report" if existing_reports == 0 else f"Token report, iteration {existing_reports}"

    per = {}
    for r in rows:
        name = r.get("subagent_type", "unknown")
        p = per.setdefault(name, {"calls": 0, "fresh": 0, "out": 0, "cache_w": 0, "cache_r": 0})
        p["calls"] += 1
        p["fresh"] += r.get("input_tokens", 0) or 0
        p["out"] += r.get("output_tokens", 0) or 0
        p["cache_w"] += r.get("cache_creation_input_tokens", 0) or 0
        p["cache_r"] += r.get("cache_read_input_tokens", 0) or 0

    totals = {"calls": 0, "fresh": 0, "cache_w": 0, "cache_r": 0, "out": 0, "cost": 0.0}
    rows_out = []
    for name in sorted(per.keys()):
        p = per[name]
        model = model_for(name)
        c = cost_for(model, p["fresh"], p["cache_w"], p["cache_r"], p["out"])
        total_in = p["fresh"] + p["cache_w"] + p["cache_r"]
        rows_out.append((name, model, p["calls"], total_in, p["fresh"], p["cache_w"], p["cache_r"], p["out"], c))
        for k in ("calls", "fresh", "cache_w", "cache_r", "out"):
            totals[k] += p[k]
        totals["cost"] += c
    total_in_all = totals["fresh"] + totals["cache_w"] + totals["cache_r"]

    lines = [
        "",
        "---",
        "",
        f"## {heading}",
        "",
        "Cost is **estimated** from Anthropic public pricing (Opus 4.7 for `-boss`, Sonnet 4.6 for the others). Input total = fresh + cache write + cache read.",
        "",
        "| Persona | Model | Calls | Input total | Fresh | Cache write | Cache read | Output | Cost (USD) |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, model, calls, total_in, fresh, cw, cr, out, c in rows_out:
        lines.append(f"| {name} | {model} | {calls} | {total_in:,} | {fresh:,} | {cw:,} | {cr:,} | {out:,} | {c:.4f} |")
    lines.append(f"| **Total** | | {totals['calls']} | **{total_in_all:,}** | **{totals['fresh']:,}** | **{totals['cache_w']:,}** | **{totals['cache_r']:,}** | **{totals['out']:,}** | **{totals['cost']:.4f}** |")
    lines.append("")

    with transcript.open("a") as f:
        f.write("\n".join(lines) + "\n")
    ledger.unlink(missing_ok=True)

    summary = f"Tokens: {total_in_all:,} in / {totals['out']:,} out, cost ~{totals['cost']:.4f} USD (estimated)"
    print(json.dumps({"systemMessage": summary}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
