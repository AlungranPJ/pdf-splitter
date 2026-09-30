"""Static, crawler-visible copy for the hosted pages: meta tags, JSON-LD, the "about" section.

Everything here is plain HTML/text that exists before any JavaScript runs, so search engines and link
previews see real content instead of an empty app shell. Claims are limited to what the tool does and
what has been tested; there are no made-up ratings, user counts or awards.
"""
import html
import json

META = {
    "th": {
        "title": "ตัดหน้า PDF ฟรี ไม่อัปโหลดไฟล์ ใช้ออฟไลน์ได้ | PDF Splitter",
        "description": "เครื่องมือตัดหน้า PDF ฟรี ดึงหน้าที่ต้องการเป็นไฟล์ใหม่ แยกทีละหน้า หรือลบหน้าทิ้ง ทำงานในเบราว์เซอร์ของคุณ ไฟล์ไม่ถูกอัปโหลดไปไหน มีไฟล์ดาวน์โหลดไปใช้ออฟไลน์",
        "og_alt": "PDF Splitter: ตัดหน้า PDF ในเบราว์เซอร์ ไฟล์ไม่ออกจากเครื่อง",
        "locale": "th_TH",
        "noscript": "เครื่องมือนี้ต้องเปิด JavaScript ในเบราว์เซอร์ถึงจะตัดหน้า PDF ได้ ไฟล์ของคุณยังอยู่ในเครื่องเท่านั้น",
    },
    "en": {
        "title": "Split PDF Pages Free: Private, in Your Browser, Works Offline | PDF Splitter",
        "description": "Free PDF splitter that runs in your browser. Extract pages into a new file, split one page per file, or delete pages. Your PDF is never uploaded. Offline copy available.",
        "og_alt": "PDF Splitter: split PDF pages in your browser, files never leave your device",
        "locale": "en_US",
        "noscript": "This tool needs JavaScript to split PDF pages. Your files still never leave your device.",
    },
}

GITHUB = "https://github.com/AlungranPJ/pdf-splitter"


def _about_th(counter: bool) -> str:
    q2 = (
        "ไม่เก็บ ไฟล์ถูกอ่านและตัดในเบราว์เซอร์ของคุณเท่านั้น หน้าเว็บนับเฉพาะจำนวนผู้เข้าชมแบบไม่ระบุตัวตน (GoatCounter ไม่ใช้ cookie) "
        "และไม่เคยได้รับชื่อหรือเนื้อหาไฟล์"
        if counter else
        "ไม่เก็บ ไฟล์ถูกอ่านและตัดในเบราว์เซอร์ของคุณเท่านั้น และหน้านี้ไม่มีโค้ดติดตามใด ๆ"
    )
    offline_li = (
        "<li>ต้องการให้ข้อมูลรั่วไม่ได้เลย: กดปุ่มดาวน์โหลดไปใช้ออฟไลน์ที่มุมซ้ายล่าง ไฟล์นั้นไม่มีตัวนับผู้เข้าชมและปิดการเชื่อมต่อเน็ตทุกชนิด</li>"
        if counter else ""
    )
    return f"""
<h2>ตัดหน้า PDF ฟรี ไม่ต้องอัปโหลดไฟล์</h2>
<p>PDF Splitter เป็นเครื่องมือตัดหน้า PDF ที่ทำงานในเบราว์เซอร์ของคุณทั้งหมด เลือกหน้าที่ต้องการแล้วดึงออกเป็นไฟล์ใหม่ แยกทีละหน้า หรือลบหน้าที่ไม่ต้องการ โดยไฟล์ไม่ถูกส่งออกจากเครื่อง ใช้ฟรี ไม่ต้องสมัครสมาชิก ไม่มีลายน้ำ</p>
<h3>วิธีตัดหน้า PDF</h3>
<ol>
<li>วางไฟล์ PDF ลงในหน้านี้ หรือกดเลือกไฟล์จากเครื่อง</li>
<li>คลิกภาพย่อของหน้าที่ต้องการ กด Shift ค้างเพื่อเลือกเป็นช่วง หรือพิมพ์ช่วงหน้า เช่น <code>2-4, 7</code> ในช่องระบุหน้า</li>
<li>เลือกว่าจะรวมหน้าที่เลือกเป็น 1 ไฟล์ แยกทีละหน้า (ได้หลายไฟล์) หรือลบหน้าที่เลือกทิ้ง ไฟล์จะดาวน์โหลดทันที</li>
</ol>
<h3>ปลอดภัยแค่ไหน</h3>
<ul>
<li>ทุกอย่างประมวลผลในเครื่องของคุณ ไม่มีเซิร์ฟเวอร์รับไฟล์</li>
<li>ตรวจเองได้: เปิด DevTools แท็บ Network แล้วลองตัดไฟล์ จะไม่เห็น request ที่ส่งไฟล์ออก</li>
{offline_li}
<li>โค้ดทั้งหมดเปิดเผยบน <a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a> (สัญญาอนุญาต MIT)</li>
</ul>
<h3>คำถามที่พบบ่อย</h3>
<details><summary>ใช้ฟรีจริงไหม</summary><p>ฟรี ไม่ต้องสมัครสมาชิก ไม่มีลายน้ำ และโค้ดเป็นโอเพนซอร์สสัญญาอนุญาต MIT</p></details>
<details><summary>เว็บนี้เก็บไฟล์ PDF ของฉันไหม</summary><p>{q2}</p></details>
<details><summary>ใช้ตอนไม่มีอินเทอร์เน็ตได้ไหม</summary><p>ได้ โหลดไฟล์เวอร์ชันออฟไลน์ไปเก็บไว้ แล้วเปิดด้วยการดับเบิลคลิก ไม่ต้องติดตั้งโปรแกรม</p></details>
<details><summary>ใช้บนมือถือได้ไหม</summary><p>ได้ หน้าจอปรับให้พอดีกับมือถือ</p></details>
""".strip()


def _about_en(counter: bool) -> str:
    q2 = (
        "No. Your file is read and split inside your browser only. The page counts visits anonymously (GoatCounter, no cookies) "
        "and never receives file names or contents."
        if counter else
        "No. Your file is read and split inside your browser only, and this page contains no tracking code."
    )
    offline_li = (
        "<li>Want zero chance of a leak: press the download button at the bottom-left for an offline copy. It has no visit counter and blocks every network connection.</li>"
        if counter else ""
    )
    return f"""
<h2>Split PDF pages for free, without uploading anything</h2>
<p>PDF Splitter runs entirely in your browser. Pick the pages you want and extract them into a new file, split the document one page per file, or delete the pages you don't need. Your file never leaves your device. It is free, needs no account and adds no watermark.</p>
<h3>How to split a PDF</h3>
<ol>
<li>Drop a PDF onto this page, or choose a file from your device.</li>
<li>Click the page thumbnails you want, hold Shift to select a range, or type page ranges such as <code>2-4, 7</code> in the range box.</li>
<li>Choose to merge the selected pages into one file, split them one page per file (several files), or delete the selected pages. The download starts right away.</li>
</ol>
<h3>How private is it</h3>
<ul>
<li>Everything is processed on your device. There is no server that receives files.</li>
<li>You can check it yourself: open DevTools, go to the Network tab and split a file. No request carries your file out.</li>
{offline_li}
<li>All code is public on <a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a> under the MIT license.</li>
</ul>
<h3>FAQ</h3>
<details><summary>Is it really free?</summary><p>Yes. No account, no watermark, and the code is open source under the MIT license.</p></details>
<details><summary>Does this site keep my PDF?</summary><p>{q2}</p></details>
<details><summary>Does it work offline?</summary><p>Yes. Download the offline copy, keep it on your computer and open it with a double click. Nothing to install.</p></details>
<details><summary>Does it work on a phone?</summary><p>Yes, the layout adapts to phone screens.</p></details>
""".strip()


def about_block(lang: str, counter: bool, hidden: bool = False) -> str:
    body = _about_th(counter) if lang == "th" else _about_en(counter)
    h = " hidden" if hidden else ""
    return f'<section class="about" data-about="{lang}" lang="{lang}"{h}>\n{body}\n</section>'


def about_html(mode: str, counter: bool) -> str:
    """mode: 'th' | 'en' (language-locked page, one block) or 'both' (auto-detect page, both blocks, JS picks one)."""
    if mode in ("th", "en"):
        return about_block(mode, counter)
    return about_block("th", counter) + "\n" + about_block("en", counter, hidden=True)


def noscript_html(mode: str) -> str:
    if mode in ("th", "en"):
        return f'<noscript><p class="nojs">{html.escape(META[mode]["noscript"])}</p></noscript>'
    return ('<noscript><p class="nojs">' + html.escape(META["th"]["noscript"]) + '<br><span lang="en">'
            + html.escape(META["en"]["noscript"]) + '</span></p></noscript>')


def head_tags(mode: str, site: str, indexable: bool, favicon_href: str) -> str:
    """mode: 'th' | 'en' | 'both'. site ends with '/'. indexable=False -> noindex (offline copy)."""
    lang = "th" if mode == "both" else mode
    m = META[lang]
    e = html.escape
    out = [f"<title>{e(m['title'])}</title>",
           f'<meta name="description" content="{e(m["description"], quote=True)}">',
           f'<link rel="icon" type="image/svg+xml" href="{e(favicon_href)}">']
    if not indexable:
        out.append('<meta name="robots" content="noindex">')
        return "\n".join(out)
    url = {"both": site, "th": site + "th/", "en": site + "en/"}[mode]
    out += [
        f'<link rel="canonical" href="{url}">',
        f'<link rel="alternate" hreflang="th" href="{site}th/">',
        f'<link rel="alternate" hreflang="en" href="{site}en/">',
        f'<link rel="alternate" hreflang="x-default" href="{site}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="PDF Splitter">',
        f'<meta property="og:title" content="{e(m["title"], quote=True)}">',
        f'<meta property="og:description" content="{e(m["description"], quote=True)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:locale" content="{m["locale"]}">',
        f'<meta property="og:image" content="{site}og-{lang}.png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{e(m["og_alt"], quote=True)}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{e(m["title"], quote=True)}">',
        f'<meta name="twitter:description" content="{e(m["description"], quote=True)}">',
        f'<meta name="twitter:image" content="{site}og-{lang}.png">',
    ]
    ld = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "PDF Splitter",
        "url": url,
        "description": m["description"],
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Any (web browser)",
        "browserRequirements": "Requires JavaScript",
        "inLanguage": ["th", "en"],
        "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "license": GITHUB + "/blob/main/LICENSE",
        "sameAs": [GITHUB],
    }
    out.append('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>")
    return "\n".join(out)
