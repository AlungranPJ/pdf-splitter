# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML/CSS/JS in one self-contained file (`template.html` + `vendor/` inlined by `build.py`), deployed to GitHub Pages. No framework, no runtime network.

## Users

General public who need to cut pages out of a PDF right now: students, office workers. They arrive once, do one job, and leave. Thai and English speakers (Thai first).

## Product Purpose

Free PDF page splitter. Pick pages from thumbnails or a range like `1-3, 5, 8-10`, then extract them into one file, split one file per page, or delete pages. Success is a correct PDF downloaded in seconds with zero trust required.

## Positioning

Every byte is processed inside the visitor's own browser. No upload, no server that receives files. A strict Content-Security-Policy makes the browser itself enforce it, and the visitor can verify this in DevTools or by going offline.

## Operating Context

Runs from GitHub Pages or a saved `.html` file, offline-capable. Optional anonymous visit counter (GoatCounter, off unless the maintainer sets `GOATCOUNTER_CODE`); it never sees file names or contents and respects Do Not Track.

## Capabilities and Constraints

- Thumbnails via PDF.js, page assembly via pdf-lib, both inlined.
- Modes: extract selected into one file, one file per page, delete selected.
- Thai and English UI, toggle in the page, `?lang=` override.
- CSP must stay closed: `default-src 'none'`, `connect-src 'none'` (only opened to GoatCounter when the counter is built in). No remote fonts, images, or scripts.
- Privacy statement and its "how to verify" list must stay on the page.
- Not tested: password-protected PDFs, very large files, Firefox/Safari/Edge.

## Brand Commitments

Visual world is pinned by the owner: Windows 7 / Frutiger Aero, full commitment (glass, gel buttons, sky, bubbles, grass). Existing copy, buttons, functions and the privacy box stay.

## Evidence on Hand

Live site: https://alungranpj.github.io/pdf-splitter/ . Repo: https://github.com/AlungranPJ/pdf-splitter . No user counts, testimonials or benchmarks exist; none may be invented.

## Product Principles

1. Trust is the product: the privacy claim is always visible and checkable.
2. One job, no detours: pick pages, get a file.
3. Works the same offline, on a phone, and in Thai or English.
4. Nothing loads from the network that the page does not need.
