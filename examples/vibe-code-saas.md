# Meeting: Vibe coding a SaaS invoicing tool for freelancers

- Date: 2026-04-19
- Lineup: dev-boss, dev-pusher, dev-rookie, dev-watcher, dev-cynic
- Language: English

---

## Topic

I want to vibe code a SaaS end-to-end: a simple invoicing tool for freelancers who hate Stripe's dashboard. I'll direct the AI but I'm not a pro dev. Before I write a line, help me plan: what technical constraints to lock in upfront, what to build first, where I need to make the call myself rather than let the AI decide, and how I avoid the "works on my laptop, dies in prod" trap.

---

## Round 0, framing by dev-boss

Alright. Invoicing tool, vibe-coded, non-pro dev at the wheel. I have seen this movie. Sometimes it ships, sometimes it becomes a folder of abandoned repos. Let me put the angles on the table before anyone jumps.

This debate can play on the **stack lock-in axis**: what you pick on day one (language, framework, DB, hosting) will be the thing you cannot undo in six months, and AI is great at writing code but terrible at picking boring defaults for you.

Or on the **scope axis**: invoicing sounds simple until you hit taxes, multi-currency, PDF rendering, email deliverability, and legal archival. What is the actual v1?

Or on the **human-in-the-loop axis**: where must you override the AI, precisely because it will confidently generate plausible nonsense (auth, money handling, data model, migrations).

Or on the **prod-readiness axis**: the gap between "runs locally" and "handles a real customer's data Friday at 11pm" is where vibe-coded SaaS usually dies.

Or elsewhere.

Floor is open.

---

## Round 1, opening statements

### dev-pusher

Stack lock-in is the one that kills non-dev founders and I want to talk about it first.

The AI will happily scaffold you a Next.js app with Prisma, Postgres, Stripe webhooks, and a custom auth layer in 20 minutes. It will look complete. It is a trap. You now own a distributed system with five moving parts you cannot debug when something breaks at 11pm. And something will break.

My prescription: pick the most boring, batteries-included stack that exists today. That means Next.js with Supabase (Postgres + auth + storage out of the box), Vercel for hosting, and Stripe for payments even if you hate the dashboard, because the alternative is writing your own payment reconciliation logic. You do not want that. Nobody wants that.

Lock those in before you write a prompt. Tell the AI "we use Supabase auth, never roll custom sessions." Make it a rule, not a suggestion.

Second priority: data model first, features second. Invoicing has a deceptively simple core: Client, Invoice, LineItem, Payment. Get that schema right before you build a single UI. The AI will drift the schema every session if you let it. Write it down, version it, treat it like law.

Third: PDF generation is not a nice-to-have you add later. It is the product. A freelancer's invoice IS a PDF. If you do not nail this in week one you will rebuild half the data model when you finally tackle it.

Those three decisions made upfront save you from the 80% of vibe-coded SaaS that never ships.

### dev-rookie

Wait, before we talk about what to build first, can we agree on what "vibe coding" actually means here?

Because it means two different things and they have totally different consequences.

Version A: the human makes all architectural decisions, uses AI to write the implementation. You still understand what you are building, you just type less.

Version B: the human describes what they want, AI makes the calls, human accepts or rejects output. The human does not fully understand what ended up in the codebase.

This matters a lot for an invoicing tool because invoices touch money, legal archival, and user trust. If a bug eats an invoice, your user loses a real payment. If your data model is wrong on day one, migrations on a live DB with real customer data are genuinely dangerous, and AI-generated migrations are some of the scariest code I have seen.

So my first concern is: does "I'll direct the AI" mean you understand the decisions, or you approve the output? That line is the difference between a risky project and a ticking clock.

My second concern is the definition of v1. The Boss named it: invoicing sounds scoped until it is not. What does this tool actually do on day one? Send a PDF to a client? Track payment status? Handle partial payments? Taxes? Every yes answer is a new surface where AI can generate plausible wrong code.

Can we define the absolute smallest v1 that a real freelancer would pay for? Not someday. Next month.

### dev-watcher

The prod-readiness axis is the one that kills this project. Not the stack, not the scope. The gap between "AI wrote me a working invoicing flow" and "a real human's real money is in this system on a Friday night" is where vibe-coded SaaS goes to die quietly.

Here is the specific scenario the room is not considering: Stripe webhooks. The AI will generate a webhook handler that looks completely correct. It will work in testing. It will fail in production under one condition: the webhook arrives twice. Or out of order. Or the handler throws after Stripe already marked the event delivered. Now you have a customer whose invoice says "paid" but your database says "pending," or the reverse. You wake up to a support email from someone who cannot send their own client a receipt.

The AI does not know to make webhook handling idempotent. It does not know to store the Stripe event ID and check for duplicates before acting. It will not tell you it forgot. It will write confident, plausible, broken money handling.

My top three concerns, in order:

One: money state transitions. Every place where payment status changes must be explicit, logged, and idempotent. The AI needs to be told this constraint before it writes a single line of payment code.

Two: data migrations. The AI will generate a schema. You will change it. You need a migration tool locked in from day one, not bolted on after three months of manual ALTER TABLE regret.

Three: email deliverability. Invoices sent from a misconfigured domain hit spam. The customer never sees the invoice. You never know.

### dev-cynic

Alright, invoicing SaaS, vibe-coded, non-dev at the wheel. I have seen this exact pitch approximately once per quarter since GPT-4 dropped. Sometimes it ships. Usually it becomes a cautionary tale someone posts on Hacker News.

Let me name the two places where vibe-coding specifically kills this project, not just "hard things are hard."

**First: the data model is the product.** An invoice is not a form. It is a legal document with a sender, a recipient, line items, taxes, a state machine (draft, sent, paid, void, disputed), and audit history. The AI will generate you a `invoices` table with five columns on day one and you will spend month three migrating production data because the model was wrong. Lock the schema before you write a line of UI. Draw it on paper. Argue with it. That is the one thing you cannot let the AI decide, because it will decide confidently and incorrectly.

**Second: auth is not a feature, it is a liability.** Non-dev founders vibe-coding auth is where accounts get compromised. Use something off the shelf, Clerk, Auth0, Supabase Auth, whatever. Do not touch it. Do not customize it. The AI will happily write you a JWT implementation with a hardcoded secret. Say no.

The prod-readiness angle is real but it is downstream of these two. Fix the model, outsource auth, and half the "dies in prod" scenarios disappear before you write a line.

What I would actually want to debate: is Stripe really the problem, or is it the pricing page?

---

## Round 2, rebuttals and chair challenge

### dev-boss

Good opening. Four of you converged faster than usual, which makes me nervous. Let me name what nobody said.

**The unstated assumption in this room**: you are all designing for a founder who will be at the keyboard for 12 months. The user said "vibe code end-to-end." Nobody asked what happens in month 4 when the AI generates a fix for a bug it introduced in month 2 and the founder cannot tell. The operator skill gap compounds. That is the real risk, not webhooks.

**The gap on scope**: Rookie asked the right question and the room moved on. "Smallest v1 a real freelancer would pay for" is not answered by "PDF + payment tracking." It is answered by talking to three freelancers this week. Without that, you are vibe-coding a product nobody validated, which is the cheaper failure mode than a broken webhook.

**The gap on legal**: invoicing has jurisdiction. France requires sequential numbering and 10-year archival. EU e-invoicing mandates are landing in 2026 and 2027. Nobody mentioned which country's freelancers this serves. That decision reshapes the data model more than any schema debate.

**Where I am leaning**: the data-model-first and outsource-auth points are correct and boring, which is why they are right. The webhook idempotency point is correct but premature; you do not need it in v1 if v1 does not touch Stripe yet.

**The question I want answered before synthesis**: what does the user mean by "end-to-end"? Landing page to paid customer, or localhost to deployed? Those are different projects.

### dev-pusher

The cynic landed the best point in the room: the data model is the product. I will go further. Before the user writes a single prompt, they need to draw the invoice state machine on paper. Not in code, not in a schema, on paper. Draft, sent, viewed, paid, void, disputed. Every arrow is a business rule. The AI cannot invent those rules for you because they are your product decisions.

The rookie's Version A vs Version B framing is the right question but I think it dissolves into a simpler rule: any decision you cannot explain to a friend in one sentence, the AI should not be making. Stack choice, schema shape, auth provider. Those are yours. Function bodies, form validation, PDF layout. Those are the AI's.

The watcher's webhook idempotency point is correct and concrete. I want to add: this is also the easiest problem to constrain away. One rule, stated once to the AI before it writes payment code: "Every Stripe event handler must check for duplicate event IDs before acting." That is a prompt constraint, not a skill gap.

Where I will push back on the room's general caution: the risk of over-planning this into paralysis is just as real as the risk of shipping broken money code. The smallest v1 that earns money is: create invoice, send PDF by email, mark as paid manually. No Stripe webhook at all. Manual payment confirmation. That is a real product a real freelancer would pay for, and it sidesteps the entire async payment state machine problem until you have actual revenue to justify solving it.

### dev-rookie

The webhook idempotency point is the one that genuinely surprised me. I came in thinking "stack choice is the scary decision" but actually the stack is recoverable. A double-processed payment that credits the wrong account is a support nightmare, maybe a legal one. That specific failure mode deserves a name in the docs before you write a single handler.

But I want to push on something nobody has defined yet: what does "non-pro dev" actually mean here? Because the advice changes a lot depending on the answer.

If it means "I can read code and prompt precisely," then Supabase plus Vercel plus a schema-first approach is totally reasonable. If it means "I paste AI output and move on," then even a batteries-included stack is dangerous because you will not catch the webhook handler that looks right but is not.

The "data model is the product" argument about invoices being legal documents landed for me. But I want to ask: what is the actual minimum legal surface? Is it just sender, recipient, line items, a total, and a date? Or does country of business already matter for v1? Because if you are building for EU freelancers, VAT is not optional, and that changes the schema before you write anything.

That is the scope question nobody answered yet. "Simple invoicing tool" is not a spec. What countries, what currencies, what tax regimes? That decision shapes the data model more than any framework choice.

Who decides that, if not the AI?

### dev-watcher

Agreed on two things without reservation: lock the schema before writing UI, and outsource auth completely. Those are not paranoia, they are table stakes. The state machine argument especially: an invoice that can silently transition from "sent" to "draft" because a migration dropped a column is not a bug, it is a legal problem.

Here is what the room has not said yet about the "boring stack" recommendation: Supabase is three external services pretending to be one. Auth, storage, and Postgres over REST. That is fine until Supabase has a regional incident, which they have had. Your user is trying to send an invoice to a client with a payment deadline. Your app returns 503. Your user cannot even log in to tell the client what is happening. That is not a Supabase-specific critique, it is what happens when you treat any managed platform as invisible infrastructure.

The question is not whether to use it, it is whether you have a graceful degraded state. Can the user at least see their invoice list if realtime is down? Or does the whole app go white?

The Rookie's vibe-coding taxonomy is the sharpest thing said in round one. Version B, where the human approves output without understanding it, is specifically dangerous for the migration surface. AI generates a migration, human runs it, production data changes. That sequence has no undo button if the migration was wrong and the AI hallucinated a column type that silently coerces your stored amounts.

The answer is: never run an AI-generated migration without reading every line yourself.

### dev-cynic

Right, three rounds in and the room has basically converged on "this is hard, pick boring tools, define v1." Solid advice. Also advice that exists in approximately forty blog posts from 2019.

Let me poke at what is actually being said here.

The stack sermon is correct but incomplete. Supabase plus Vercel plus Stripe is a fine choice. It is also three vendor lock-ins dressed up as "boring defaults." The real constraint is not which SaaS you pick, it is whether you can read the error when one of them fails at 11pm. If you cannot read a Supabase log or parse a Vercel function timeout, the boring stack does not save you, it just gives you a nicer 404.

The webhook idempotency point is the most load-bearing thing anyone said. That is not a "be careful" warning, that is a hard requirement. The AI will not add it by default. You have to write the constraint in the prompt, every time, and verify it in the output. That is the actual human-in-the-loop job: not approving vibes, but knowing the three or four things the AI will confidently get wrong with money.

The rookie's question about "Version A vs Version B" vibe coding is the one nobody actually answered. It is also the one that determines whether this project ships or becomes a very polished README. Worth pinning before we move on.

PDF generation being week-one scope: agree completely. It is not a feature, it is the product. Build the PDF first, wrap the form around it, not the other way.

---

## Round 3, closing statements and chair challenge

### dev-boss

The room is still dodging the question I asked at round 2. "End-to-end" was never defined. Pusher's v1 (create, PDF, mark paid manually) and Cynic's v1 (PDF-first) are not the same product. One is a billing log. The other is a document generator. Different schemas, different first prompts, different customers.

Second unchecked assumption: nobody costed the learning curve. Reading a Supabase log at 11pm is a skill acquired over months. What is the user doing in weeks 1 to 4 to build that skill, before the first paying customer depends on it?

And the legal surface Rookie raised got acknowledged, then dropped. Jurisdiction is not a v2 concern. It determines the schema on day one. France, EU, US are three different products.

Pick: which v1, which jurisdiction, which ops-skill runway. Then we decide.

### dev-pusher

Conceding to Cynic and Watcher: "boring stack" framing is incomplete if you cannot debug it solo at 11pm. That reframes the real constraint from "pick Supabase" to "pick whatever has the clearest error messages and the most Stack Overflow coverage."

One concrete thing for the Boss: the jurisdiction question from Rookie and Boss is not a research task, it is a gate. France + EU e-invoicing 2026/2027 means sequential numbering and VAT handling are not future features, they are schema constraints you cannot retrofit cheaply. Answer "what country, what tax regime" before touching Vercel. That single decision collapses half the open questions in this room.

My v1 scope stands: create invoice, email PDF, mark paid manually. But add one column to Invoice from day one: `legal_sequence_number`. Empty for now, enforced later. Costs nothing to add, costs a migration and potential audit risk to add after.

### dev-rookie

Conceding one thing: Pusher was right that no-webhook v1 sidesteps the idempotency problem entirely. I overcomplicated it.

But my A vs B question is still unanswered and the Boss needs it answered before deciding anything else. Every recommendation in this room assumes Version A. If the answer is actually Version B, the whole plan changes: tighter scope, no migrations without a human reading every line, and probably no custom data model at all, use an existing invoicing API as backend.

One concrete thing for the Boss: ask the user to answer this single question before writing line one. "When the AI proposes a schema change, will you read it and understand it, or approve it because it looks plausible?" The answer routes the entire build strategy.

### dev-watcher

Concede to Pusher on the smallest v1: no webhook is the right call. Manual "mark paid" sidesteps the entire async state machine until you actually need it.

Still doubling down on one thing: never run an AI-generated migration without reading every line, full stop. Not because AI is always wrong. Because a coerced amount column or a silent type change is invisible until a tax audit or a corrupted invoice number sequence. By then the damage is done and there is no rollback that helps you.

One concrete thing for the Boss: the legal surface question from Rookie is the real blocker. France sequential numbering and EU e-invoicing 2027 are not features you add later. They reshape the schema. Lock jurisdiction before locking schema. Ask those three freelancers where they invoice, not what they hate about Stripe.

### dev-cynic

Rookie landed the real grenade: jurisdiction reshapes everything. France sequential numbering plus 2026 EU e-invoicing is not a edge case, it is a schema constraint that belongs in week one, not a compliance ticket you file in month 8.

Concede to Watcher: I undersold the Supabase-as-three-services risk. One vendor, three failure domains. Know which one you actually need.

Concrete thing for the Boss: before the first line of code, write down the answer to two questions on paper. One, which country, which tax regime, which currency. Two, what does "paid" mean legally, is it the Stripe event, the bank transfer, the PDF acknowledgment. These two answers constrain the schema. Everything else is negotiable. Let the AI write the UI. Do not let it answer those two questions.

---

## Synthesis by dev-boss

Do not write a line of code yet. Spend the next two weeks turning three undecided questions into locked constraints, then build the smallest possible invoicing tool around them.

**Why**

- Jurisdiction is a schema constraint, not a feature. France requires sequential invoice numbering with no gaps and 10-year archival. EU e-invoicing (Peppol, structured formats) phases in through 2026 and 2027. US freelancing has none of that but cares about 1099s. These three realities produce three different data models. Picking after you ship means a painful migration on live financial data.
- Your self-honesty about AI output decides the whole build strategy. If you will read every schema change and migration the AI proposes and understand it, you can own a custom Postgres model. If you will paste and approve because it looks plausible, you should not own a schema at all: wrap an existing invoicing API (Stripe Invoicing, Tiime, Indy, Sellsy) and build UX on top.
- "Paid" is a legal event, not a UI state. Decide now what triggers it: a Stripe webhook, a manual mark, a bank reconciliation. That choice defines half your backend.
- Operator skill compounds. Reading a Supabase log, a Stripe event, or a Vercel trace at 11pm is a skill learned over months. You need a runway of small failures on cheap stakes before a paying customer depends on you.
- Smallest v1 that dodges most traps: create invoice, generate PDF, email it, mark paid manually. No webhook, no async state machine, no payment reconciliation. Add payments in v2 once you survive v1.

**Plan**

- Days 1 to 7: talk to 3 freelancers in your target country. Ask where they invoice, what they currently use, what they actually hate. Not "do you like Stripe's dashboard".
- Days 8 to 14: write two pages on paper. Page 1: country, currency, tax regime, numbering rules, archival duration. Page 2: definition of "paid", invoice state machine (draft, sent, paid, void), what is legally mandatory on the PDF.
- Days 15 to 30: stack pick based on error-message clarity, not hype. Next.js + Supabase + Vercel + Resend for email, Clerk or Supabase Auth (never hand-rolled). Add `legal_sequence_number` on the Invoice table day one, even if empty. Set up Prisma or Drizzle migrations, never run an AI-generated migration without reading every line.
- Days 31 to 60: v1 live with 3 beta users from your interviews. PDF generation via react-pdf or a server-side Chromium. No Stripe integration yet.
- Days 61 to 90: add Stripe Payment Links (not webhooks) for v1.5. Webhooks only when a paying customer asks.

**Open questions**

- Which jurisdiction: France only, EU, US, or multi? This is not research, it is a gate before line one.
- Version A or Version B of vibe coding: will you read and understand every schema change, or approve on plausibility? Answer honestly, the plan bifurcates here.
- What does "paid" mean in your product: Stripe event, manual, or bank reconciliation?

**Confidence**

Medium. The plan is sound if you are a Version A operator in a single jurisdiction with 3 real beta users lined up. What raises it: the two pages written and three interviews done by end of week 2. What kills it: discovering you are Version B and still want a custom schema, which means you will ship a legal-grade product you cannot debug.

_Framing angles not retained: none dropped, all four (stack lock-in, scope, human-in-the-loop, prod-readiness) were explored, with jurisdiction and operator skill gap emerging as dominant axes on top._

---

> The full debate (framing, every persona, every round) is recorded above. This synthesis has also been shown in the console.

---

## Token report

Cost is **estimated** from Anthropic public pricing (Opus 4.7 for `-boss`, Sonnet 4.6 for the others). Input total = fresh + cache write + cache read.

| Persona | Model | Calls | Input total | Fresh | Cache write | Cache read | Output | Cost (USD) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| meeting-bots:dev-boss | opus-4.7 | 4 | 38,987 | 24 | 24,284 | 14,679 | 2,403 | 0.6579 |
| meeting-bots:dev-cynic | sonnet-4.6 | 3 | 18,310 | 9 | 9,700 | 8,601 | 910 | 0.0526 |
| meeting-bots:dev-pusher | sonnet-4.6 | 3 | 18,501 | 9 | 12,092 | 6,400 | 925 | 0.0612 |
| meeting-bots:dev-rookie | sonnet-4.6 | 3 | 18,426 | 9 | 9,912 | 8,505 | 826 | 0.0521 |
| meeting-bots:dev-watcher | sonnet-4.6 | 3 | 19,382 | 7 | 7,326 | 12,049 | 889 | 0.0444 |
| **Total** | | 16 | **113,606** | **58** | **63,314** | **50,234** | **5,953** | **0.8683** |

