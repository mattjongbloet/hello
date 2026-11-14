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
| `redesigns/face-lab/` | One page to try nose and mouth ideas on the 3D face (`tools/build-face-lab.py`, `tools/toys/face-lab.js`). Noses: tree, cursor (edit mode), pinecone, tent, trowel. Mouths: coffee beans, bezier curve, hiking trail, colour swatches. Matt's current pick, now on the home page too: **framed art** nose (Matt's "Why?" illustration, `assets/art-why.jpg`; click opens a lightbox) and **half a stroopwafel** mouth (each click takes a bite of its own size and shape where clicked; it regrows as pale dough that browns). The earlier pick (smaller cursor nose + colour-swatch mouth) is still selectable in the lab. |
| `redesigns/index.html` | Overview page listing every direction and demo (built from `tools/directions-a.src.html`). |
| `redesigns/a-clarity/` | Direction A: the base HTML/CSS/JS everything else is generated from. |
| `redesigns/a6-*`, `a7-*`, `a8-*`, `a1`–`a5`, `p-sentence/`, `pmi-formats/`, `cases/`, `archive/` | Earlier iterations and explorations, kept for reference. Not the current direction. |
| `canvas.html`, `manifest.js`, `shots/`, `sites.json` | The reference canvas: screenshots of 36 inspiration portfolios plus Matt's directions. |
| `tools/` | Builders, capture and QA scripts (below). |

## Decisions Matt has made

- **Home page**: A6.1 ("I make complex products feel simple."; "Shaping systems, stories + strategy." was tried as the headline and moved into the intro), with a header and hero modelled on taschiba.com:
  - Header: face, "Matt Jongbloet", "Senior Staff Product Designer" · Work, About, Resume, light/dark toggle. On phones (560px and down) the links sit behind a hamburger button next to the toggle, which opens them as a panel under the header. No "Let's talk" button (removed). No logo in the header (the pencil logo is the favicon).
  - Hero: two-line headline "I make complex products / feel simple." ("feel simple." in the accent), intro (smaller type), then, just below the intro where the buttons were, two soft pills: Dutch flag + "Amsterdam, NL" and "Designing @ [Hospitable logo]" (15 treatments to compare in `redesigns/meta-lab/`, built by `tools/build-meta-lab.py`; Matt chose the soft pills; the others he shortlisted are in the full hero at `redesigns/meta-lab/heroes.html`) (logo links to hospitable.com; its wordmark takes the text colour). The **3D object face** on the right, in a column exactly as tall as the text column (objects' top roughly level with the headline top, hint level with the pills; the stage spills 36px above and 24px below the column so the face is ~17% bigger). No buttons, no impact-stat blocks, no bottom strip. Hint under the face: "Click the record, wheel, artwork or stroopwafel." in Roobert, sentence case. The hero stops short of the first screen so "Selected work" and the top of the first project card peek in from the bottom.
  - Intro copy: "I'm a rigorously curious product designer with 15 years' experience shaping systems, stories and strategy. I'm happiest when people succeed with what I design."
- **Object face** (home page): vinyl record (label "MJ / DNB") + bike wheel (eyes), **framed art** (nose: Matt's "Why?" illustration, no mat board; click opens a lightbox), **half a stroopwafel** (smile; each click takes a bite, it regrows). No eyebrows. Realistic 3D, not flat. Built from `tools/toys/face-lab.js` + eyes from `object-face.js` (`face-home.html/.css`). Sound (Web Audio, starts on click only; on iPhones it plays even with the silent switch on, by Matt's choice, via `Jungle.unmute()` in `tools/toys/jungle.js`): clicking the record toggles the "Stroop" liquid jungle loop; clicking the wheel gives it a push and it ticks like a freewheel as it coasts down; bites crunch. The colour swatches (which set the accent via `--signal` / `--accent-text`) are no longer on the home page, so the accent stays the tan there; the code remains in the lab.
- **Hover cursors** (live on the home page and in the face lab): each object on the face swaps the pointer for a 32px white chip (44px was tried and felt too big) with a line icon: record = play (pause while playing), wheel = spin arrow, framed art = magnifier, stroopwafel = chomper. Desktop only (no hover on touch). Code: `chip()` in `tools/toys/face-lab.js`. How it was chosen: `redesigns/cursor-lab/` (`tools/build-cursor-lab.py`) is a playground with five ideas each for the record, wheel, framed art and stroopwafel, three styles (chip, line, emoji), two modes (replaces the cursor, or a badge beside the hand) and two sizes. The face exposes what is under the pointer as `data-hover` on `.toy-stage` (`music`, `cycle`, `nose`, `mouth`). Matt chose the **chip** style with play/pause (record), spin arrow (wheel) and magnifier (art); he wasn't convinced by the first five stroopwafel icons, so the lab now has twenty for it (he suggested "a smile with teeth"). The cursor lab now shows round 3: five refined, geometry-built line drawings of each chosen icon (play/pause, spin, magnifier, chomper) for Matt to pick from; he picked Outline (play/pause), Arrow round a hub (spin), Plus (magnifier) and Chomper, now live on the home page. He then picked Chomper (13), chip style, large; he did not say replace-or-badge, so it replaces the cursor (the lab default he tested).
- **Record music**: Matt wants the record to play calm, melodic liquid jungle / drum and bass. Ten generated loops (Web Audio, no files; `tools/toys/jungle.js`) are on `redesigns/sound-lab/` (`tools/build-sound-lab.py`) for him to pick from; Matt picked **Stroop** (164 BPM, C major, sparse break, warm keys), which the record now plays on the home page and in the face lab. The loops were checked by offline render for level and balance only; nobody has listened to them yet. A real licensed track from Matt would sound better and can replace this.
- **3D realism** (Matt wants the objects as realistic as possible): the record's surface shows the music (four tracks of differing tone, broad loud/quiet bands and fine streaks that vary round the disc, glassy gaps, a run-out spiral, dust and a few hairline scratches, all in colour and roughness maps) and it has a slight warp, so you can see it turning by more than the label; it sits on a strobe-dotted platter with a Technics SL-1210 style S-shaped tonearm (gimbal, counterweight, angled headshell, finger lift); the wheel is modelled on a DT Swiss GRC 1100 (deep carbon rim with decals, 24 straight-pull spokes that turn a little lighter in dark mode, hub, disc rotor) with a slim tan-wall gravel tyre and chunky tread knobs on the outer edge only (the black shoulder is smooth). The record label reads "MJ / DNB". In the lab the eyes and stroopwafel are scaled down so the larger frame leads. Both live in `tools/toys/object-face.js`. In the lab, the framed art has a moulded frame and glass (no mat board; Matt asked for it removed, and for the frame to be a little larger next to the eyes); the stroopwafel is two wafers (pale crumb inside, baked faces, uneven browning, fine pressed lattice, hand-cut wobbly outline) with a glossy caramel layer that squeezes out past the rim; it is built from 31 stacked alpha-cut layers and sits nearly front-on: flat while the pointer is on it, with only a slight lean otherwise, so the wafer / caramel / wafer edge is just glimpsed as the face moves (Matt found a stronger tilt too dramatic). Bites are each a different size and scalloped shape, cut through all three layers, and drop crumbs; after ~2.2s they knit back from the tooth marks inward over ~2.8s, arriving as pale dough that browns over ~2.6s. Five synthesised bite sounds (never the same twice running). All are modelled in code; true photorealism would need scanned/modelled GLB assets or baked renders.
- **Accent colour**: the tan of the gravel tyre's sidewall, `#b28550` (set in `tools/site_parts.py`; a deeper `--signal-ink` for small text, lighter tans in dark mode). The record label, hub band, headline accent and page accents all use it. The earlier orange `#ff5a1f` remains only in older explorations.
- **Typeface**: Roobert only, everywhere (including small labels; no monospace). Apercu, GT Eesti, Geograph, Styrene and serifs were tried and rejected.
- **Case-study format**: opening = title, intro, facts row (company, role, team, date), cover image, metric tiles (except Trellis, where Matt removed them; tiles were briefly removed everywhere and restored at his request); body = contents menu on the left with Context → Opportunity → Approach → Outcome; "Next project" at the end.
  **Animated covers** (Matt's plan: every case study's cover becomes a 3–8s loop showing what was done). First one: Trellis, `tools/anims/trellis.html` (HTML/CSS/JS, no video), inserted by `build-case-studies.py`: Savvy mobile homepage → tap Start saving → vehicle (2022 Honda Civic) → own/rent → monthly premium ($250) → "Shopping 40+ insurers" → "You could save an average of $1,500/year" (the homepage's own claim) with five insurer offers (Progressive $118 "Best offer", Allstate $131, Liberty Mutual $139, Travelers $142, Farmers $149 a month: **illustrative prices** Matt asked for, chosen so the best saves ~$1,580/yr against the $250 entered). Insurer logos are cut from Savvy's own archived homepage graphic (`assets/trellis/ins-*.png`); the homepage cards keep "$$/mo" as the real site did. Rebuilt from Matt's screens (Wayback homepage + flow PNG). Uses Savvy's real logo mark (Matt's SVG) and Montserrat (Savvy's typeface, from Google Fonts): regular and semibold, with the screen titles and headlines in bold (Matt asked). The phone is a CSS iPhone (titanium band with faked thickness, bezel, Dynamic Island, side keys, glass glare, home bar) shown front on (Matt didn't want it tilted) with a gentle float; an iOS keyboard (letters or number pad, keys light up as characters land) slides up while typing; the loading screen pops in the five insurer logos; the best offer glows once. Loops about every 8.9s, pauses off screen, shows the final frame for reduced motion. Matt has not supplied a real result screen; the premium was changed from the mock-up's $150 to $250 so the savings add up.
  Matt likes putting the cover image first, above the headline (reference: a Fin Studio case study). Three options on PMI are in `redesigns/cs-cover-lab/` (`tools/build-cs-cover-lab.py`): 1 image first, same layout; 2 framed stage, centred title; 3 full-bleed cover, split title. No pick yet.
- **Project cards** (home): white card with the screenshot on top edge to edge, the logo tile straddling the image's bottom edge, then company, **bold** title and one line. All cards are half-width, two per row (no wide cards). Fifteen variations of this card (light theme first) are in `redesigns/card-lab/` (`tools/build-card-lab.py`); Matt picked 4 (image on top, logo overlapping), now on the home page; 5 (compact header) and 13 (no card) were also shortlisted (`redesigns/card-lab/home.html`).
- **Recent roles** (home): rows with a company logo, role, company and dates, condensed (no description), separated by white space only (no rule lines); the resume link under it is a bold text link (a primary button was tried and dropped). Matt's pick from round 2 of the roles lab. History: 15 variations with company logos are in `redesigns/roles-lab/` (`tools/build-roles-lab.py`); Matt preferred rows with logos, one line each, one card, two-by-two cards and the timeline, and wants cards outlined (not grey-filled) and more condensed; `roles-lab/round-2.html` has 15 refinements of those. No final pick yet. Logo tiles: `assets/hospitable-mark.svg` (made from the Hospitable logo's mark), Homebot and Savvy PNGs, `assets/carv-logo.svg` (from the SVG Matt uploaded). Variations are shown in the real half-column About layout. LinkedIn could not be scraped (login wall; we never sign in).
- **Case-study team**: Trellis's Team fact is three 44px round headshots (Drew Bolles, Chuong Nguyen, Alexey Komissarouk; photos from Matt in `assets/team/<linkedin-handle>.jpg`), each linking to their LinkedIn, names only in the link label and tooltip (Matt asked to drop the visible names and the engineering note). `team()` in `build-case-studies.py`; it falls back to initials when no photo exists.
- **Type size**: headings and body ~10–15% smaller than Direction A (`tools/type-smaller.css`).
- Dark mode exists behind the toggle; the site opens in light mode.

## Build

Everything under `redesigns/site/` and `redesigns/case-studies/` is generated. Edit the builders, then run in this order:

```
python3 tools/build-a-cv.py          # A-family iterations incl. site/ (home, about) from a-clarity + CV copy
python3 tools/build-hero-toys.py     # adds the 3D object face to site/ (and the standalone demos)
python3 tools/build-case-studies.py  # all case studies
python3 tools/build-face-lab.py      # face lab
python3 tools/build-card-lab.py      # 15 variations of the project card
python3 tools/build-roles-lab.py     # 15 variations of the Recent roles list
python3 tools/build-cs-cover-lab.py  # 3 image-first openings for the case studies (reads case-studies/pmi.html)
python3 tools/build-cursor-lab.py    # hover-cursor playground (uses site/toy.js)
python3 tools/build-sound-lab.py     # 10 generated liquid jungle loops to audition
python3 tools/build-meta-lab.py      # 15 treatments of the location/role items (reads the built home page)
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
- Matt's title: Senior Staff Product Designer at Hospitable (shown in full in the header). "15 years' experience" is his wording.
- Dates: Trellis Jan 2023 – Jan 2024 and Homebot Dec 2020 – Dec 2022 follow the CV. Hospitable shows "Now" (start month unconfirmed).

## Open items

- The 3D face has no keyboard or screen-reader way to open the artwork or take a bite yet (pointer only).
- Trellis case study: story reframed by Matt (no designer for two years; ~15 experiments across homepage, linked and unlinked flows; one worked example, the unlinked re-order test; no experiment log). Approach opens with Matt's note that he no longer has access to the other experiments, so this is one example of the 15. The control and V2 flows are shown as nine rounded screens on a tinted stage (`tflow()`, screens cut into `assets/trellis/screens/`), scrolling sideways on phones; the two charts sit in padded white frames. Still needed: full-resolution before/after homepage images (his uploads were 89px and 194px wide; the Wayback Machine blocks automated browsers, so we don't capture it), whether V2 shipped, how the $3.5MM was predicted.
- Carv and Hospitable case studies need content from Matt.

- Internal Admin is dated January 2020 on the live site, before the CV's Homebot start (Dec 2020): confirm.
- Hospitable start month.
- Live site issues found: contact links on case-study pages point to a template email and phone number.

## Publishing

Two private Claude artifacts are kept in sync with the repo:
- Overview: https://claude.ai/artifact/J5V6wpaD8o5bLZHaUKoEQt — root `redesigns/`, page `redesigns/index.html`.
- Canvas: https://claude.ai/artifact/GR5an3NddvLwwnYeHKLSmQ — near its 511-file cap; remove unused files when adding.

Work happens on branch `claude/portfolio-reference-canvas-fhglla`.
