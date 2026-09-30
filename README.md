# PDF Splitter

**TH:** ตัดหน้า PDF ฟรี ทำงานในเบราว์เซอร์ของคุณทั้งหมด ไฟล์ไม่ถูกอัปโหลดไปไหน
**EN:** Free PDF page splitter. Runs entirely in your browser. Your files are never uploaded.

## Features / ความสามารถ

- Click page thumbnails to select, Shift+click for a range, or type `1-3, 5, 8-10`
- Extract selected pages into one file / split into one file per page / delete selected pages
- Thai and English UI (auto-detected, toggle in the header, or `?lang=en` / `?lang=th`)
- Works offline: save the page as an `.html` file and it still runs

## Privacy / ความเป็นส่วนตัว

- PDF files are read and processed **only inside your browser** (pdf-lib + PDF.js). There is no upload and no server that receives files.
- The page ships a strict `Content-Security-Policy` (`connect-src 'none'`, `default-src 'none'`) so the browser itself blocks the page from sending data anywhere.
- **Visit counter (optional, off by default in the source):** when the maintainer sets the repo variable `GOATCOUNTER_CODE`, the built page loads [GoatCounter](https://www.goatcounter.com/) to count page visits anonymously. It does not use cookies, and it is never given file names or file contents. Nothing is counted if the browser sends Do Not Track. The privacy banner on the page changes to describe exactly this when the counter is on.
- Verify yourself: open DevTools, Network tab, split a file, and check that no request carries your data.

## Build

`index.html` is generated (single self-contained file) from `template.html` + `vendor/`:

```bash
python build.py                       # no tracking code at all
python build.py --goatcounter mysite  # anonymous visit counter (mysite.goatcounter.com)
```

Deployment: GitHub Actions builds and publishes to GitHub Pages on every push to `main` (`.github/workflows/pages.yml`). To turn on the counter, create a GoatCounter site, then set the repository variable `GOATCOUNTER_CODE` to its code and re-run the workflow.

## Third-party

- [pdf-lib](https://github.com/Hopding/pdf-lib) 1.17.1 (MIT)
- [PDF.js](https://github.com/mozilla/pdf.js) 3.11.174 (Apache-2.0)

## License

MIT, see `LICENSE`. Provided as is, without warranty.
