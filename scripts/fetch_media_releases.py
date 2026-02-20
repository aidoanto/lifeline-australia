#!/usr/bin/env python3
"""Fetch Lifeline media release pages and output <150 char summaries."""
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

BASE = "https://lla-drupal-app-prod.lifeline.org.au"
PATHS = """
/about/news-and-media/10-jun-2020-nrma-insurance-and-racv-provide-2m-funding-boost-for-lifeline
/about/news-and-media/13yarn-marks-50000-calls
/about/news-and-media/13yarn-welcomes-federal-funding-to-expand-culturally-safe-crisis-support-for
/about/news-and-media/6-increase-in-lives-lost-to-suicide-demands-more-funding-urgently-to-reduce
/about/news-and-media/agreement-of-lifeline-australia-and-on-the-line-australia-to-provide-better
/about/news-and-media/australia-unites-to-help-lifeline-deliver-crisis-support-to-communities
/about/news-and-media/australians-reaching-out-for-help-in-record-numbers
/about/news-and-media/beyond-now-app-goes-to-lifeline-to-streamline-support
/about/news-and-media/cost-of-living-pressures
/about/news-and-media/cost-of-living-pressures-trigger-record-demand-for-lifelines-resources
/about/news-and-media/covid-19-impact-activates-first-national-emergency-appeal-in-lifelines-57-year
/about/news-and-media/extreme-weather-events
/about/news-and-media/how-lifeline-can-help-if-you-are-struggling-with-distressing-current-events
/about/news-and-media/in-lead-up-to-world-suicide-prevention-day-and-ruok-day-australians-reach-out
/about/news-and-media/john-brogden-charmain-lifeline-australia-and-northern-beaches-resident-reminds
/about/news-and-media/landmark-amalgamation-paves-way-for-better-support-for-help-seekers-across
/about/news-and-media/lifeline-adds-bondi-centre-to-national-network
/about/news-and-media/lifeline-and-beyond-blue-partnership-announcement
/about/news-and-media/lifeline-and-rebel-launch-a-game-changing-partnership
/about/news-and-media/lifeline-and-the-centre-of-best-practice-in-aboriginal-and-torres-strait
/about/news-and-media/lifeline-australia-honours-the-remarkable-dedication-and-impact-of-its
/about/news-and-media/lifeline-australia-is-encouraged-by-the-victorian-coroners-findings-the-rate
/about/news-and-media/lifeline-australia-spreads-hope-through-new-podcast-series
/about/news-and-media/lifeline-australia-welcomes-federal-funding-to-continue-dv-alert-program
/about/news-and-media/lifeline-australia-welcomes-her-excellency-the-honourable-ms-sam-mostyn-ac-as
/about/news-and-media/lifeline-australia-welcomes-victorian-governments-funding-to-provide-crisis
/about/news-and-media/lifeline-celebrates-volunteers
/about/news-and-media/lifeline-connect-offers-in-person-support-across-northern-sydney-libraries
/about/news-and-media/lifeline-hacks-tech-to-remind-australians-to-check-in-this-christmas
/about/news-and-media/lifeline-is-here-247-during-extended-nsw-lockdown
/about/news-and-media/lifeline-is-here-for-you-this-holiday-season
/about/news-and-media/lifeline-is-here-for-you-throughout-the-holiday-season
/about/news-and-media/lifeline-is-here-to-provide-connection-and-support-over-busive-festive-season
/about/news-and-media/lifeline-is-there-for-victorians-247-as-calls-from-victoria-spike-22-in-second
/about/news-and-media/lifeline-reminds-australians-that-suicide-doesnt-discriminate
/about/news-and-media/lifeline-to-launch-dedicated-bushfire-response-phoneline
/about/news-and-media/lifeline-urges-australians-to-get-to-know-all-the-ways-to-reach-out-for
/about/news-and-media/lifeline-welcomes-additional-state-government-funding-to-support-the-nsw
/about/news-and-media/lifeline-welcomes-federal-government-appointment-of-australias-first-deputy
/about/news-and-media/lifeline-welcomes-federal-government-funding-to-safeguard-the-wellbeing-of
/about/news-and-media/lifeline-welcomes-introduction-of-suicide-monitoring-system-across-nsw
/about/news-and-media/lifeline-welcomes-new-mental-health-support-package-for-nsw
/about/news-and-media/lifeline-welcomes-the-appointment-of-an-assistant-minister-to-the-prime
/about/news-and-media/lifeline-welcomes-the-national-suicide-and-self-harm-monitoring-system-website
/about/news-and-media/lifelines-new-24-7-crisis-text-service-opens-up-crisis-support-to-hard-to
/about/news-and-media/more-australians-than-ever-seeking-crisis-support
/about/news-and-media/national-sporting-organisations-commit-to-landmark-trans-and-gender-diverse
/about/news-and-media/new-one-of-a-kind-aboriginal-and-torres-strait-islander-helpline-up-and
/about/news-and-media/new-partnership-to-help-meet-record-mental-health-demand
/about/news-and-media/new-position-piece-reveals-the-concerning-silent-challenge-of-older-men-in
/about/news-and-media/new-toolkit-empowers-help-seekers-to-access-support-on-their-own-terms
/about/news-and-media/newly-refurbished-geelong-lifeline-centre-is-now-australias-largest
/about/news-and-media/nib-supports-lifeline-australia-to-meet-increased-demand-for-mental-health
/about/news-and-media/prince-william-handpicks-lifeline-australia-for-donation
/about/news-and-media/suicides-drop-in-new-south-wales-by-5-during-the-pandemic
/about/news-and-media/sydney-local-named-volunteer-of-the-year
/about/news-and-media/this-world-suicide-prevention-day-lifeline-will-call-on-australians-to-send
/about/news-and-media/unique-aboriginal-and-torres-strait-islander-helpline-officially-launched-in
/about/news-and-media/victorian-government-contributes-funding-to-ensure-lifeline-continues
""".strip().splitlines()

# Fix typo in path
PATHS = [p.replace("busive-festive", "busy-festive") for p in PATHS if p.strip()]


class TitleAndLeadParser(HTMLParser):
    """Capture page title and first substantial paragraph for summary."""
    def __init__(self):
        super().__init__()
        self.title = None
        self.in_title = False
        self.in_h1 = False
        self.in_lead = False
        self.lead_parts = []
        self.in_main = False
        self.tag_stack = []
        self.seen_first_p_after_h1 = False
        self.after_h1 = False

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.in_h1 = True
        if tag == "p" and self.after_h1 and not self.seen_first_p_after_h1:
            self.in_lead = True
            self.seen_first_p_after_h1 = True
        attrs_d = dict(attrs)
        if tag == "main" or (tag == "div" and attrs_d.get("class", "").find("content") >= 0):
            self.in_main = True

    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        if tag == "title":
            self.in_title = False
        if tag == "h1":
            self.in_h1 = False
        if tag == "h1":
            self.after_h1 = True
        if tag == "p":
            self.in_lead = False

    def handle_data(self, data):
        s = data.strip()
        if not s:
            return
        if self.in_title and self.title is None:
            self.title = s.split("|")[0].strip()
        if self.in_h1 and self.title is None:
            self.title = s
        if self.in_lead:
            self.lead_parts.append(s)


def fetch_page(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; Lifeline)"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="replace")


GENERIC_DESC = "Lifeline is a national charity providing all Australians with 24 hour crisis support and suicide prevention services."


def extract_summary(html: str, max_len: int = 150) -> tuple[str, str]:
    """Return (title, summary) with summary at most max_len chars."""
    title = None
    # Title from <title> (strip " | Lifeline")
    t = re.search(r"<title>([^<]+)</title>", html)
    if t:
        title = t.group(1).split("|")[0].strip()
    if not title:
        title = "Media release"
    # Prefer meta description when it's specific (not the generic site description)
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    if m:
        raw = m.group(1).replace("&#039;", "'").strip()
        if raw != GENERIC_DESC and len(raw) > 20:
            summary = raw
            if len(summary) > max_len:
                summary = summary[: max_len - 3].rsplit(" ", 1)[0] + "..."
            return title, summary
    # Otherwise derive a unique summary from the title and first substantive <p>
    # Skip boilerplate that appears in global page chunks (e.g. "Help starts here")
    skip_phrases = (
        GENERIC_DESC,
        "Support looks different for everyone",
        "Lifeline is Australia's leading suicide prevention service",
        "How can we help?",
    )
    for m in re.finditer(r"<p>([^<]+)</p>", html):
        lead = m.group(1).replace("&#039;", "'").replace("&amp;", "&").replace("\u00a0", " ").strip()
        if len(lead) > 50 and not any(s in lead for s in skip_phrases):
            summary = lead.split(".")[0].strip() + ("." if "." in lead else "")
            if len(summary) > max_len:
                summary = summary[: max_len - 3].rsplit(" ", 1)[0] + "..."
            return title, summary
    # Fallback: turn title into a sentence (capitalise first letter)
    summary = (title[0].lower() + title[1:]) if len(title) > 1 else title
    if not summary.endswith("."):
        summary += "."
    if len(summary) > max_len:
        summary = summary[: max_len - 3].rsplit(" ", 1)[0] + "..."
    summary = summary[0].upper() + summary[1:] if len(summary) > 1 else summary
    return title, summary


def main():
    out_path = Path(__file__).resolve().parent.parent / "docs" / "media-releases-summary.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Lifeline News & Media – page summaries",
        "",
        "Short summary for each media release (each under 150 characters).",
        "",
        "Source: [News & Media](https://lla-drupal-app-prod.lifeline.org.au/about/news-and-media)",
        "",
        "---",
        "",
    ]
    for path in PATHS:
        path = path.strip()
        if not path:
            continue
        url = BASE + path
        try:
            html = fetch_page(url)
            title, summary = extract_summary(html)
            title = title.replace("&#039;", "'").replace("&amp;", "&")
            summary = summary.replace("&nbsp;", " ").replace("&#039;", "'")
            lines.append(f"## {title}")
            lines.append("")
            lines.append(f"**Summary:** {summary}")
            lines.append("")
            lines.append(f"*[Read more]({url})*")
            lines.append("")
        except Exception as e:
            lines.append(f"## {path.split('/')[-1]}")
            lines.append("")
            lines.append(f"**Summary:** (could not fetch: {e})")
            lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
