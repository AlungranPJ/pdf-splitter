---
name: PDF Splitter
description: Windows 7 Frutiger Aero explorer window floating on a sky, hills and bubbles wallpaper
colors:
  sky-top: "#2a97de"
  sky-mid: "#55b6ee"
  sky-low: "#9bdcf7"
  ink: "#14283c"
  ink-soft: "#46596d"
  glass-edge: "rgba(10,40,70,.6)"
  gel-blue-top: "#5fb0ea"
  gel-blue-bottom: "#1d5fb0"
  gel-green-top: "#69bd45"
  gel-green-bottom: "#237414"
  privacy-bg: "#d9f0c4"
  privacy-ink: "#1d3a12"
  select-glass: "#c4e3fa"
  close-red: "#c73f29"
typography:
  body:
    fontFamily: "Segoe UI, Leelawadee UI, Noto Sans Thai, Tahoma, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.5
  title:
    fontFamily: "Segoe UI, Leelawadee UI, Noto Sans Thai, Tahoma, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 400
rounded:
  window: "9px"
  button: "3px"
  gel-large: "6px"
spacing:
  sm: "8px"
  md: "16px"
components:
  button-primary:
    backgroundColor: "{colors.gel-blue-bottom}"
    textColor: "#ffffff"
    rounded: "{rounded.button}"
    height: "34px"
  button-alt:
    backgroundColor: "{colors.gel-green-bottom}"
    textColor: "#ffffff"
    rounded: "{rounded.button}"
    height: "34px"
  privacy-bar:
    backgroundColor: "{colors.privacy-bg}"
    textColor: "{colors.privacy-ink}"
    padding: "11px 14px"
---

## Overview

A Windows 7 Explorer window on an Aero desktop. The privacy promise is the green Action Center bar, so trust is the first thing a visitor reads. Everything is authored inline (SVG and CSS); no font, image or script is fetched.

## Colors

Sky gradient wallpaper with a sun glow and rays, white clouds, layered green hills, grass blades. The window is translucent blue glass; the client area is white; the command bar is pale blue. Blue gel is the primary action, green gel is the "one file per page" action, red gel exists only on the decorative close button. Secondary text is tinted blue-gray, never neutral gray.

## Typography

Segoe UI with Leelawadee UI for Thai, Tahoma and system fallbacks. One family for everything. Title text carries a white glow so it reads on glass.

## Layout

One centered window, max 1120px. Title bar, address strip (tagline plus language button), then the client area: privacy bar, drop zone, and after loading a two-row sticky command bar over a thumbnail grid. Below 700px the command bar scrolls with the page, and the window nearly fills the screen.

## Elevation & Depth

Glass frame: backdrop blur 16px, inner white hairline, wide soft drop shadow. Buttons: light top half, darker bottom half (the gel split), inset highlight. Hover uses an offset blue shadow, not a zero-offset halo. Thumbnails sit on soft offset shadows.

## Shapes

Small radii (3px buttons, 9px window). Circular blue check badge with a white ring on selected pages. Bubbles are radial-gradient spheres with a rim and inner shadow.

## Components

- Push button: silver gel, blue hover, pressed inset. Disabled is flat gray.
- Gel buttons (`.primary`, `.alt`): 49/51 split gradient, white text with dark text-shadow.
- Thumbnail: transparent by default, light glass on hover, blue glass with badge when selected; keyboard focusable, Space or Enter toggles.
- Privacy bar: green gradient, drawn shield, expandable verify list.
- Drop zone: dashed inner outline, PDF icon, one primary button.

## Do's and Don'ts

- Do keep the CSP closed (`connect-src 'none'`); never add remote fonts or images.
- Do keep copy and privacy verification on the page.
- Do respect `prefers-reduced-motion` (bubbles stop drifting).
- Don't use emoji or text glyphs as icons; draw them.
- Don't use zero-offset colored glows; offset the shadow.
- Don't make the decorative caption buttons interactive.
