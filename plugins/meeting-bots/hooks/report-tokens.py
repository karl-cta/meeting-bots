#!/usr/bin/env python3
"""
Aggregate the per-call token ledger into a Markdown report.

Usage:
  python3 report-tokens.py <ledger.jsonl> <transcript.md> [heading]

Reads the JSONL ledger, groups by subagent_type, estimates cost using
published Anthropic pricing (Opus 4.7 for *-boss personas, Sonnet 4.6
for the rest), appends a Markdown section to the transcript, deletes
the ledger, and prints a TOKEN_SUMMARY line on stdout that the skill
relays to the console.

Cost is estimated, not billed: Claude Code does not forward its own
cost figure through the hook payload, so we compute from the usage
counters we have.
"""

import json
import pathlib
import sys


PRICING = {
    "opus-4.7":   {"in": 15.0, "cache_w": 18.75, "cache_r": 1.50, "out": 75.0},
    "sonnet-4.6": {"in":  3.0, "cache_w":  3.75, "cache_r": 0.30, "out": 15.0},
}


def model_for(raw_name: str) -> str:
    name = raw_name.split(":", 1)[-1] if ":" in raw_name else raw_name
    if name.endswith("-boss"):
        return "opus-4.7"
    return "sonnet-4.6"


def cost_for(model: str, fresh_in: int, cw: int, cr: int, out: int) -> float:
    p = PRICING[model]
    return (
        fresh_in * p["in"]
        + cw * p["cache_w"]
        + cr * p["cache_r"]
        + out * p["out"]
    ) / 1_000_000


def load_rows(ledger: pathlib.Path):
    rows = []
    for line in ledger.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            pass
    return rows


def aggregate(rows):
    per = {}
    for r in rows:
        name = r.get("subagent_type", "unknown")
        p = per.setdefault(
            name, {"calls": 0, "fresh": 0, "out": 0, "cache_w": 0, "cache_r": 0}
        )
        p["calls"] += 1
        p["fresh"] += r.get("input_tokens", 0) or 0
        p["out"] += r.get("output_tokens", 0) or 0
        p["cache_w"] += r.get("cache_creation_input_tokens", 0) or 0
        p["cache_r"] += r.get("cache_read_input_tokens", 0) or 0
    return per


def render(per, heading: str):
    rows_out = []
    totals = {"calls": 0, "fresh": 0, "cache_w": 0, "cache_r": 0, "out": 0, "cost": 0.0}
    for name in sorted(per.keys()):
        p = per[name]
        model = model_for(name)
        c = cost_for(model, p["fresh"], p["cache_w"], p["cache_r"], p["out"])
        total_in = p["fresh"] + p["cache_w"] + p["cache_r"]
        rows_out.append(
            (name, model, p["calls"], total_in, p["fresh"], p["cache_w"], p["cache_r"], p["out"], c)
        )
        totals["calls"] += p["calls"]
        totals["fresh"] += p["fresh"]
        totals["cache_w"] += p["cache_w"]
        totals["cache_r"] += p["cache_r"]
        totals["out"] += p["out"]
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
        lines.append(
            f"| {name} | {model} | {calls} | {total_in:,} | {fresh:,} | {cw:,} | {cr:,} | {out:,} | {c:.4f} |"
        )
    lines.append(
        f"| **Total** | | {totals['calls']} | **{total_in_all:,}** | **{totals['fresh']:,}** | **{totals['cache_w']:,}** | **{totals['cache_r']:,}** | **{totals['out']:,}** | **{totals['cost']:.4f}** |"
    )
    lines.append("")
    return lines, total_in_all, totals


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: report-tokens.py <ledger.jsonl> <transcript.md> [heading]", file=sys.stderr)
        return 2

    ledger = pathlib.Path(sys.argv[1])
    transcript = pathlib.Path(sys.argv[2])
    heading = sys.argv[3] if len(sys.argv) > 3 else "Token report"

    if not ledger.exists():
        return 0

    rows = load_rows(ledger)
    if not rows:
        ledger.unlink(missing_ok=True)
        return 0

    per = aggregate(rows)
    lines, total_in_all, totals = render(per, heading)

    with transcript.open("a") as f:
        f.write("\n".join(lines) + "\n")
    ledger.unlink(missing_ok=True)

    print(
        f"TOKEN_SUMMARY total_in={total_in_all} total_out={totals['out']} cost={totals['cost']:.4f}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
