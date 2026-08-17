# HTML → Figma (your own local importer)

Your self-owned version of the "copy a webpage, paste it into Figma" workflow —
no html.to.design, no browser extension, no external service. Two pieces:

1. **`capture.js`** — snapshots the *rendered* page (positions + computed styles) to JSON on your clipboard.
2. **The Figma plugin** (`manifest.json` + `code.js` + `ui.html`) — you paste that JSON and it rebuilds native Figma layers.

---

## One-time setup

### A. Load the Figma plugin (30 seconds)
1. Figma desktop app → menu **Plugins → Development → Import plugin from manifest…**
2. Select `tools/figma-import/manifest.json` in this project.
3. It now lives under **Plugins → Development → "HTML Paste to Figma (local)"**.

### B. Make sure the page is being served
The capture script fetches over http, so open your screens from the local server, e.g.:
```
http://localhost:8642/screens/onboarding.html
```
(If the server isn't running: `python3 -m http.server 8642` from the project root.)

---

## Every time you want to import a screen

### 1. Capture
On the page in your browser, open DevTools console and run:
```js
fetch('/tools/figma-import/capture.js').then(r=>r.text()).then(eval)
```
Then copy what you want:
```js
copyToFigma('.frames')        // the whole grid of screens
copyToFigma('.fw')            // the first labelled screen
copyToFigma($0)               // whatever element is selected in the Elements panel
copyToFigma()                 // the entire <body>
```
It copies a JSON snapshot to your clipboard and logs the size.

> **Tip — capture at full width.** Layout depends on the browser width at capture
> time (the page uses `flex-wrap`). Widen the window first, or capture one screen
> at a time with `copyToFigma('.fw')` / `copyToFigma($0)` for predictable results.

### 2. Paste into Figma
1. Run the plugin (**Plugins → Development → HTML Paste to Figma (local)**).
2. Paste the JSON into the box → **Rebuild in Figma**.
3. It builds the layers to the right of existing content and zooms to them.

---

## What transfers vs. what doesn't

| Transfers | Does NOT transfer |
|---|---|
| Layout & exact positions | **Raster/embedded images** (base64 JPEGs, `<img>`) — those areas come in empty |
| Solid fills + linear gradients | CSS animations, `::before`/`::after` pseudo-content |
| Text, font family/size/weight/color | `background-image` textures other than linear-gradient |
| Border, corner radius, opacity | CSS filters, blend modes |
| Box-shadows (drop & inner) | |

Fonts: the plugin loads the page's font (e.g. Manrope) if Figma has it, else falls back to Inter.

## Optional: bookmarklet
Make a browser bookmark whose URL is the single line in `bookmarklet.txt`.
Click it on any served page to inject the capturer and prompt for a selector.
