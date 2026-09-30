"""Build the site from template.html: inline vendor libs, write the CSP, optional visit counter.

Produces self-contained pages plus the SEO files:
  index.html                  hosted page, language auto-detected (optional anonymous counter, "download offline copy" button)
  th/index.html, en/index.html  the same page locked to one language, each with its own title/description/canonical (hreflang pair)
  pdf-splitter-offline.html   the same app with NO counter code, a fully closed CSP (connect-src 'none'),
                              no download button and noindex; this is the file the button hands out
  sitemap.xml, robots.txt     generated for SITE_URL

Usage:
  python build.py                          # no tracking at all (both files identical apart from the button)
  python build.py --goatcounter mysite     # anonymous visit counter via mysite.goatcounter.com (index.html only)
Env: GOATCOUNTER_CODE can be used instead of the flag; SITE_URL overrides the public address (default: GitHub Pages).
"""
import argparse
import datetime
import os
import re
import urllib.parse
from pathlib import Path

import seo

REPO_URL = "https://github.com/AlungranPJ/pdf-splitter"
OFFLINE_NAME = "pdf-splitter-offline.html"
SITE_URL = os.environ.get("SITE_URL", "https://alungranpj.github.io/pdf-splitter/").strip()
if not SITE_URL.endswith("/") or not SITE_URL.startswith("https://"):
    raise SystemExit("SITE_URL must start with https:// and end with /")
# the app icon as a data: URI favicon (the CSP allows img-src data:, so no extra file or request)
FAVICON = ("data:image/svg+xml," + urllib.parse.quote(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs>'
    '<linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#cfe2f4"/></linearGradient>'
    '<linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f08a78"/><stop offset=".5" stop-color="#d23c26"/><stop offset="1" stop-color="#b52a16"/></linearGradient></defs>'
    '<path d="M13 3h28l12 12v46H13z" fill="url(#a)" stroke="#5b7a99" stroke-width="2" stroke-linejoin="round"/>'
    '<path d="M41 3v12h12" fill="#dce9f6" stroke="#5b7a99" stroke-width="2" stroke-linejoin="round"/>'
    '<rect x="5" y="30" width="40" height="19" rx="4" fill="url(#b)" stroke="#7d1b0c" stroke-width="1.5"/>'
    '<text x="25" y="44" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" font-weight="700" fill="#fff">PDF</text></svg>', safe=""))

ap = argparse.ArgumentParser()
ap.add_argument("--goatcounter", default=os.environ.get("GOATCOUNTER_CODE", ""))
args = ap.parse_args()
code = args.goatcounter.strip().lower()
if code and not re.fullmatch(r"[a-z0-9-]{2,40}", code):
    raise SystemExit("invalid goatcounter code")

root = Path(__file__).parent
template = (root / "template.html").read_text(encoding="utf-8")
rd = lambda n: (root / "vendor" / n).read_text(encoding="utf-8")
libs = {"/*PDFLIB*/": rd("pdf-lib.min.js"), "/*PDFJS*/": rd("pdf.min.js"), "/*WORKER*/": rd("pdf.worker.min.js")}
for k, v in libs.items():
    assert "</script" not in v.lower()
    assert k in template, k


def render(counter_code: str, offline: bool, mode: str = "both") -> tuple[str, str]:
    """Return (html, csp) for one variant. mode: 'both' (auto-detect) | 'th' | 'en' (language-locked)."""
    t = template
    depth = "" if mode == "both" else "../"
    t = t.replace("<!--HEADTAGS-->", seo.head_tags(mode, SITE_URL, indexable=not offline, favicon_href=FAVICON))
    t = t.replace("<!--ABOUT-->", seo.noscript_html(mode) + "\n" + seo.about_html(mode, bool(counter_code)))
    t = t.replace("/*HTMLLANG*/", "th" if mode == "both" else mode)
    t = t.replace("/*FIXEDLANG*/", "" if mode == "both" else mode)
    t = t.replace("/*SIBLING*/", {"both": "", "th": "../en/", "en": "../th/"}[mode])
    t = t.replace('href="pdf-splitter-offline.html"', f'href="{depth}pdf-splitter-offline.html"')
    if offline:
        # the offline copy does not offer to download itself
        t, n = re.subn(r"<!--DL-->.*?<!--/DL-->", "", t, flags=re.S)
        assert n == 1, "download button markers not found exactly once"

    # Content-Security-Policy: the browser itself blocks any outbound connection.
    csp = {
        "default-src": "'none'",
        "script-src": "'unsafe-inline'",
        "style-src": "'unsafe-inline'",
        "img-src": "data: blob:",
        "worker-src": "blob:",
        "connect-src": "'none'",
        "font-src": "'none'",
        "form-action": "'none'",
        "base-uri": "'none'",
    }
    counter_js = ""
    if counter_code:
        host = f"https://{counter_code}.goatcounter.com"
        csp["script-src"] += " https://gc.zgo.at"
        csp["connect-src"] = host
        csp["img-src"] += f" {host}"
        counter_js = (
            "if (/^https?:$/.test(location.protocol) && navigator.doNotTrack !== '1' && window.doNotTrack !== '1') {\n"
            "    const s = document.createElement('script');\n"
            f"    s.dataset.goatcounter = '{host}/count';\n"
            "    s.async = true; s.src = 'https://gc.zgo.at/count.js';\n"
            "    document.head.appendChild(s);\n"
            "  }"
        )
    csp_str = "; ".join(f"{k} {v}" for k, v in csp.items())

    # replace small placeholders first, then inline libs (libs may contain comment-like text)
    for k, v in {
        "/*CSP*/": csp_str,
        "/*REPO_URL*/": REPO_URL,
        "/*HAS_COUNTER*/": "true" if counter_code else "false",
        "/*COUNTER*/": counter_js,
    }.items():
        assert k in t, k
        t = t.replace(k, v)
    for k, v in libs.items():
        t = t.replace(k, v)
    return t, csp_str


hosted, hosted_csp = render(code, offline=False)
offline, offline_csp = render("", offline=True)
pages = {m: render(code, offline=False, mode=m)[0] for m in ("th", "en")}

# hard guarantees for the file people download to keep their data private
assert "gc.zgo.at" not in offline and ".goatcounter.com" not in offline, "offline build must not contain counter code"
assert "connect-src 'none'" in offline_csp and "gc.zgo.at" not in offline_csp
assert "HAS_COUNTER = false" in offline
assert 'name="robots" content="noindex"' in offline and "canonical" not in offline
for name, page in [("index", hosted), ("th", pages["th"]), ("en", pages["en"])]:
    for ph in ("/*HTMLLANG*/", "/*FIXEDLANG*/", "/*SIBLING*/", "<!--HEADTAGS-->", "<!--ABOUT-->"):
        assert ph not in page, (name, ph)

(root / "index.html").write_text(hosted, encoding="utf-8")
(root / OFFLINE_NAME).write_text(offline, encoding="utf-8")
for m, page in pages.items():
    (root / m).mkdir(exist_ok=True)
    (root / m / "index.html").write_text(page, encoding="utf-8")

today = datetime.date.today().isoformat()
urls = [SITE_URL, SITE_URL + "th/", SITE_URL + "en/"]
alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE_URL}{l}/"/>' for l in ("th", "en"))
sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')
sm += "".join(f"<url><loc>{u}</loc><lastmod>{today}</lastmod>{alts}</url>\n" for u in urls) + "</urlset>\n"
(root / "sitemap.xml").write_text(sm, encoding="utf-8")
(root / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")

print("ok index.html", (root / "index.html").stat().st_size, "bytes | counter:", code or "OFF")
print("ok th/index.html, en/index.html, sitemap.xml, robots.txt | SITE_URL:", SITE_URL)
print("ok", OFFLINE_NAME, (root / OFFLINE_NAME).stat().st_size, "bytes | counter: OFF | CSP connect-src 'none' | noindex")
print("CSP (hosted):", hosted_csp)
