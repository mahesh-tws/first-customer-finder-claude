# First Customer Finder (for Claude)

A Claude Code / Claude skill that turns a startup URL, repo, or product idea
into a qualified, evidence-backed shortlist of potential first customers --
using only recent **public** signals.

It defines the ideal customer profile, researches public sources via web
search, links every prospect to the specific public evidence behind them,
scores fit and timing, drafts respectful source-based outreach openers, and
builds a polished standalone HTML report. It never sends outreach
automatically, and never touches private contact data or enrichment
services.

This is a port of the workflow from
[Kappaemme-git/codex-first-customer-finder-skill](https://github.com/Kappaemme-git/codex-first-customer-finder-skill)
(built for OpenAI Codex) to Claude's skill format. The research step leans on
Claude's built-in web search and fetch tools directly, rather than custom
scraping infrastructure.

## What it does

- Analyzes a startup URL, repo, or product description
- Defines the primary and adjacent ideal customer profiles, plus disqualifiers
- Finds explicit demand, pain, workaround, switching, and timing signals via public web research
- Qualifies prospects with an evidence-based fit and timing score
- Links every primary prospect to its original public source, with a date
- Drafts respectful, source-based outreach openers -- draft only, never sent
- Builds a responsive, standalone HTML report deterministically (via a script, not hand-rolled HTML each run)
- Keeps all outreach manual by default
- Refuses private contact enrichment and sensitive personal data as a hard rule, not a preference

## Installation

Clone this repo and copy the skill folder into Claude's skills directory:

```bash
git clone https://github.com/<you>/first-customer-finder-claude.git
mkdir -p ~/.claude/skills
cp -R first-customer-finder-claude/first-customer-finder ~/.claude/skills/first-customer-finder
```

Restart Claude Code (or start a new session) after installing.

## Usage

Find the first ten potential customers:

> Use first-customer-finder to find ten evidence-backed potential first
> customers for https://example.com and build the final HTML report.

Find design partners:

> Use first-customer-finder in design-partners mode for this startup: [URL].
> Prioritize people publicly describing the problem who seem likely to give
> product feedback.

B2B research:

> Use first-customer-finder in b2b mode for [URL]. Find public business
> triggers, qualify the relevant companies, and draft one opener per
> prospect without sending anything.

## Modes

- `quick` -- up to 5 strong prospects
- `standard` (default) -- up to 10 prospects across several source types
- `deep` -- up to 20 prospects plus repeated-pattern analysis
- `design-partners` -- feedback-oriented early adopters
- `b2b` -- companies and public business triggers
- `community` -- explicit requests and public discussion signals

## Output

```
outputs/first-customer-report.html   -- the polished, standalone report
outputs/first-customer-report.json   -- the underlying evidence data
```

The report includes: early-customer verdict, primary ICP and disqualifiers,
highest-confidence prospect, evidence-backed shortlist, fit/timing scores,
source links and signal dates, draft outreach openers, repeated pain
patterns (deep mode), a seven-day manual outreach plan, and research
limitations.

Prospects are hypotheses based on public signals, not confirmed customers or
guaranteed buyers.

## Hard rules (not preferences)

- Never sends outreach automatically -- drafting is in scope, sending never is.
- Never enriches private contact data or uses paid data-broker/enrichment services.
- Never fabricates a prospect or a signal to hit a mode's target count.
- Every primary prospect needs a working source link and a signal date.
- Never compiles sensitive personal data (health, religion, immigration
  status, etc.) even if technically discoverable -- irrelevant to B2B fit,
  needless privacy risk.

## Repo layout

```
first-customer-finder/
├── SKILL.md                       # skill definition + workflow
├── scripts/
│   └── build_report.py            # deterministic HTML report renderer
└── references/
    ├── icp-framework.md           # primary/adjacent ICP + disqualifiers
    ├── signal-types.md            # the 5 signal categories + where to look
    ├── scoring-rubric.md          # fit score / timing score definitions
    ├── outreach-guidelines.md     # how to draft respectful openers
    └── report-template.html       # the HTML template build_report.py renders into
```

## License

MIT
