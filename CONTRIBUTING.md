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
└── skills/
    └── meeting/
        └── SKILL.md
```

## How to add a persona

1. Fork the repo and create a branch: `add-<team>-<archetype>` (or `update-<team>-<archetype>` if tweaking).
2. Create a file at `plugins/meeting-bots/agents/<team>-<archetype>.md` following the existing format:
   - YAML frontmatter: `name`, `description`, `model` (opus for boss, sonnet for others), `tools: Read, Grep, Glob`, `color`.
   - System prompt with these sections: Psychology (constant across the archetype), Role in the team, How you argue, Code taste (dev personas only), Blind spots, Language, Style.
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

## Style rules (strict)

- **No em-dashes anywhere.** Not in personas, not in README, not in commit messages. Use commas, colons, parentheses, or split the sentence.
- **No franglais.** One file, one language. The runtime detection handles user language.
- **Word caps per persona contribution**: 250 words for rounds 1 and 2, 150 words for round 3 closings, up to 500 for the Boss synthesis.
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
