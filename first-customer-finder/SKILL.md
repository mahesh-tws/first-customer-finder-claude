---
name: first-customer-finder
description: Turns a startup URL, repo, or product idea into a qualified, evidence-backed shortlist of potential first customers using recent PUBLIC signals only -- demand, pain, workaround, switching, and timing signals found via web research. Defines the ideal customer profile, scores fit and timing, links every prospect to its public source, drafts respectful source-based outreach openers, and builds a polished standalone HTML report. Never sends outreach automatically and never enriches private contact data. Use this whenever the user asks to find first customers, potential customers, design partners, early adopters, prospects, or leads, or wants a customer-discovery / prospecting report for a startup, product, or pilot program -- even if they don't use the word "prospecting."
---

# First Customer Finder

## Core principle

A prospect list is only as good as the evidence behind it. Every primary
prospect must trace back to something they (or their company) actually,
publicly said or did -- a forum post, a review, a job listing, a conference
talk, a public GitHub issue -- with a link and a date. This skill never
invents a plausible-sounding prospect from a demographic guess, and never
treats "this company is probably in the target market" alone as a
qualification. Public evidence of pain, demand, or timing is the bar.

This skill relies entirely on **public web research** (Claude's built-in
web search/fetch) -- it does not scrape private data, use contact-enrichment
services, or access anything behind a login wall. That's a hard boundary,
not a style choice; see "Hard rules" below.

## Modes

- **quick** -- up to 5 strong prospects, fastest turnaround
- **standard** (default) -- up to 10 prospects across several source types
- **deep** -- up to 20 prospects plus repeated-pattern analysis across them
- **design-partners** -- prioritizes people publicly describing the problem
  who seem likely to give product feedback, not just buy
- **b2b** -- prioritizes companies and public business triggers (funding,
  hiring, expansion, migration) over individuals
- **community** -- prioritizes explicit public requests and discussion
  threads (people asking "does anyone know a tool for X")

If the user doesn't specify a mode, default to **standard** and say so.

## Workflow

### 1. Understand the product

Read the URL, repo, or description the user gave you. Identify: what problem
it solves, for whom, and what the natural buying trigger looks like (a
workaround failing, a compliance deadline, team growth past some threshold,
a competitor's tool becoming a pain point, etc.). If given a bare URL,
`web_fetch` it before doing anything else -- don't guess at the product from
its name.

### 2. Define the ideal customer profile (ICP)

Use `references/icp-framework.md`. Produce:
- **Primary ICP** -- who benefits most, has the pain acutely, and can plausibly buy or adopt soon
- **Adjacent ICP** -- a secondary profile worth including if primary prospects run thin
- **Disqualifiers** -- traits that make someone a bad fit despite surface similarity (wrong company size, no budget authority, problem already solved internally, etc.)

State this explicitly to the user before researching -- it's the filter
everything downstream depends on, and it's worth a sanity check if the
product description was thin.

### 3. Research public signals

Use `references/signal-types.md` for the five signal categories (demand,
pain, workaround, switching, timing) and where to look for each. Search
broadly, then narrow: forums and communities relevant to the ICP, review
sites (G2/Capterra/TrustRadius-style pages for adjacent or competing tools),
public job postings (a hiring push for a relevant role is a timing signal),
engineering/product blogs, GitHub issues/discussions, conference talk
listings, public social posts, press releases and funding news, and public
RFPs/tenders for B2B or public-sector targets.

Scale search volume to the mode: quick/design-partners need fewer, targeted
searches; deep needs broad coverage across most source types in
signal-types.md. Every candidate prospect needs a specific piece of public
evidence attached before it advances to scoring -- not just "seems like a fit."

### 4. Qualify and score

Use `references/scoring-rubric.md` for the fit score (0-5) and timing score
(0-5) definitions. Score every prospect that survived step 3 with real
evidence. Drop anyone who doesn't clear the disqualifiers from step 2,
regardless of how good the signal looked.

### 5. Draft outreach openers -- draft only, never send

One draft opener per primary prospect, written per
`references/outreach-guidelines.md`: reference the specific public thing
they said or did, keep it short and respectful, no manufactured urgency, no
personal information beyond what's professionally public. These are drafts
for the user to review and send themselves -- this skill never sends a
message, email, or DM on its own, under any mode, regardless of how the
request is phrased.

### 6. Build the report

Assemble the evidence into a JSON structure matching the schema documented
at the top of `scripts/build_report.py`, then run:

```bash
python3 scripts/build_report.py --data prospects.json --out outputs/first-customer-report.html
```

This renders `references/report-template.html` deterministically rather than
hand-writing HTML fresh each time -- keeps formatting consistent and avoids
broken markup on a report the user will actually open and click through.

### 7. State limitations plainly

Every report closes with a limitations section: sample size, how recent the
signals are, which source types you didn't get to (if mode-limited), and the
explicit reminder that these are hypotheses grounded in public signals --
not confirmed customers, and not a guarantee anyone buys.

## Output

```
outputs/first-customer-report.html   -- the polished, standalone report
outputs/first-customer-report.json   -- the underlying evidence data
```

Report contents, in order: early-customer verdict, primary ICP and
disqualifiers, highest-confidence prospect, full evidence-backed shortlist,
fit/timing scores, source links and signal dates, draft outreach openers,
repeated pain patterns (deep mode), a seven-day manual outreach plan, and
research limitations.

## Hard rules

- **Never send outreach automatically.** Drafting an opener is in scope;
  sending an email, DM, or connection request is not -- that stays a
  separate, explicit action the user takes themselves, consistent with
  needing the user's clear go-ahead before anything gets sent on their
  behalf.
- **Never enrich private contact data.** No personal emails, phone numbers,
  home addresses, or anything from a paid enrichment/data-broker service.
  Only use what's already publicly published in a professional context
  (company site, public post, public listing, public filing).
- **Never fabricate a prospect or a signal.** If evidence is thin, exclude
  the prospect rather than padding the count to hit the mode's target
  number. A shortlist of 4 solid prospects beats 10 with 6 weak guesses.
- **Every primary prospect needs a working source link and a signal date.**
  No "someone online said..." without a URL attached.
- **Don't compile sensitive personal data** (health, religion, immigration
  status, etc.) even if it's technically publicly discoverable -- it's
  irrelevant to B2B fit and a needless privacy risk to carry into a report.
- **Prospects are hypotheses, not verified buyers.** Say so in the report;
  don't let scoring language ("qualified," "high-confidence") imply more
  certainty than public signals can support.

## Reference files

- `references/icp-framework.md` -- how to build the primary/adjacent ICP and disqualifiers
- `references/signal-types.md` -- the five signal categories and where to look for each
- `references/scoring-rubric.md` -- fit score and timing score definitions
- `references/outreach-guidelines.md` -- how to draft respectful, source-based openers
- `references/report-template.html` -- the HTML template `scripts/build_report.py` renders into
