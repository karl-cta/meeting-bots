# Meeting Bots

AI personas sit around a table and debate your question. The Boss listens, then delivers the call. You push back until you are satisfied.

5 by default, 3 to 10 on demand. Mix teams. Add custom personas on the fly. No plugin files to edit.

A meeting room, inside Claude Code.

[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-6B5BEE)](https://code.claude.com/docs/en/plugins)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

## Why

Ask one AI, you get one answer, hedged and polite. That is not a decision, that is noise with confidence.

A real decision comes from a room with disagreement. Someone who wants to ship. Someone who asks the naive question. Someone who spots the thing that will bite you in six months. Someone who teases the pretense out of the room. And someone with the scars to call it at the end.

Meeting Bots gives you that room, on tap, in Claude Code.

## The five personas

The same five psychologies in every meeting. The expertise changes with the team.

| Archetype | Model      | Role                                                       |
| --------- | ---------- | ---------------------------------------------------------- |
| Boss      | Opus 4.7   | Listens, synthesizes, makes the final call                 |
| Pusher    | Sonnet 4.6 | Bold, pushes the ambitious move                            |
| Rookie    | Sonnet 4.6 | Asks the naive questions that force clarity                |
| Watcher   | Sonnet 4.6 | Thinks sideways, surfaces the second-order effects         |
| Cynic     | Sonnet 4.6 | Teases, cuts through, brings back pragmatism               |

## The five teams

Pick a team, or let the plugin detect it from your question.

| Team       | Best for                                            | Personas (examples)                                           |
| ---------- | --------------------------------------------------- | ------------------------------------------------------------- |
| `dev`      | Code, architecture, stack, engineering calls        | Senior architect, bold engineer, curious junior, SRE, seasoned dev |
| `design`   | Brand, UX, UI, visual, design systems               | Design director, avant-garde designer, intern, UX researcher, sharp eye |
| `product`  | Features, MVP, roadmap, metrics                     | Head of Product, startup PM, junior PM, data-minded analyst, cynical marketer |
| `business` | Strategy, GTM, pricing, legal, market               | Strategy veteran, founder, intern, meticulous lawyer, field sales |
| `life`     | Career moves, big choices, personal decisions       | Coach, ambitious friend, curious friend, philosopher, sarcastic friend |

Each team has the same 5 archetypes. Same psychology. Different expertise.

## Install

```
/plugin marketplace add karl-cta/meeting-bots
/plugin install meeting-bots@meeting-bots
```

Dev test from the repo:

```
claude --plugin-dir ./plugins/meeting-bots
```

## Use it

**One-shot, team auto-detected from your question:**

```
/meeting-bots:meeting "I want to launch a SaaS. Where do I start, what do I build first, and how do I know if anyone will pay for it?"
```

The plugin picks the right team, convenes the lineup, asks you to confirm or override, runs the rounds, the Boss delivers the call. You push back, it relaunches until you say stop.

**Pick the team yourself:**

```
/meeting-bots:meeting "Should I take the Dublin offer or stay put?" --team life
```

**Custom lineup, mix across teams (3 to 10 personas):**

```
/meeting-bots:meeting "Should we rebuild the onboarding flow?" --agents product-boss,design-pusher,product-rookie,dev-watcher,product-cynic
```

```
/meeting-bots:meeting "Big strategic pivot?" --agents business-boss,business-pusher,life-rookie,product-watcher,business-cynic,design-watcher
```

**Add a custom persona on the fly:**

```
/meeting-bots:meeting "Should we raise a seed round?"
```

At the confirm step, say something like:

```
Add a CFO obsessed with burn rate.
```

The chair drafts the CFO on the spot (role, values, style, blind spots) and includes them in the lineup. No plugin files touched.

**Full interactive wizard (no args):**

```
/meeting-bots:meeting
```

## How a meeting goes

The full debate (personas, 3 rounds: openings, rebuttals, closings) is written to a markdown file in your current directory. **Your console stays clean:** you only see the Boss's final synthesis plus the file path. If you push back, a new iteration is appended to the same file and you see the refreshed synthesis.

```
You  ->  /meeting-bots:meeting "I want to launch a SaaS. Where do I start?"

Chair -> Product team. boss, pusher, rookie, watcher, cynic. OK?

You  ->  ok

Chair -> Transcript: ./meeting-saas-launch.md
         Round 1 recorded.
         Round 2 recorded.
         Round 3 recorded.

         Final synthesis:
         [Boss, full text, up to 500 words]

         Tokens: 99,586 in / 7,527 out, cost ~0.7725 USD (estimated)
         Full debate: ./meeting-saas-launch.md

         Want to push an angle or are you good?

You  ->  But I have no distribution yet.

Chair -> Iteration 2 recorded, synthesis below:
         [Boss, updated call]

         Tokens: 38,412 in / 2,980 out, cost ~0.2987 USD (estimated)

You  ->  ok

Chair -> Meeting closed. Full debate: ./meeting-saas-launch.md
```

Open the file to see every persona's round 1 opening, round 2 rebuttal, round 3 closing, and the synthesis, cleanly structured. The console is the executive summary, the file is the record.

### Token report

At the end of each synthesis, a `## Token report` table is appended to the transcript with a per-persona row (model, calls, input total, fresh/cache-write/cache-read breakdown, output, estimated cost in USD) plus a totals row. A one-line summary, e.g. `Tokens: 99,586 in / 7,527 out, cost ~0.7725 USD (estimated)`, is printed to the console alongside the synthesis. Iterations get their own report.

Two things to know when reading the numbers:

- **Input total is the real volume**, not just fresh input. Anthropic's API reports fresh input, cache writes, and cache reads as three separate counters. Most of a meeting's input traffic sits in the cache (the persona prompts, the prior rounds), so fresh input alone looks tiny. The report sums all three.
- **Cost is estimated** from Anthropic public pricing, using the model inferred from the persona name (Opus 4.7 for `-boss`, Sonnet 4.6 for the rest). Claude Code does not currently forward its own cost figure through the hook payload, so the table is a calculated estimate, not a billed amount.

The data comes from a PostToolUse hook on the `Agent` tool that logs each subagent call to a short-lived ledger in your cwd. The hook runs asynchronously (`async: true`), so accounting adds no latency to the meeting itself. The ledger is consumed and deleted at the end of each synthesis. No network calls, no telemetry leaves your machine.

## Customize

Two levels of customization, depending on whether you want the change to stick.

### At runtime (no plugin edit)

Happens inside a meeting, no files touched. Use it when you want a one-shot tweak for a specific question.

- **Mix teams**: pass `--agents product-boss,dev-pusher,life-rookie,business-watcher,product-cynic` to pull personas from any team.
- **Resize the meeting**: any lineup from 3 to 10 personas works. Smaller goes faster. Larger explores more angles at token cost.
- **Add a custom persona in natural language**: at the confirm step, say "add a CFO obsessed with burn rate" or "add a paranoid DPO from a healthcare startup". The chair crafts their prompt on the spot and includes them in the round.
- **Designate a custom Boss**: if you want your custom persona to synthesize, tell the chair explicitly ("make the CFO the Boss").

### Permanent (add to the plugin)

Ship a new persona or team that others can use too.

**Add a persona:**

1. Drop a new file in `plugins/meeting-bots/agents/`, following the pattern `<team>-<archetype>.md`.
2. Frontmatter (`name`, `description`, `model`, `tools`, `color`) and a system prompt that fits the archetype's psychology with your team's expertise.
3. Use it: `/meeting-bots:meeting "..." --agents your-new-agent,dev-pusher,...`

**Add a whole new team:**

Drop 5 files: `<theme>-boss.md`, `<theme>-pusher.md`, `<theme>-rookie.md`, `<theme>-watcher.md`, `<theme>-cynic.md`. Update the SKILL.md team table. Done.

## Example output

Two full meetings in the `examples/` folder:

- [`examples/saas-launch.md`](./examples/saas-launch.md) (English, `product` team): "I want to launch a SaaS. Where do I start, what do I build first, and how do I know if anyone will pay for it?"
- [`examples/app-monetisation.md`](./examples/app-monetisation.md) (French, `dev` team): building and monetizing an app, with a stack constraint.

## License

MIT. Do what you want, no warranty.

## Credits

Built by [Karl Certa](https://github.com/karl-cta). Inspired by every meeting where the quiet person turned out to be right.
