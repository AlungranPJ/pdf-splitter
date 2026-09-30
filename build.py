"""Build index.html: inline vendor libs into template.html.

Usage:
  python build.py                          # no tracking at all
  python build.py --goatcounter mysite     # anonymous visit counter via mysite.goatcounter.com
Env: GOATCOUNTER_CODE can be used instead of the flag.
"""
import argparse
import os
import re
from pathlib import Path

REPO_URL = "https://github.com/AlungranPJ/pdf-splitter"

ap = argparse.ArgumentParser()
ap.add_argument("--goatcounter", default=os.environ.get("GOATCOUNTER_CODE", ""))
args = ap.parse_args()
code = args.goatcounter.strip().lower()
if code and not re.fullmatch(r"[a-z0-9-]{2,40}", code):
    raise SystemExit("invalid goatcounter code")

root = Path(__file__).parent
t = (root / "template.html").read_text(encoding="utf-8")
rd = lambda n: (root / "vendor" / n).read_text(encoding="utf-8")

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
if code:
    host = f"https://{code}.goatcounter.com"
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

libs = {"/*PDFLIB*/": rd("pdf-lib.min.js"), "/*PDFJS*/": rd("pdf.min.js"), "/*WORKER*/": rd("pdf.worker.min.js")}
for k, v in libs.items():
    assert "</script" not in v.lower()
    assert k in t, k
# replace small placeholders first, then inline libs (libs may contain comment-like text)
for k, v in {
    "/*CSP*/": csp_str,
    "/*REPO_URL*/": REPO_URL,
    "/*HAS_COUNTER*/": "true" if code else "false",
    "/*COUNTER*/": counter_js,
}.items():
    assert k in t, k
    t = t.replace(k, v)
for k, v in libs.items():
    t = t.replace(k, v)

(root / "index.html").write_text(t, encoding="utf-8")
print("ok index.html", (root / "index.html").stat().st_size, "bytes | counter:", code or "OFF")
print("CSP:", csp_str)
