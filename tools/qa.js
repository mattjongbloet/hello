// Strict QA for redesign pages: node tools/qa.js page.html [...]
// At 390, 768, 1024 and 1440 wide it checks: console errors, horizontal overflow, elements past the right edge,
// broken images, dead local links, clipped text, overlapping text, low contrast (WCAG AA), fonts that failed to load,
// and small tap targets on phones. Prints one line per problem; exits 1 if any were found.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const WIDTHS = [390, 768, 1024, 1440];
(async () => {
  const pages = process.argv.slice(2);
  const b = await chromium.launch();
  let problems = 0;
  for (const w of WIDTHS) {
    const mobile = w < 500;
    const ctx = await b.newContext({ viewport: { width: w, height: mobile ? 844 : 900 }, isMobile: mobile, hasTouch: mobile });
    for (const f of pages) {
      const p = await ctx.newPage(); const errs = [];
      p.on('pageerror', (e) => errs.push('JS error: ' + e.message));
      p.on('console', (m) => m.type() === 'error' && errs.push('console: ' + m.text()));
      p.on('requestfailed', (r) => errs.push('request failed: ' + r.url().split('/').slice(-2).join('/')));
      await p.goto('file://' + path.resolve(f), { waitUntil: 'networkidle' }).catch((e) => errs.push('load: ' + e.message));
      await p.evaluate(async () => { await document.fonts.ready; for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 40)); } scrollTo(0, 0); });
      await p.waitForTimeout(700);
      const found = await p.evaluate((mobile) => {
        const out = [];
        const vis = (el) => {
          const s = getComputedStyle(el); const r = el.getBoundingClientRect();
          if (s.visibility === 'hidden' || s.display === 'none' || !(r.width > 0 && r.height > 0)) return false;
          for (let a = el; a; a = a.parentElement) if (+getComputedStyle(a).opacity < 0.05) return false;
          return true;
        };
        const inFixed = (el) => { for (let a = el; a; a = a.parentElement) if (getComputedStyle(a).position === 'fixed') return true; return false; };
        const de = document.documentElement;
        if (de.scrollWidth > innerWidth + 1) out.push(`horizontal overflow ${de.scrollWidth - innerWidth}px`);
        const clippedBy = (el) => { for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) { const s = getComputedStyle(a); if (/(hidden|auto|scroll|clip)/.test(s.overflowX)) return a; } return null; };
        const desc = (el) => (el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '') + ' "' + (el.innerText || el.alt || '').trim().slice(0, 30) + '"');
        const all = [...document.querySelectorAll('body *')].filter(vis);
        for (const el of all) {
          const r = el.getBoundingClientRect(), s = getComputedStyle(el);
          if (!inFixed(el) && (r.right > innerWidth + 1 || r.left < -1) && !clippedBy(el)) out.push(`past viewport edge: ${desc(el)} (${Math.round(r.left)}..${Math.round(r.right)})`);
          if (el.tagName === 'IMG' && el.complete && !el.naturalWidth) out.push(`broken image: ${el.getAttribute('src')}`);
          if (/(hidden|clip)/.test(s.overflow) && s.textOverflow !== 'ellipsis' && el.children.length === 0 && el.innerText && el.scrollWidth > el.clientWidth + 1) out.push(`clipped text: ${desc(el)}`);
        }
        // Text leaves for overlap + contrast
        // Text inside a closed <details> isn't rendered, so it can't clip, overlap or fail contrast.
        const hiddenInDetails = (el) => { const d = el.closest('details:not([open])'); return d && !el.closest('summary'); };
        const leaves = all.filter((el) => !hiddenInDetails(el) && [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()));
        const lum = (c) => { const v = c.map((x) => { x /= 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); }); return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; };
        const parse = (c) => {
          const m = c.match(/[\d.]+/g); if (!m) return null; let v = m.map(Number);
          if (c.startsWith('color(srgb')) { v = [v[0] * 255, v[1] * 255, v[2] * 255, v[3]]; } // color-mix() results
          return v;
        };
        const bgOf = (el) => {
          let layers = [];
          for (let a = el; a; a = a.parentElement) {
            const s = getComputedStyle(a);
            if (s.backgroundImage !== 'none' && !/radial-gradient\([^)]*1\.[23]px|repeating-linear-gradient|linear-gradient\(var|linear-gradient\(rgb\(255 240/.test(s.backgroundImage) && !s.backgroundImage.includes('radial-gradient(var(--dots)') && !(a === document.body)) {
              if (/url\(|gradient/.test(s.backgroundImage) && !/1px, transparent 1px/.test(s.backgroundImage)) return null; // image or gradient behind text: can't judge
            }
            const c = parse(s.backgroundColor); if (c && (c[3] === undefined || c[3] > 0)) { layers.push(c); if (c[3] === undefined || c[3] >= 1) break; }
          }
          let base = [255, 255, 255];
          for (const c of layers.reverse()) { const a = c[3] === undefined ? 1 : c[3]; base = base.map((v, i) => v * (1 - a) + c[i] * a); }
          return base;
        };
        for (const el of leaves) {
          const s = getComputedStyle(el); const fg = parse(s.color); if (!fg) continue;
          const bg = bgOf(el); if (!bg) continue;
          const a = fg[3] === undefined ? 1 : fg[3]; const f = fg.slice(0, 3).map((v, i) => v * a + bg[i] * (1 - a));
          const L1 = lum(f), L2 = lum(bg); const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
          const size = parseFloat(s.fontSize), bold = +s.fontWeight >= 700; const large = size >= 24 || (bold && size >= 18.66);
          if (ratio < (large ? 3 : 4.5)) out.push(`contrast ${ratio.toFixed(2)}:1 ${desc(el)}`);
        }
        // Overlapping text boxes (excluding ancestor/descendant pairs and rotated/decorative layers)
        const boxes = leaves.map((el) => {
          const range = document.createRange(); range.selectNodeContents(el);
          return { el, r: [...range.getClientRects()] };
        });
        for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
          const A = boxes[i], B = boxes[j];
          if (A.el.contains(B.el) || B.el.contains(A.el)) continue;
          let hit = false;
          for (const ra of A.r) for (const rb of B.r) {
            const ox = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left), oy = Math.min(ra.bottom, rb.bottom) - Math.max(ra.top, rb.top);
            if (ox > 3 && oy > 3 && ox * oy > 0.3 * Math.min(ra.width * ra.height, rb.width * rb.height)) hit = true; // glyph boxes overhang tight line-heights; require real overlap
          }
          if (hit && !inFixed(A.el) && !inFixed(B.el)) out.push(`overlapping text: ${desc(A.el)} × ${desc(B.el)}`);
        }
        // Wide punctuation: a comma or full stop after a letter rendered wider than ~0.42em (e.g. tabular-nums widening it)
        if (!mobile) {
          const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
          const seen = new Set();
          for (let n; (n = tw.nextNode());) {
            const el = n.parentElement; if (!el || !vis(el)) continue;
            const cs = getComputedStyle(el); if (/mono/i.test(cs.fontFamily)) continue;
            const t = n.textContent; const re = /[A-Za-z][.,](?=\s|$)/g; let m;
            while ((m = re.exec(t))) {
              const r = document.createRange(); r.setStart(n, m.index + 1); r.setEnd(n, m.index + 2);
              const fs = parseFloat(cs.fontSize), ls = parseFloat(cs.letterSpacing) || 0, w = r.getBoundingClientRect().width - ls;
              if (w / fs > 0.42 && !seen.has(el)) { seen.add(el); out.push(`wide punctuation (${(w / fs).toFixed(2)}em): ${desc(el)}`); }
            }
          }
        }
        // Small tap targets on phones
        if (mobile) for (const el of all.filter((e) => e.matches('a, button'))) {
          const r = el.getBoundingClientRect();
          const inline = getComputedStyle(el).display === 'inline' && el.closest('p, li, td, figcaption');
          if (!inline && r.height < 32 && r.width < 400) out.push(`small tap target ${Math.round(r.width)}×${Math.round(r.height)}: ${desc(el)}`);
        }
        // Fonts
        const fams = new Set(); for (const ss of document.styleSheets) { try { for (const r of ss.cssRules) if (r.style && r.style.getPropertyValue) { const v = r.style.getPropertyValue('font-family') || r.style.getPropertyValue('font'); } } catch (e) {} }
        document.fonts.forEach((ff) => { if (ff.status === 'error') out.push('font failed: ' + ff.family); });
        // Local links
        const links = [...document.querySelectorAll('a[href]')].map((a) => a.getAttribute('href')).filter((h) => !/^(https?:|mailto:|tel:|#)/.test(h));
        return { out, links };
      }, mobile);
      for (const l of found.links) { const t = path.resolve(path.dirname(f), l.split('#')[0]); if (!fs.existsSync(t)) found.out.push('dead local link: ' + l); }
      const list = [...new Set([...errs, ...found.out])];
      for (const m of list) console.log(`${w}\t${f}\t${m}`);
      problems += list.length;
      await p.close();
    }
    await ctx.close();
  }
  await b.close();
  console.log(problems ? `\n${problems} problem(s)` : '\nall clear');
  process.exit(problems ? 1 : 0);
})();
