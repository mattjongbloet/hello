# Portfolio reference canvas

Full-page screenshots of product designer portfolios, laid out on one canvas to compare how each site is structured.

- `canvas.html` — open locally in a browser. One row per page type (Home, Case study, About, Contact, Other), one column per portfolio. Drag to pan, ⌘/ctrl + scroll (or pinch) to zoom, Desktop/Mobile toggle, click a page to enlarge, "live ↗" opens the real page, Portfolios menu or × on a column hides sites.
- `sites.json` — which pages were picked for each portfolio, with notes on why.
- `manifest.json` — every captured page: URL, final URL, size, capture method, errors. (`manifest.js` is the same data for the canvas.)
- `shots/{page_type}/{site}-{width}.png` — full-resolution captures at 1440 and 390 wide; "other" pages are `shots/other/{site}-{n}-{width}.png`. `shots/_web/` holds the downsized JPEGs the canvas displays.

## Re-running

```
node tools/capture.js [site-id ...]   # capture (all sites, or just these; run several in parallel on different ids)
python3 tools/rethumb.py [site-id ...] # regenerate the web-sized JPEGs
node tools/build-canvas.js            # merge shots/_manifest/*.json into manifest.json, rebuild canvas.html + manifest.js
python3 tools/report.py               # list missing, locked and failed pages
```

`sites.json` holds the page picks per portfolio. A page can carry `actions` (clicks/waits before capture, e.g. to open a modal or pass an intro screen), `viewport` (`true` or a list of widths, to capture a fixed window/overlay as one screen), `missing` with a reason, or `same_as` another page type.

Capture: dismisses cookie banners/popups, scrolls slowly to the bottom and back, waits for fonts and images, then takes a full-page shot. Each full-page shot is checked against live viewport shots at 25/50/75% of the page; if it differs (common with smooth-scroll and reveal-on-scroll sites) the page is reloaded and captured as overlapping viewport shots stitched together. Pages are capped at 30,000px tall.
