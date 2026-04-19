#!/usr/bin/env python3
"""
PostToolUse hook for the Agent tool.

Reads the JSON payload from stdin, extracts usage counters from
tool_response, and appends one JSON line per subagent call to the
per-cwd ledger at .meeting-bots-tokens.jsonl.

Fails silently on any error: the meeting should always run, even
if token accounting cannot be written.
"""

import json
import os
import pathlib
import sys
import time


def coerce_int(value) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    if payload.get("tool_name") != "Agent":
        return 0

    tool_input = payload.get("tool_input") or {}
    tool_response = payload.get("tool_response") or {}
    usage = tool_response.get("usage") if isinstance(tool_response, dict) else None
    if not isinstance(usage, dict):
        usage = {}

    entry = {
        "ts": time.time(),
        "subagent_type": tool_input.get("subagent_type", "general-purpose"),
        "description": tool_input.get("description", ""),
        "input_tokens": coerce_int(usage.get("input_tokens", 0)),
        "output_tokens": coerce_int(usage.get("output_tokens", 0)),
        "cache_creation_input_tokens": coerce_int(
            usage.get("cache_creation_input_tokens", 0)
        ),
        "cache_read_input_tokens": coerce_int(
            usage.get("cache_read_input_tokens", 0)
        ),
    }

    cwd = payload.get("cwd") or os.getcwd()
    ledger = pathlib.Path(cwd) / ".meeting-bots-tokens.jsonl"
    try:
        with ledger.open("a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
