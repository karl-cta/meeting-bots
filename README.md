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

| Archetype | Model      | Role                                                                    |
| --------- | ---------- | ----------------------------------------------------------------------- |
| Boss      | Opus 4.7   | Frames at round 0, silent at round 1, challenges at rounds 2 and 3, synthesizes |
| Pusher    | Sonnet 4.6 | Bold, pushes the ambitious move                                         |
| Rookie    | Sonnet 4.6 | Asks the naive questions that force clarity                             |
| Watcher   | Sonnet 4.6 | Thinks sideways, surfaces the second-order effects                      |
| Cynic     | Sonnet 4.6 | Teases, cuts through, brings back pragmatism                            |

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

**Auto-detect team from your question:**

```
/meeting-bots:meeting "I want to launch a SaaS. Where do I start, what do I build first, and how do I know if anyone will pay for it?"
```

The plugin picks the team, convenes the lineup, asks you to confirm or override, runs the rounds, the Boss delivers the call. You push back, it relaunches until you say stop.

**Force a team:**

```
/meeting-bots:meeting "..." --team life
```

**Custom lineup, mix teams (3 to 10 personas):**

```
/meeting-bots:meeting "..." --agents product-boss,design-pusher,product-rookie,dev-watcher,product-cynic
```

**Add a custom persona on the fly:**

Run `/meeting-bots:meeting "..."` then at the confirm step say something like `Add a CFO obsessed with burn rate` (or `Make the CFO the Boss` if you want them to synthesize). The chair drafts them on the spot (role, values, style, blind spots). No plugin files touched.

**Full interactive wizard (no args):**

```
/meeting-bots:meeting
```

Real, tested commands with full transcripts are in the [Example output](#example-output) section below.

## How a meeting goes

A meeting runs 4 rounds: the Boss frames the debate at round 0 (open angles, no position), the others open at round 1, everyone rebuts at round 2 (Boss rejoins as challenger), everyone closes at round 3, then the Boss synthesizes. The full debate is written to a markdown file in your current directory. **Your console stays clean:** you only see the Boss's final synthesis plus the file path. If you push back, a new iteration is appended to the same file and you see the refreshed synthesis.

```
You  ->  /meeting-bots:meeting "I want to launch a SaaS. Where do I start?"

Chair -> Product team. boss, pusher, rookie, watcher, cynic. OK?

You  ->  ok

Chair -> Transcript: ./meeting-saas-launch.md
         Framing recorded.
         Round 1 recorded.
         Round 2 recorded.
         Round 3 recorded.

         Final synthesis:
         [Boss, full text, up to 500 words]

         Tokens: 112,845 in / 7,355 out, cost ~0.8604 USD (estimated)
         Full debate: ./meeting-saas-launch.md

         Want to push an angle or are you good?

You  ->  But I have no distribution yet.

Chair -> Iteration 2 recorded, synthesis below:
         [Boss, updated call]

         Tokens: 38,412 in / 2,980 out, cost ~0.2987 USD (estimated)

You  ->  ok

Chair -> Meeting closed. Full debate: ./meeting-saas-launch.md
```

Open the file to see the Boss's round 0 framing, every persona's round 1 opening, round 2 rebuttals (with the Boss's challenges), round 3 closings, and the final synthesis. The console is the executive summary, the file is the record.

### Token report

At the end of each synthesis, a `## Token report` table is appended to the transcript with a per-persona row (model, calls, input total, fresh/cache-write/cache-read breakdown, output, estimated cost in USD) plus a totals row. A one-line summary (`Tokens: 99,586 in / 7,527 out, cost ~0.7725 USD (estimated)`) is printed to the console alongside the synthesis. Iterations get their own report.

- **Input total is the real volume**, not just fresh input. Most of a meeting's input sits in the prompt cache (persona prompts, prior rounds). The report sums fresh + cache writes + cache reads.
- **Cost is estimated** from Anthropic public pricing (Opus 4.7 for `-boss`, Sonnet 4.6 for the rest). Claude Code does not currently forward its own cost figure through the hook payload, so the table is a calculated estimate.

No network calls, no telemetry leaves your machine. Hook internals are documented in [CONTRIBUTING.md](./CONTRIBUTING.md).

## Extend the plugin

Ship a new persona, a whole new team, or tweak the hooks: see [CONTRIBUTING.md](./CONTRIBUTING.md) for the file layout, frontmatter rules, and style guardrails.

## Example output

Full meetings in the `examples/` folder, each produced by the exact command shown:

**[`examples/rest-or-push.md`](./examples/rest-or-push.md)** (English, 3 agents, life team)

```
/meeting-bots:meeting "I have two weeks off coming up. Should I rest, or push hard on my side project?" --agents life-boss,life-pusher,life-cynic
```

Minimal lineup on a binary life decision. 10 Agent calls, $0.71 estimated cost.

**[`examples/vibe-code-saas.md`](./examples/vibe-code-saas.md)** (English, 5 agents, dev team auto-detected)

```
/meeting-bots:meeting "I want to vibe code a SaaS end-to-end: a simple invoicing tool for freelancers who hate Stripe's dashboard. I'll direct the AI but I'm not a pro dev. Before I write a line, help me plan: what technical constraints to lock in upfront, what to build first, where I need to make the call myself rather than let the AI decide, and how I avoid the 'works on my laptop, dies in prod' trap."
```

Full default team, auto-detected dev, realistic non-dev-founder scenario. 16 Agent calls, $0.87 estimated cost.

**[`examples/freelance-transition.md`](./examples/freelance-transition.md)** (English, 5 agents, cross-team business + life)

```
/meeting-bots:meeting "I want to go freelance this year. How do I line up my first clients and my finances without burning out?" --agents business-boss,business-pusher,life-rookie,business-watcher,life-cynic
```

Mixed lineup: business-boss decides, life-rookie and life-cynic keep the burnout question alive while business voices handle pipeline, entity, and contracts. 16 Agent calls, $0.75 estimated cost.

## License

MIT. Do what you want, no warranty.

## Credits

Built by [Karl Certa](https://github.com/karl-cta). Inspired by every meeting where the quiet person turned out to be right.
