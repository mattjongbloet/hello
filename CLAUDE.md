# Matt Jongbloet — portfolio redesign

Redesign of mjongbloet.com for Matt Jongbloet, Senior Staff Product Designer at Hospitable (Amsterdam).
This file records the decisions made so far and how the project is built, so a new session can pick up without the history.

## Where things are

| Path | What |
|---|---|
| `redesigns/site/` | **The current site**: `index.html` (home), `about.html`. Generated; do not edit by hand. |
| `redesigns/case-studies/` | **All case studies** in the chosen format. Generated. |
| `redesigns/assets/` | Images: covers, logos, `cases/` (process images, video stills), `trellis/` (crops from Matt's deck), `mj-logo.svg`. |
| `redesigns/fonts/` | `fonts.css` plus Roobert `.woff2` files. The `.woff2` files are **git-ignored** (trial licence, public repo); pages fall back to Hanken Grotesk without them. |
| `redesigns/face-lab/` | One page to try nose and mouth ideas on the 3D face (`tools/build-face-lab.py`, `tools/toys/face-lab.js`). Noses: tree, cursor (edit mode), pinecone, tent, trowel. Mouths: coffee beans, bezier curve, hiking trail, colour swatches. Matt is trying the smaller cursor nose with the colour-swatch mouth (the lab opens on that pair); a swatch click also recolours the record label and wheel reflector. Not yet on the home page. |
| `redesigns/index.html` | Overview page listing every direction and demo (built from `tools/directions-a.src.html`). |
| `redesigns/a-clarity/` | Direction A: the base HTML/CSS/JS everything else is generated from. |
| `redesigns/a6-*`, `a7-*`, `a8-*`, `a1`–`a5`, `p-sentence/`, `pmi-formats/`, `cases/`, `archive/` | Earlier iterations and explorations, kept for reference. Not the current direction. |
| `canvas.html`, `manifest.js`, `shots/`, `sites.json` | The reference canvas: screenshots of 36 inspiration portfolios plus Matt's directions. |
| `tools/` | Builders, capture and QA scripts (below). |

## Decisions Matt has made

- **Home page**: A6.1 ("I make complex products feel simple."), with a header and hero modelled on taschiba.com:
  - Header: face, "Matt Jongbloet", "Product Designer" · Work, About, Resume, light/dark toggle, "Let's talk". No logo in the header (the pencil logo is the favicon).
  - Hero: headline + intro (smaller type), the **3D object face** on the right, and one line underneath: "Amsterdam, Netherlands · Currently Senior Staff Product Designer at Hospitable". No impact-stat blocks. The hero must fit the first screen on a laptop.
  - Intro copy: "I'm a rigorously curious product designer with 15 years' experience helping people and businesses shine. I'm happiest when people succeed with what I design."
- **Object face**: vinyl record + bike wheel (eyes), tree (nose, he likes exploring the woods), smile = coffee beans as a **stand-in** (undecided; options offered: hammock, chocolate bar, open book, festoon lights). No eyebrows. Realistic 3D, not flat.
- **Typeface**: Roobert only, everywhere (including small labels; no monospace). Apercu, GT Eesti, Geograph, Styrene and serifs were tried and rejected.
- **Case-study format**: opening = title, intro, facts row (company, role, team, date), cover image, metric tiles; body = contents menu on the left with Context → Opportunity → Approach → Outcome; "Next project" at the end.
- **Project cards** (home): his current site's style — white card, logo tile, company, title, one line, screenshot bleeding off the bottom-right.
- **Type size**: headings and body ~10–15% smaller than Direction A (`tools/type-smaller.css`).
- Dark mode exists behind the toggle; the site opens in light mode.

## Build

Everything under `redesigns/site/` and `redesigns/case-studies/` is generated. Edit the builders, then run in this order:

```
python3 tools/build-a-cv.py          # A-family iterations incl. site/ (home, about) from a-clarity + CV copy
python3 tools/build-hero-toys.py     # adds the 3D object face to site/ (and the standalone demos)
python3 tools/build-case-studies.py  # all case studies
node tools/build-canvas.js           # overview page (redesigns/index.html) + canvas
```

- `tools/site_parts.py` — shared header, theme toggle, dark CSS.
- `tools/toys/` — 3D pieces (three.js r160 from jsDelivr, classic script so `file://` works): `three-common.js`, `object-face.*`, `untangle.*`.
- `tools/build-case-studies.py` — one content block per case study. Seven come from mjongbloet.com (text tightened, facts kept), Trellis from Matt's deck; `carv` and `hospitable` are templates with highlighted placeholders and are not linked from the home page.
- Other builders (`build-a-variants.py`, `build-p.py`, `build-cases.py`, `build-pmi-formats.py`) produce the older explorations; `build-case-studies.py` imports pieces from the last two.

## Checks before committing

```
node tools/qa.js <pages…>      # 390/768/1024/1440: console errors, overflow, broken images, dead links, clipped/overlapping text, contrast, tap targets
node tools/shoot.js <outdir> <pages…>   # full-page screenshots at 1440 and 390
```

Run QA on every changed page; it should print `all clear`. For dark mode, QA a temporary copy with the theme forced to dark. Look at screenshots before calling something done.

## Content rules

- Never invent facts, numbers or claims. Copy comes from mjongbloet.com, Matt's 2024 CV and what he says in chat.
- Label estimates as estimates (e.g. PMI "≈$200M a month in estimated savings"; Trellis "$3.5MM in **predicted gross annual revenue**").
- Matt's title: Senior Staff Product Designer at Hospitable (header shows "Product Designer"). "15 years' experience" is his wording.
- Dates: Trellis Jan 2023 – Jan 2024 and Homebot Dec 2020 – Dec 2022 follow the CV. Hospitable shows "Now" (start month unconfirmed).

## Open items

- Smile object for the 3D face; whether the tree should be more realistic (would need modelled assets).
- Trellis case study placeholders: what "unlinked application" means, 4–6 more experiments, whether V2 shipped, how the $3.5MM was predicted.
- Carv and Hospitable case studies need content from Matt.
- Internal Admin is dated January 2020 on the live site, before the CV's Homebot start (Dec 2020): confirm.
- Hospitable start month.
- Phone header hides Work/About/Resume (no menu yet). Hero still has "See my work" / "More about me" buttons (the reference has none).
- Live site issues found: contact links on case-study pages point to a template email and phone number.

## Publishing

Two private Claude artifacts are kept in sync with the repo:
- Overview: https://claude.ai/artifact/J5V6wpaD8o5bLZHaUKoEQt — root `redesigns/`, page `redesigns/index.html`.
- Canvas: https://claude.ai/artifact/GR5an3NddvLwwnYeHKLSmQ — near its 511-file cap; remove unused files when adding.

Work happens on branch `claude/portfolio-reference-canvas-fhglla`.
