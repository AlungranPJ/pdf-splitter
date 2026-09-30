"""Build the site from template.html: inline vendor libs, write the CSP, optional visit counter.

Produces two self-contained files:
  index.html                  hosted page (optional anonymous counter, has the "download offline copy" button)
  pdf-splitter-offline.html   the same app with NO counter code, a fully closed CSP (connect-src 'none')
                              and no download button; this is the file the button hands out

Usage:
  python build.py                          # no tracking at all (both files identical apart from the button)
  python build.py --goatcounter mysite     # anonymous visit counter via mysite.goatcounter.com (index.html only)
Env: GOATCOUNTER_CODE can be used instead of the flag.
"""
import argparse
import os
import re
from pathlib import Path

REPO_URL = "https://github.com/AlungranPJ/pdf-splitter"
OFFLINE_NAME = "pdf-splitter-offline.html"

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


def render(counter_code: str, offline: bool) -> tuple[str, str]:
    """Return (html, csp) for one variant."""
    t = template
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

# hard guarantees for the file people download to keep their data private
assert "gc.zgo.at" not in offline and ".goatcounter.com" not in offline, "offline build must not contain counter code"
assert "connect-src 'none'" in offline_csp and "gc.zgo.at" not in offline_csp
assert "HAS_COUNTER = false" in offline

(root / "index.html").write_text(hosted, encoding="utf-8")
(root / OFFLINE_NAME).write_text(offline, encoding="utf-8")
print("ok index.html", (root / "index.html").stat().st_size, "bytes | counter:", code or "OFF")
print("ok", OFFLINE_NAME, (root / OFFLINE_NAME).stat().st_size, "bytes | counter: OFF | CSP connect-src 'none'")
print("CSP (hosted):", hosted_csp)
