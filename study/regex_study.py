"""What the article's email regex actually finds on live pages.

Fetches the homepage and /contact of well-known sites (the audited 300-site frame from
the embedded-JSON study) until 100 pages have answered 200 with HTML. On each page it runs
the article's regex over the raw HTML and classifies every match:

  valid-looking  - plausible mailbox on a plausible domain
  asset          - filename artifacts (logo@2x.png, sprite@3x.webp, name@2x.jpg)
  code           - css/js artifacts (font names, @media fragments glued to identifiers,
                   package@version strings, uuid-ish tokens)
  tracking       - sentry/newrelic-style keys (hex@hex)

It also counts obfuscation signals the regex cannot see: mailto: links whose address is
assembled or encoded, Cloudflare's data-cfemail attribute, and "[at] / (at) / [dot]"
spellings in the visible text. Single stream, small delay. Writes results/regex_study.json.
"""
import json
import pathlib
import re
import sys
import time

import requests

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "python-parse-json" / "verify" / "scripts"))
from sites import SITES

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
S = pathlib.Path(__file__).resolve().parent.parent / "results"
S.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
ARTICLE_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}")

ASSET_EXT = re.compile(r"@\dx\.(png|jpg|jpeg|webp|gif|avif|svg)$", re.I)
HEXY = re.compile(r"^[0-9a-f]{12,}@[0-9a-f]{8,}", re.I)
VERSIONISH = re.compile(r"@\d+(\.\d+){1,3}$")


def classify(match):
    if ASSET_EXT.search(match):
        return "asset"
    if HEXY.match(match):
        return "tracking"
    if VERSIONISH.search(match) or "@media" in match.lower():
        return "code"
    local, _, dom = match.partition("@")
    tld = dom.rsplit(".", 1)[-1].lower()
    if "|" in tld or len(local) > 40 or len(dom) > 40:
        return "code"
    if tld in {"png", "jpg", "jpeg", "webp", "gif", "svg", "css", "js", "woff", "woff2",
               "ttf", "ico", "avif", "mp4", "webm", "json", "xml", "html"}:
        return "asset"
    return "valid-looking"


OBFUSCATION = {
    "cf_email": re.compile(r"data-cfemail=", re.I),
    "at_dot_spelled": re.compile(r"\b[\w.-]{2,30}\s*[\[(]\s*at\s*[\])]\s*[\w.-]{2,30}", re.I),
    "mailto": re.compile(r'href=["\']mailto:', re.I),
}

pages = []
targets = []
for cat, domains in SITES.items():
    for d in domains:
        targets.append((cat, f"https://www.{d}/"))
        targets.append((cat, f"https://www.{d}/contact"))

session = requests.Session()
for cat, url in targets:
    if len(pages) >= 100:
        break
    try:
        r = session.get(url, headers=HEADERS, timeout=12, allow_redirects=True)
    except requests.RequestException:
        continue
    ctype = r.headers.get("content-type", "")
    if r.status_code != 200 or "html" not in ctype:
        continue
    html = r.text
    matches = sorted(set(ARTICLE_RE.findall(html)))
    kinds = {}
    for m in matches:
        kinds.setdefault(classify(m), []).append(m)
    row = dict(category=cat, url=url, final=str(r.url), size=len(html),
               matches=len(matches),
               valid=len(kinds.get("valid-looking", [])),
               asset=len(kinds.get("asset", [])),
               code=len(kinds.get("code", [])),
               tracking=len(kinds.get("tracking", [])),
               samples={k: v[:5] for k, v in kinds.items()},
               obfuscation={k: bool(p.search(html)) for k, p in OBFUSCATION.items()})
    pages.append(row)
    print(f"{len(pages):>3} {url:<44} matches={row['matches']:>3} valid={row['valid']:>2} "
          f"asset={row['asset']:>2} code={row['code']:>2} cf={row['obfuscation']['cf_email']}")
    (S / "regex_study.json").write_text(json.dumps(pages, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    time.sleep(1.0)

tot = dict(pages=len(pages),
           pages_with_any_match=sum(1 for p in pages if p["matches"]),
           pages_with_valid=sum(1 for p in pages if p["valid"]),
           total_matches=sum(p["matches"] for p in pages),
           total_valid=sum(p["valid"] for p in pages),
           total_asset=sum(p["asset"] for p in pages),
           total_code=sum(p["code"] for p in pages),
           total_tracking=sum(p["tracking"] for p in pages),
           pages_cf_email=sum(1 for p in pages if p["obfuscation"]["cf_email"]),
           pages_at_dot=sum(1 for p in pages if p["obfuscation"]["at_dot_spelled"]),
           pages_mailto=sum(1 for p in pages if p["obfuscation"]["mailto"]))
(S / "regex_summary.json").write_text(json.dumps(tot, indent=1), encoding="utf-8")
print(json.dumps(tot, indent=1))
