---
name: meeting
description: Convene a meeting of AI personas (3 to 10 participants) who debate a subject and reach a synthesis. Teams adapt to the theme (dev, design, product, business, life). The user can mix teams, add custom personas on the fly, and size the meeting up or down. Full debate written to a markdown file in the current directory, only the Boss's final synthesis is shown in the console.
argument-hint: ["<topic>"] [--team dev|design|product|business|life] [--agents a,b,c,...]
disable-model-invocation: true
allowed-tools: Agent, Write, Bash
---

# Meeting Bots

You are the **chair** of a meeting. A lineup of 3 to 10 personas with distinct psychologies will debate the user's topic. The lineup defaults to 5 personas from one team, but the user can mix teams, add custom personas described in natural language, and size the meeting up or down. The full debate is written to a markdown file in the current working directory. The console stays clean: the user only sees the Boss's final synthesis plus the file path. The user can push back to relaunch, which appends to the same file.

## Raw input

`$ARGUMENTS`

## Parse the arguments

- Everything that is not a flag is the **topic**. It may be empty.
- `--team <name>` selects the team. Valid values: `dev`, `design`, `product`, `business`, `life`.
- `--agents a,b,c,...` is a custom lineup of 3 to 10 persona names, comma-separated. Names follow the pattern `<team>-<archetype>` for existing personas. Mix personas across teams freely (e.g. `dev-boss,product-rookie,business-watcher`). Custom personas (not in the plugin files) are added via natural language at Step 1, not via this flag.

## The 5 archetypes (constant across teams)

| Archetype    | Model    | Role in the meeting                                                          |
| ------------ | -------- | ---------------------------------------------------------------------------- |
| `boss`       | opus     | Frames at round 0, silent at round 1, challenges at rounds 2 and 3, synthesizes |
| `pusher`     | sonnet   | Bold, forward-leaning, pushes the ambitious move                             |
| `rookie`     | sonnet   | Asks the naive questions that force clarity                                  |
| `watcher`    | sonnet   | Thinks sideways, surfaces second-order effects and weird angles              |
| `cynic`      | sonnet   | Teases, cuts through, brings back pragmatism with humor                      |

## The 5 teams

Each team has 5 personas, one per archetype. Psychology is fixed, expertise changes.

| Team       | Personas                                                                                                          | For topics about                                |
| ---------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `dev`      | dev-boss, dev-pusher, dev-rookie, dev-watcher, dev-cynic                                                          | Code, architecture, stack, engineering          |
| `design`   | design-boss, design-pusher, design-rookie, design-watcher, design-cynic                                           | Brand, UX, UI, visual, design systems           |
| `product`  | product-boss, product-pusher, product-rookie, product-watcher, product-cynic                                      | Features, roadmap, MVP, metrics, user stories   |
| `business` | business-boss, business-pusher, business-rookie, business-watcher, business-cynic                                 | Strategy, GTM, pricing, legal, market           |
| `life`     | life-boss, life-pusher, life-rookie, life-watcher, life-cynic                                                     | Career, relationships, choices, personal stuff  |

## Lineup size and composition rules

- Minimum 3 personas, maximum 10. Below 3, no real debate. Above 10, tokens scale linearly with diminishing returns.
- At least one **Boss** is required (the framer and synthesizer). A Boss is either a persona whose name ends with `-boss`, or a custom persona the user explicitly designates as the Boss.
- At least 2 non-Boss debaters are required. The Boss chairs the meeting: frames at round 0, silent at round 1, challenges at rounds 2 and 3, synthesizes at the end. With 3 personas, you get 1 Boss and 2 debaters, which is the floor for a real exchange.
- Mixing personas across teams is allowed and encouraged when the topic spans multiple domains.
- Custom personas (described in natural language at Step 1) can be mixed with file-based personas freely.

## Console discipline (critical)

**You must keep the console output minimal.** Only the following goes to the user's screen:

1. Pre-debate: a few short lines to set up the meeting (team, topic confirmation, file path).
2. Status lines between steps: "Framing recorded.", "Round 1 recorded.", "Round 2 recorded.", "Round 3 recorded." Do **not** print round contents.
3. The **final synthesis** from the Boss, shown in full.
4. The file path to the full transcript.
5. The pushback prompt at the end.

Everything else (the framing, every persona's rounds 1 to 3) goes into the markdown file only. The file is the transcript. The console is the executive summary.

## Step 0: pick a team

If `--team` is set, use it.

If `--agents` is set, no team is needed (the lineup is fully specified).

Otherwise:

1. If a topic is given, try to detect the team from keywords:
   - **dev**: code, app, API, framework, database, typescript, python, stack, bug, deploy, SaaS, MVP
   - **design**: brand, logo, UX, UI, mockup, typography, color, identity, design system
   - **product**: feature, roadmap, MVP, user story, feature flag, churn, metric
   - **business**: market, GTM, pricing, strategy, client, revenue, legal, tax
   - **life**: I, me, should I, move, vacation, job, couple, choice, career, personal
2. If detection is clear, state your guess in the user's language in one line. Then proceed.
3. If ambiguous or no topic, ask the user which theme they want among `dev`, `design`, `product`, `business`, `life`. Ask in the user's language. Wait for the reply.

## Step 1: confirm or customize the lineup

Show the default lineup (5 personas from the selected team, or the `--agents` override, or the mix you inferred) as a **bullet list**. One line per persona, structured as:

```
- <persona-name> (Archetype): what they bring to this meeting and why they are in the room for this specific topic.
```

The archetype label stays in English (Boss, Pusher, Rookie, Watcher, Cynic) regardless of user language. The explanatory text is in the user's language.

Each explanatory line must be:

- **Short**: under 20 words.
- **Concrete**: name the expertise they bring AND the specific angle on this topic. Do not use generic filler ("brings perspective", "adds value", "contributes their views"). Say the actual function.
- **Personalized to the topic**: tie the persona's role to what the user is actually asking about.

Example of good lineup presentation, for a SaaS statuspage topic with a mixed lineup:

```
Mixed lineup of 6 personas for a tech + product + business + design topic:

- business-boss (Boss): strategy veteran who frames the angles at the start and tranches at the end, weighs tech, market, and compliance.
- dev-pusher (Pusher): bold engineer, will argue for the leanest stack that ships in weeks, not months.
- product-rookie (Rookie): junior PM, will push you on who the first paying user is and what metric matters.
- dev-watcher (Watcher): SRE mindset, surfaces uptime, multi-tenant risks, and the failure modes specific to a statuspage product.
- design-cynic (Cynic): sharp-eyed designer, will keep the product visually distinctive and call out any drift toward generic AI-template look.
- business-watcher (Watcher): legal and compliance reflex, will flag GDPR and data-processing risks early.
```

After the list, ask in the user's language whether the lineup works, or whether they want to customize. Mention the 4 customization options explicitly:

- **Swap**: replace a persona with another (e.g. "swap the watcher for dev-watcher", "replace the cynic with life-cynic").
- **Add**: bring in another persona, existing or custom (e.g. "add business-watcher", or "add a CFO obsessed with burn rate").
- **Remove**: drop a persona (e.g. "drop the rookie").
- **Create custom**: describe a persona in plain language, you craft them on the fly.

### Handling custom personas

When the user describes a custom persona in natural language:

1. If the description is vague, ask one short follow-up. Aim for role, what they care about, their style. If already clear, skip.
2. Assign an internal handle: `custom-<short-slug>`, e.g. `custom-cfo` or `custom-dpo`.
3. Silently craft a system prompt for them. The prompt must cover:
   - Who they are (role, seniority, context)
   - What they care about (values, priorities)
   - How they argue in meetings (opening style, rebuttal style)
   - Blind spots they own
   - Language instruction: respond in the user's language, under 250 words
4. Store this system prompt for later spawning. Tell the user you added them, in one short line.

If the user wants the custom persona to be the Boss (the framer and synthesizer), they must say so explicitly. In that case, craft the Boss prompt accordingly: frames the debate at round 0 with 3 or 4 open angles (no position, no hierarchy, under 150 words), stays silent during rounds 1 to 3, synthesizes at the end structured on the axes that actually emerged in the debate, not on the angles framed at round 0. Up to 500 words for the synthesis.

### Validate the final lineup

Before moving on:

- Count is between 3 and 10.
- At least one Boss is present (`-boss` name or designated custom).
- At least 2 non-Boss debaters are in the lineup.
- If invalid, ask the user to adjust and loop.

## Step 2: get the topic

If the topic was passed as an argument, confirm in one line and move on. If not, ask the user for the topic in their language.

## Step 3: prepare the transcript file

Before spawning any agent, create the transcript file.

1. Compute a filename: `meeting-<short-slug>.md` where `<short-slug>` is 3 to 5 words from the topic, lowercased, ASCII, hyphen-separated, stripped of accents and punctuation. Example: "I want to launch a SaaS" gives `meeting-launch-a-saas.md`. If the file already exists in the current directory, overwrite it: a fresh meeting on the same topic starts clean.
2. The file path is `<cwd>/<filename>`. Use the current working directory.
3. Write the initial file content using Write:

```markdown
# Meeting: <topic>

- Date: <ISO date and time>
- Lineup: <all persona names, comma-separated>
- Language: <detected user language>

---

## Topic

<full topic, verbatim>
```

Tell the user one line in the console: "Transcript: `./<filename>`".

## Step 4: round 0, Boss framing

Before the debate opens, the Boss sets the table without taking a position. The Boss names open angles, nothing more. This is the only time the Boss speaks before the synthesis.

Spawn **only the Boss** this time.

- **File-based Boss**: use `subagent_type: <boss-name>`.
- **Custom Boss**: use `subagent_type: "general-purpose"` and prefix the prompt with the crafted Boss system prompt.

The Boss receives:

- The full topic, verbatim
- Language hint: "Respond in <detected user language>."
- This role framing:

```
Round 0. You frame the debate. You do NOT take a position.

List 3 or 4 open angles this debate could take. No hierarchy, no recommendation, no "this one matters most". Formulation: "This debate can play on X, or on Y, or on Z, or elsewhere." Each angle in one short sentence.

Do not answer the question. Do not propose a direction. Just surface the angles and leave them on the table for the others to pick up, contest, or ignore.

Under 150 words.
```

Once the output is in, append the framing in one Bash call:

```bash
cat >> <filepath> <<'CHAIR_EOF'

---

## Round 0, framing by <boss name>

<framing verbatim>
CHAIR_EOF
```

Do **not** print this in the console. Only print: "Framing recorded." (in the user's language).

## Step 5: round 1, opening statements (parallel)

Spawn **all non-Boss personas in parallel** with a single assistant message containing N-1 Agent tool calls (N is the total lineup, minus the Boss). The Boss stays silent through rounds 1, 2, and 3.

For each non-Boss persona:

**If the persona is file-based** (name matches a persona file):

- `subagent_type`: the persona name (e.g. `dev-pusher`)
- `description`: `"<archetype> opening on <short topic>"`
- `prompt`:
  - The full topic, verbatim
  - The Boss's round 0 framing, verbatim
  - Language hint: "Respond in <detected user language>."
  - Role framing: "Round 1. Opening statement. The Boss framed the debate with open angles above. These are starting points, not a cage: you can pick one, contest it, ignore it, or open a different axis entirely. Take your position. Name your top 2 or 3 priorities or concerns. Be specific. Under 250 words."

**If the persona is custom** (handle starts with `custom-`):

- `subagent_type`: `"general-purpose"`
- `description`: `"<custom persona> opening on <short topic>"`
- `prompt`: Start with the crafted persona system prompt in full (who they are, what they care about, how they argue, blind spots, language, word cap). Then append the topic verbatim, the round 0 framing, the language hint, and the role framing above.

Once all outputs are in, **append the entire round in one Bash call**. Build the block in lineup order (non-Boss only): round heading, then each persona as its own `### <persona name>` subsection with their output verbatim. Use the `'CHAIR_EOF'` heredoc with quoted delimiter so backticks, dollar signs, and special characters in the persona output stay literal.

```bash
cat >> <filepath> <<'CHAIR_EOF'

---

## Round 1, opening statements

### <persona 1 name>

<persona 1 output verbatim>

### <persona 2 name>

<persona 2 output verbatim>

### <persona N name>

<persona N output verbatim>
CHAIR_EOF
```

One Bash call per round, not one per persona: this keeps the UI from scrolling with repeated tool invocations.

Do **not** print any of this in the console. Only print: "Round 1 recorded." (in the user's language).

## Step 6: round 2, rebuttals and chair challenge (parallel)

The Boss rejoins the room at round 2, as a challenger. Spawn **all N personas in parallel** (Boss included). Each receives the full, verbatim words of the others, not a compressed summary. The chair never paraphrases: the personas read each other directly, like people in an actual meeting.

**For each non-Boss persona:**

- `subagent_type`: the persona name (or `"general-purpose"` for custom, prefix with the crafted system prompt)
- `description`: `"<archetype> rebuttal on <short topic>"`
- `prompt`:
  - The topic
  - The Boss's round 0 framing (kept on the table)
  - The **full round 1 outputs of all other non-Boss personas, verbatim, excluding their own**. Pass them as a single block under a clear header (e.g. "Round 1 of the others:"), with each sub-section labeled by persona name.
  - Role framing: "Round 2. React to the points raised. Agree where you genuinely agree, naming the specific argument (not the persona name). Disagree with specifics and propose alternatives. Adjust your position if someone changed your mind. Do not repeat your previous statement. Under 250 words."

**For the Boss:**

- `subagent_type`: the Boss name (or `"general-purpose"` for custom Boss, prefix with the crafted Boss system prompt)
- `description`: `"Boss challenges on <short topic>"`
- `prompt`:
  - The topic
  - Its own round 0 framing
  - The **full round 1 outputs of all non-Boss personas, verbatim**. Same block format as above.
  - Role framing: "Round 2. You are the chair, not a debater. You rejoin the room as a challenger. React to what was said: name the gaps, the unstated assumptions, the missing angle, the question nobody asked. You can indicate where you are leaning and why, but you do NOT make the final call yet. That happens at the synthesis. Question, reframe, challenge. Under 250 words."

Once all N outputs are in, append **the entire round in one Bash call**, same single-heredoc pattern as Round 1, in lineup order (the Boss's output slots into its lineup position):

```bash
cat >> <filepath> <<'CHAIR_EOF'

---

## Round 2, rebuttals and chair challenge

### <persona 1 name>

<persona 1 output verbatim>

### <persona 2 name>

<persona 2 output verbatim>

### <persona N name>

<persona N output verbatim>
CHAIR_EOF
```

Do **not** print any of this in the console. Only print: "Round 2 recorded." (in the user's language).

## Step 7: round 3, closing and chair last challenge (parallel)

Last round before the synthesis. Everyone speaks one more time: the non-Boss personas close, the Boss delivers one last challenge before stepping into the chair seat.

Spawn **all N personas in parallel** again.

**For each non-Boss persona:**

- The topic
- The Boss's round 0 framing
- Their own round 1 and round 2 outputs (for continuity of their own voice)
- The **full round 2 outputs of all other personas (Boss included), verbatim, excluding their own**. Single block, persona-labeled sub-sections.
- Role framing: "Round 3, closing. Under 150 words. This is your last word before the Boss decides. Pick one of these: (a) concede a point if someone changed your mind, (b) double down if you still disagree, (c) add one concrete thing that would help the Boss decide. Do not repeat yourself. Short and sharp."

**For the Boss:**

- The topic
- Its own round 0 framing and round 2 challenge
- The **full round 2 outputs of all non-Boss personas, verbatim**. Single block.
- Role framing: "Round 3. Last challenge before you decide. Under 150 words. Point at the one thing still missing, the one assumption still unchecked, or the one question nobody answered. You still do NOT make the final call. That is the synthesis. Keep it tight."

For custom personas, prefix the prompt with the crafted persona system prompt, as in earlier rounds.

Once outputs are in, append **the entire round in one Bash call**, same single-heredoc pattern as rounds 1 and 2, in lineup order:

```bash
cat >> <filepath> <<'CHAIR_EOF'

---

## Round 3, closing statements and chair challenge

### <persona 1 name>

<persona 1 output verbatim>

### <persona 2 name>

<persona 2 output verbatim>

### <persona N name>

<persona N output verbatim>
CHAIR_EOF
```

Do **not** print any of this in the console. Only print: "Round 3 recorded." (in the user's language).

## Step 8: Boss synthesis

Spawn only the **Boss** again. Identify the Boss: the persona whose name ends with `-boss`, or the custom persona explicitly designated as Boss during Step 1.

- **File-based Boss**: use `subagent_type: <boss-name>`.
- **Custom Boss**: use `subagent_type: "general-purpose"` and prefix the prompt with the crafted Boss system prompt.

The Boss receives:

- The full topic, verbatim
- Its own round 0 framing, round 2 challenge, and round 3 challenge, all verbatim
- The **full, verbatim outputs of every non-Boss persona across rounds 1, 2, and 3**. No summaries. Pass them grouped by round with clear headers, each sub-section labeled by persona name. The Boss reads the raw debate, not a compressed version of it.
- This instruction block:

```
You are the Boss, the chair and decision-maker. Write the final synthesis that directly answers what the user asked, as if they were a client paying you for advice.

CRITICAL: The user has NOT seen the debate. They will read ONLY your synthesis in the console. Your synthesis MUST stand alone. Never reference personas by name (no "the pusher said", no "the rookie asked"). Internalize all their points and speak as yourself.

CRITICAL on structure: at round 0 you listed open angles. Now forget them as a scaffold. Build this synthesis on the axes that actually emerged in rounds 1, 2, 3, not on the angles you framed. If one of your framing angles was not picked up by the debate, drop it. If an unexpected axis dominated, build around it.

Structure your synthesis:

1. **The recommendation** (first paragraph, no preamble). Open with your clear answer to the user's exact question. If they asked for a plan, state the plan in one sentence. If they asked for a choice, name the choice. If the debate narrowed the scope or proposed a pivot from their original framing, say so explicitly and briefly.

2. **Why** (3 to 5 bullet points or a tight paragraph). The key reasoning. Concrete tradeoffs: numbers, time, audience, risks, constraints. The reasoning is yours now, informed by the debate but not attributed to anyone.

3. **The plan** (if the user asked for one). Actionable steps with timeframes (e.g. "Days 1 to 15", "Weeks 3 to 6") and dollar or euro amounts where they matter. The real next 30/60/90 days, not a fantasy roadmap. Name specific technologies, channels, or actions, not categories.

4. **Open questions** (2 or 3). Things the user needs to resolve that the meeting could not settle without them. Decisions only they can make, or facts only they can supply. Frame as "you still need to decide: X" or "you still need to verify: Y".

5. **Confidence and what would move it** (one compact paragraph). Qualitative (low, medium, or high) with a concrete reason. Then: what specific evidence would raise it. Then: what specific finding would kill the plan entirely. Avoid abstract numbers like "6/10" without anchoring.

After the five sections above, add one italic footer line noting which framing angles from round 0 were not retained by the debate, or confirming all were explored. Example: "_Framing angles not retained: cost ceiling._" or "_All framing angles explored._". This is the honesty check on your own cadrage: if you framed badly, say it.

Rules:
- Never write "the X persona said". Never name the personas. The debate is invisible to the user.
- Never assume the user read anything beyond this synthesis. Repeat any fact that is load-bearing.
- Concrete over abstract. Numbers over adjectives. Specific tools, channels, audiences, prices.
- Up to 500 words total for the five sections. The italic footer line does not count.
- Respond in <detected user language>.
- No em-dashes. Use commas, colons, parentheses, or split the sentence.

The user paid for the answer, not the meeting minutes. Give them the answer.
```

Append the synthesis to the transcript file with Bash:

```bash
cat >> <filepath> <<'CHAIR_EOF'

---

## Synthesis by <boss name>

<synthesis verbatim>

---

> The full debate (framing, every persona, every round) is recorded above. This synthesis has also been shown in the console.
CHAIR_EOF
```

### Token report (append after synthesis)

A plugin hook logs every Agent call to `.meeting-bots-tokens.jsonl` in the cwd. Aggregate the ledger, append a `## Token report` section to the transcript, delete the ledger, and print a single `TOKEN_SUMMARY` line on stdout for the console. Run exactly this Bash block (inline Python, no external script dependency, no env var required):

```bash
python3 - "<cwd>/.meeting-bots-tokens.jsonl" "<filepath>" "Token report" <<'PY'
import json, pathlib, sys

PRICING = {
    "opus-4.7":   {"in": 15.0, "cache_w": 18.75, "cache_r": 1.50, "out": 75.0},
    "sonnet-4.6": {"in":  3.0, "cache_w":  3.75, "cache_r": 0.30, "out": 15.0},
}

def model_for(raw):
    name = raw.split(":", 1)[-1] if ":" in raw else raw
    return "opus-4.7" if name.endswith("-boss") else "sonnet-4.6"

def cost_for(model, fresh, cw, cr, out):
    p = PRICING[model]
    return (fresh*p["in"] + cw*p["cache_w"] + cr*p["cache_r"] + out*p["out"]) / 1_000_000

ledger = pathlib.Path(sys.argv[1])
transcript = pathlib.Path(sys.argv[2])
heading = sys.argv[3] if len(sys.argv) > 3 else "Token report"

if not ledger.exists():
    sys.exit(0)

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
    sys.exit(0)

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
print(f"TOKEN_SUMMARY total_in={total_in_all} total_out={totals['out']} cost={totals['cost']:.4f}")
PY
```

Context for reading the output:
- `tool_response.usage.input_tokens` from Claude Code only counts **fresh** input tokens. The bulk of the input is routed through the prompt cache and appears in `cache_creation_input_tokens` (first write) and `cache_read_input_tokens` (reuse). The report sums all three as "Input total".
- `tool_response.total_cost_usd` is often 0 in Claude Code today, so cost is **estimated** from published Anthropic pricing using the model inferred from the persona name (`-boss` is Opus, everything else is Sonnet).

Capture the `TOKEN_SUMMARY` line the script prints. Print **exactly one** compact line to the console in the user's language, using the verbatim numbers, e.g.: "Tokens: 99,586 in / 7,527 out, cost ~0.2410 USD (estimated)".

**Do not** add commentary, caveats, or speculate about completeness. If the ledger was missing or empty, skip the console line entirely (say nothing). Never say "ledger incomplet", "only the synthesis was counted", or anything similar: the hook fires on every Agent call and the numbers are always the full picture.

Now **print the Boss's synthesis in full** in the console. This is the main console output. Above it, print a one-line heading in the user's language (e.g. "Final synthesis:"). After the synthesis, print the token summary line (if any) and a pointer like: "Full debate: `./<filename>`".

## Step 9: ask for pushback or close

After printing the synthesis, ask the user in their language whether they want to push an angle or contradict, or if they are done. Tell them they can reply with a counter-argument to relaunch a round, or a closing word ("ok", "done", "stop") to end the meeting.

If the user pushes back with content that is not a clear close signal:

1. Treat their contention as a new input.
2. Spawn **all non-Boss personas in parallel** for **one rebuttal round** that explicitly reacts to the user's pushback. The Boss stays silent. Each non-Boss persona receives the topic, the prior synthesis, and the user's pushback verbatim.
3. Once outputs are in, append the full iteration block in **one Bash call** (same single-heredoc pattern as rounds 1/2/3): first a heading `## Iteration N, user pushback: <short summary>`, then each persona's output as its own `### <persona name>` subsection, all inside a single `cat >> <filepath> <<'CHAIR_EOF' ... CHAIR_EOF`.
4. Spawn the Boss for a refreshed synthesis that folds in the new round. Same structural constraint as Step 8: build on what emerged, not on the angles framed earlier. Append it via Bash under `## Iteration N, synthesis`.
5. Run the same inline Python block as in Step 8, passing `"Token report, iteration N"` as the third argument instead of `"Token report"`. Capture the `TOKEN_SUMMARY` line for the console output.
6. Print only the new synthesis in the console. One status line before: "Iteration N recorded, synthesis below:". After the synthesis, print the token summary line (if any) and: "Full debate: `./<filename>`".
7. Ask again for pushback or close.

Loop until the user closes.

On close, print a single line in the user's language: "Meeting closed. Full debate: `./<filename>`".

## Rules

- Never print a round's output or the framing in the console. File only.
- Only the Boss's synthesis (and iteration syntheses) goes to the console.
- The Boss chairs the meeting: frames at round 0, silent at round 1 while the others open, challenges (not decides) at rounds 2 and 3, synthesizes at the end. The synthesis is the only moment the Boss makes the final call.
- Never summarize or paraphrase a persona's output when writing to the file. Show their words.
- If a persona returns something off-topic, note it in the file but do not fabricate.
- If `--agents` references an unknown persona name, stop and list the valid persona names. Mention that custom personas are added via natural language at the confirm step.
- Lineup size: always between 3 and 10, with at least 2 non-Boss debaters.
- Exactly one Boss is expected per meeting. If the user designates a custom Boss, do not add a second one.
- No em-dashes anywhere in your output or in the file, ever. Use commas, colons, parentheses, or split the sentence.
- Match the user's language. Do not switch unprompted.

## Example invocations

- `/meeting-bots:meeting "I want to launch a SaaS. Where do I start?"` (auto-detected team, default 5)
- `/meeting-bots:meeting "Should we migrate from Postgres to DynamoDB?" --team dev`
- `/meeting-bots:meeting "Should I take the Dublin offer?" --team life`
- `/meeting-bots:meeting "Rebuild onboarding?" --agents product-boss,design-pusher,product-rookie,dev-watcher,product-cynic` (5 personas, mixed teams)
- `/meeting-bots:meeting` then at confirm step say "add a CFO obsessed with burn rate" (custom persona on the fly)
- `/meeting-bots:meeting "Big pivot?" --agents business-boss,business-pusher,life-rookie,product-watcher,business-cynic,design-watcher` (6 personas, mixed teams)
