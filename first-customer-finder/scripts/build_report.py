#!/usr/bin/env python3
"""
Renders the first-customer-finder evidence data into the standalone HTML
report template. Rendering is done with plain string substitution here --
deliberately, so the report's formatting is deterministic and doesn't drift
between runs the way hand-written HTML would.

Expected JSON schema (--data):

{
  "title": "Acme Inc.",
  "mode": "standard",
  "verdict": "One or two sentence early-customer verdict.",
  "primary_icp": "Description of the primary ICP.",
  "adjacent_icp": "Description of the adjacent ICP.",
  "disqualifiers": "Comma or sentence-separated list of disqualifying traits.",
  "top_prospect": {
    "name": "Jane Doe",
    "org": "Example Corp",
    "fit_score": 5,
    "timing_score": 4,
    "evidence": [
      {"text": "Posted about X breaking down", "url": "https://...", "date": "2026-06-01"}
    ],
    "opener": "Draft outreach message text..."
  },
  "prospects": [ /* same shape as top_prospect, one entry per shortlisted prospect */ ],
  "patterns": ["Pattern description 1", "Pattern description 2"],
  "outreach_plan": ["Day 1: ...", "Day 2: ...", "..."],
  "limitations": "Plain statement of sample size, recency, and gaps."
}

Usage:
    python3 build_report.py --data prospects.json --out outputs/first-customer-report.html \\
        --template ../references/report-template.html
"""
import argparse
import html
import json
from datetime import date


def esc(value):
    return html.escape(str(value)) if value is not None else ""


def score_class(score, kind):
    try:
        s = float(score)
    except (TypeError, ValueError):
        return ""
    if s >= 4:
        return f"{kind}-high"
    if s >= 2:
        return f"{kind}-mid"
    return ""


def render_evidence(evidence_list):
    if not evidence_list:
        return "<li><em>No evidence attached -- this prospect should not have made the shortlist.</em></li>"
    items = []
    for ev in evidence_list:
        text = esc(ev.get("text", ""))
        url = ev.get("url", "")
        date_str = esc(ev.get("date", "undated"))
        if url:
            link = f'<a href="{esc(url)}" target="_blank" rel="noopener">source</a>'
        else:
            link = "<em>no link provided</em>"
        items.append(f"<li>{text} &mdash; {link} ({date_str})</li>")
    return "\n".join(items)


def render_prospect_card(p, heading_tag="h3"):
    name = esc(p.get("name", "Unnamed prospect"))
    org = esc(p.get("org", ""))
    fit = p.get("fit_score", "?")
    timing = p.get("timing_score", "?")
    fit_class = score_class(fit, "fit")
    timing_class = score_class(timing, "timing")
    evidence_html = render_evidence(p.get("evidence", []))
    opener = esc(p.get("opener", "")).strip()
    opener_html = f'<div class="opener">{opener}</div>' if opener else ""
    org_line = f" &middot; {org}" if org else ""

    return f"""<div class="card">
  <{heading_tag}>{name}{org_line}</{heading_tag}>
  <div class="score-pair">
    <span class="score {fit_class}">Fit {fit}/5</span>
    <span class="score {timing_class}">Timing {timing}/5</span>
  </div>
  <ul class="evidence-list">
{evidence_html}
  </ul>
  {opener_html}
</div>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True, help="Path to the evidence JSON file (see schema in this file's docstring)")
    ap.add_argument(
        "--template",
        default="references/report-template.html",
        help="Path to the HTML template (default: references/report-template.html relative to cwd)",
    )
    ap.add_argument("--out", required=True, help="Path to write the rendered HTML report")
    args = ap.parse_args()

    with open(args.data) as f:
        data = json.load(f)

    with open(args.template) as f:
        template = f.read()

    top_prospect = data.get("top_prospect")
    top_card = render_prospect_card(top_prospect) if top_prospect else "<p><em>No prospect cleared the highest-confidence bar this run.</em></p>"

    prospects = data.get("prospects", [])
    prospect_cards = "\n".join(render_prospect_card(p) for p in prospects) if prospects else "<p><em>No prospects met the shortlist threshold.</em></p>"

    patterns = data.get("patterns", [])
    pattern_list = (
        "<ul>" + "".join(f"<li>{esc(p)}</li>" for p in patterns) + "</ul>"
        if patterns
        else "<p><em>Not enough prospects to identify repeated patterns (deep mode surfaces these more reliably).</em></p>"
    )

    plan = data.get("outreach_plan", [])
    plan_items = "\n".join(f"<li>{esc(step)}</li>" for step in plan) if plan else "<li><em>No plan generated.</em></li>"

    filled = template
    replacements = {
        "{{TITLE}}": esc(data.get("title", "Untitled")),
        "{{MODE}}": esc(data.get("mode", "standard")),
        "{{GENERATED_DATE}}": date.today().isoformat(),
        "{{VERDICT}}": esc(data.get("verdict", "")),
        "{{PRIMARY_ICP}}": esc(data.get("primary_icp", "")),
        "{{ADJACENT_ICP}}": esc(data.get("adjacent_icp", "")),
        "{{DISQUALIFIERS}}": esc(data.get("disqualifiers", "")),
        "{{TOP_PROSPECT_CARD}}": top_card,
        "{{PROSPECT_CARDS}}": prospect_cards,
        "{{PATTERN_LIST}}": pattern_list,
        "{{OUTREACH_PLAN_ITEMS}}": plan_items,
        "{{LIMITATIONS}}": esc(data.get("limitations", "")),
    }
    for token, value in replacements.items():
        filled = filled.replace(token, value)

    with open(args.out, "w") as f:
        f.write(filled)

    print(f"Wrote report to {args.out}")


if __name__ == "__main__":
    main()
