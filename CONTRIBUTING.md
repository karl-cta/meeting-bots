# Contributing to Meeting Bots

Contributions welcome: new personas, new teams, bug fixes, docs. Be direct, keep it sharp, no ego.

## Repo layout

```
plugins/meeting-bots/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   └── <team>-<archetype>.md   (25 files: 5 teams x 5 archetypes)
├── hooks/
│   ├── hooks.json              (PostToolUse:Agent and Stop hook registration)
│   ├── log-tokens.py           (per-call ledger writer, runs async)
│   └── finalize-tokens.py      (Stop hook: aggregates ledger, appends Token report)
└── skills/
    └── meeting/
        └── SKILL.md            (orchestration)
```

## How to add a persona

1. Fork, branch `add-<team>-<archetype>` (or `update-...` if tweaking).
2. Create `plugins/meeting-bots/agents/<team>-<archetype>.md`:
   - YAML frontmatter: `name`, `description`, `model` (opus for boss, sonnet for others), `tools: Read, Grep, Glob`, `color`.
   - Non-Boss sections: Psychology (constant across archetype), Role in the team, How you argue, Code taste (dev personas only), Blind spots, Language, Style.
   - Boss sections: Psychology, Role in the team, **How you chair the meeting** (round 0 framing, round 1 silence, rounds 2 and 3 challenger mode, synthesis at the end), Code taste (dev-boss only), When you deliver the final call, Language, Style.
3. Respect the archetype psychology (Boss, Pusher, Rookie, Watcher, Cynic). Only the team expertise varies.
4. Sanity-check locally:

   ```
   claude plugin validate .
   claude --plugin-dir ./plugins/meeting-bots
   /meeting-bots:meeting "a realistic topic" --agents your-new-persona,<4 others>
   ```

   Open the generated markdown file. If a persona's voice wobbles across rounds, tighten the system prompt.

## How to add a team

Drop 5 files, one per archetype:

- `<team>-boss.md` (Opus)
- `<team>-pusher.md` (Sonnet)
- `<team>-rookie.md` (Sonnet)
- `<team>-watcher.md` (Sonnet)
- `<team>-cynic.md` (Sonnet)

Then update the team table in `plugins/meeting-bots/skills/meeting/SKILL.md` to include the new team name and its "For topics about" hint. Add keyword triggers to Step 0's detection list if relevant.

Open an issue first if the team concept is unusual, so we can align before you invest time in 5 files.

## Token accounting

Two hooks own it: `log-tokens.py` (per-call ledger writer, `PostToolUse:Agent`, async) and `finalize-tokens.py` (Stop hook, aggregates the ledger into a `## Token report` section at the end of each synthesis). The skill does not touch tokens beyond resetting the ledger at Step 3. To update pricing or add a model, edit the `PRICING` dict and `model_for()` in `finalize-tokens.py`. If you change the ledger schema, update both scripts in the same PR.

## Style rules (strict)

- **No em-dashes anywhere.** Not in personas, not in README, not in commit messages. Use commas, colons, parentheses, or split the sentence.
- **No franglais.** One file, one language. Runtime detection handles user language.
- **Word caps per persona contribution**: 150 words for the Boss round 0 framing, 250 words for rounds 1 and 2, 150 words for round 3 closings (including the Boss last challenge), up to 500 for the Boss synthesis. The italic footer line in the synthesis does not count.
- **Every persona owns blind spots.** Keep the "Blind spots" section honest, not decorative.
- **No AI slop in prompts.** Short, concrete, specific. No ceremonial padding.
- **Dev personas respect code taste.** Readable over clever, no pointless abstraction, no defensive code for impossible cases.

## Commit and PR

- **Branch**: `add-<thing>`, `update-<thing>`, `fix-<thing>`.
- **Commit message**: imperative, lowercase, under 60 chars. Examples: `add legal team`, `fix cynic tone in rebuttal`, `tighten rookie word cap`.
- **PR title**: same style as the commit.
- **PR description**: what changed, why, and an example transcript if the change affects runtime behavior.

## Issues

Open one with what you tried, what happened, what you expected. Claude Code version if it matters.

## License

By contributing you agree your contributions are licensed under MIT (see LICENSE).
