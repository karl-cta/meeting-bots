# Contributing to Meeting Bots

Thanks for thinking about contributing. Meeting Bots is open to new personas, new teams, bug fixes, docs, and ideas.

## What you can contribute

- **New persona** in an existing team (new voice variant).
- **New team** entirely: a complete set of 5 archetype files for a new domain.
- **Bug fix** in the skill orchestration or a persona's system prompt.
- **Docs**: README, examples, translations.
- **Ideas and feedback** via issues.

## Repo layout

```
plugins/meeting-bots/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   └── <team>-<archetype>.md   (25 files: 5 teams x 5 archetypes)
├── hooks/
│   ├── hooks.json              (PostToolUse:Agent hook registration)
│   └── log-tokens.py           (per-call ledger writer, runs async)
└── skills/
    └── meeting/
        └── SKILL.md            (orchestration + inline Python for the token report)
```

## How to add a persona

1. Fork the repo and create a branch: `add-<team>-<archetype>` (or `update-<team>-<archetype>` if tweaking).
2. Create a file at `plugins/meeting-bots/agents/<team>-<archetype>.md` following the existing format:
   - YAML frontmatter: `name`, `description`, `model` (opus for boss, sonnet for others), `tools: Read, Grep, Glob`, `color`.
   - System prompt sections for non-Boss archetypes: Psychology (constant across the archetype), Role in the team, How you argue, Code taste (dev personas only), Blind spots, Language, Style.
   - System prompt sections for Boss: Psychology, Role in the team, **How you chair the meeting** (round 0 framing, round 1 silence, rounds 2 and 3 challenger mode, synthesis at the end), Code taste (dev-boss only), When you deliver the final call, Language, Style.
3. Respect the archetype psychology (Boss, Pusher, Rookie, Watcher, Cynic). Only the team expertise varies.
4. Sanity-check locally:

   ```
   claude --plugin-dir ./plugins/meeting-bots
   /meeting-bots:meeting "a realistic topic" --agents your-new-persona,<4 others>
   ```

## How to add a team

Drop 5 files, one per archetype:

- `<team>-boss.md` (Opus)
- `<team>-pusher.md` (Sonnet)
- `<team>-rookie.md` (Sonnet)
- `<team>-watcher.md` (Sonnet)
- `<team>-cynic.md` (Sonnet)

Then update the team table in `plugins/meeting-bots/skills/meeting/SKILL.md` to include the new team name and its "For topics about" hint. Add keyword triggers to Step 0's detection list if relevant.

Open an issue first if the team concept is unusual, so we can align on the expertise angle before you invest time in 5 files.

## How to touch the token accounting

The plugin tracks tokens and estimates cost in two places:

- `hooks/hooks.json` + `hooks/log-tokens.py`: a PostToolUse hook on the `Agent` tool. `async: true` is load-bearing; without it, every subagent call blocks on the Python startup and meetings slow down visibly. `log-tokens.py` reads the hook payload from stdin, pulls `usage` counters out of `tool_response`, and appends one JSON line to `.meeting-bots-tokens.jsonl` in the user's cwd. Standard library only, fails silently.
- Inline Python block inside `skills/meeting/SKILL.md` (Step 8 token report section). Called once at the end of each synthesis by the skill via the Bash tool. Aggregates the ledger, infers the model from the persona name (`-boss` is Opus, otherwise Sonnet), computes cost from a hard-coded `PRICING` table, appends a `## Token report` Markdown section to the transcript, deletes the ledger, and prints a `TOKEN_SUMMARY` line to stdout that the skill relays to the console.

Why inline and not an external script: `$CLAUDE_PLUGIN_ROOT` is only exposed to hook commands (declared in `hooks.json`), not to Bash tool calls invoked from within a skill. An external `report-tokens.py` called from the SKILL.md would fail to resolve its own path. Inlining removes the dependency.

If Anthropic updates pricing, update the `PRICING` dict in both places if you add a separate script, or just in the SKILL.md block today. If you add a new model (e.g. Haiku-based personas), add its entry to `PRICING` and extend `model_for()` to recognize the naming convention. If you change the ledger schema, update `log-tokens.py` and the inline Python in the same PR.

Claude Code does not currently forward `total_cost_usd` or `duration_ms` through the Agent hook payload, which is why cost is estimated rather than reported. If that changes upstream, simplify the inline Python to use the real value.

## Style rules (strict)

- **No em-dashes anywhere.** Not in personas, not in README, not in commit messages. Use commas, colons, parentheses, or split the sentence.
- **No franglais.** One file, one language. The runtime detection handles user language.
- **Word caps per persona contribution**: 150 words for the Boss round 0 framing, 250 words for rounds 1 and 2, 150 words for round 3 closings (including the Boss last challenge), up to 500 for the Boss synthesis. The italic footer line in the synthesis does not count.
- **Every persona owns blind spots.** Keep the "Blind spots" section honest, not decorative.
- **No AI slop in prompts.** Short, concrete, specific. No ceremonial padding.
- **Dev personas respect code taste.** Readable over clever, no pointless abstraction, no defensive code for impossible cases.

## Testing your change

Validate the plugin structure before pushing:

```
claude plugin validate .
```

Then run a real meeting in your target team:

```
claude --plugin-dir ./plugins/meeting-bots
/meeting-bots:meeting "a realistic topic for your team"
```

Open the generated markdown file. If a persona's voice wobbles across rounds, tighten the system prompt.

## Commit and PR

- **Branch name**: `add-<thing>`, `update-<thing>`, or `fix-<thing>`.
- **Commit message**: imperative, lowercase, under 60 characters. Examples: `add legal team`, `fix cynic tone in rebuttal`, `tighten rookie word cap`.
- **PR title**: same style as the commit.
- **PR description**: what changed, why, and an example transcript if the change affects runtime behavior.

## Issues

Bug? Feature idea? New team you'd like? Open an issue with:

- What you were trying to do
- What happened
- What you expected
- Claude Code version if it matters

## Code of conduct

Be direct, constructive, and respectful. The goal is a sharper meeting room, not ego. No malicious or harmful personas. No contributions that promote discrimination or target specific groups.

## License

By contributing you agree your contributions are licensed under MIT (see LICENSE).
