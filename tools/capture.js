// Capture full-page screenshots for every page listed in sites.json.
//
//   node tools/capture.js                 # all sites
//   node tools/capture.js ericsin foo     # only these site ids
//
// Writes shots/{page_type}/{site}-{width}.png (other pages: shots/other/{site}-{n}-{width}.png),
// web-sized copies under shots/_web/, and merges results into manifest.json.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SHOTS = path.join(ROOT, 'shots');
const TMP = path.join(SHOTS, '_frames', String(process.pid));
const MAX_H = 30000; // safety cap on captured page height (px)

const WIDTHS = {
  1440: { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 },
  390: {
    viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1',
  },
};

const COOKIE_SELECTORS = [
  '#onetrust-accept-btn-handler', '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll',
  '.cky-btn-accept', '.cc-allow', '.cc-dismiss', '[data-cookiebanner="accept_button"]',
  '#truste-consent-button', '.fc-cta-consent', 'button[aria-label*="accept" i]',
];
const DISMISS_TEXT = /^(accept( all)?( cookies)?|allow( all)?|agree|i agree|got it|ok(ay)?|close|dismiss|no thanks|continue|×|✕)$/i;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function dismissPopups(page) {
  for (const sel of COOKIE_SELECTORS) {
    const el = page.locator(sel).first();
    if (await el.isVisible().catch(() => false)) await el.click({ timeout: 2000 }).catch(() => {});
  }
  // Buttons with dismiss-like text inside something that looks like a banner / modal.
  await page.evaluate((src) => {
    const re = new RegExp(src, 'i');
    const containers = [...document.querySelectorAll('div,section,aside,dialog,[role=dialog]')].filter((el) => {
      const s = getComputedStyle(el);
      const t = (el.innerText || '').toLowerCase();
      return (s.position === 'fixed' || s.position === 'sticky' || el.getAttribute('role') === 'dialog')
        && /cookie|consent|privacy|newsletter|subscribe/.test(t) && t.length < 1500;
    });
    for (const c of containers) {
      const btn = [...c.querySelectorAll('button,a,[role=button]')].find((b) => re.test((b.innerText || b.getAttribute('aria-label') || '').trim()));
      if (btn) btn.click(); else c.remove();
    }
  }, DISMISS_TEXT.source).catch(() => {});
  // Escape only when a modal is open, and undo it if it navigated (some sites bind Escape to "Back").
  const modal = await page.locator('[role=dialog]:visible, [aria-modal=true]:visible').count().catch(() => 0);
  if (modal) {
    const before = page.url();
    await page.keyboard.press('Escape').catch(() => {});
    await sleep(500);
    if (page.url() !== before) await page.goto(before, { waitUntil: 'domcontentloaded' }).catch(() => {});
  }
}

// Find how the page scrolls: native window, an inner overflow container, or a transformed smooth-scroll wrapper.
async function scrollModel(page) {
  return page.evaluate(() => {
    const doc = document.scrollingElement || document.documentElement;
    const vh = innerHeight;
    // Trust window scrolling only if it actually moves.
    const y0 = scrollY; scrollTo(0, y0 + 50); const windowScrolls = scrollY !== y0; scrollTo(0, y0);
    if (doc.scrollHeight > vh * 1.15 && windowScrolls) return { kind: 'window', height: doc.scrollHeight };
    let best = null;
    for (const el of [document.body, ...document.querySelectorAll('body *')]) {
      const s = getComputedStyle(el);
      if (/(auto|scroll)/.test(s.overflowY) && el.scrollHeight > el.clientHeight + 50 && el.clientHeight > vh * 0.7) {
        if (!best || el.scrollHeight > best.scrollHeight) best = el;
      }
    }
    if (best) { best.setAttribute('data-cap-scroller', '1'); return { kind: 'inner', height: best.scrollHeight }; }
    // Transform-driven smooth scroll (e.g. locomotive): tall wrapper inside a viewport-high body.
    let tall = null;
    for (const el of document.querySelectorAll('[data-scroll-container],main,body > div,#__next > div,#root > div')) {
      const h = el.scrollHeight;
      if (h > vh * 1.5 && (!tall || h > tall.scrollHeight)) tall = el;
    }
    if (tall) { tall.setAttribute('data-cap-scroller', 'transform'); return { kind: 'transform', height: tall.scrollHeight }; }
    return { kind: 'window', height: doc.scrollHeight };
  });
}

async function slowScroll(page, model) {
  const vh = page.viewportSize().height;
  let last = -1, still = 0;
  for (let i = 0; i < 120; i++) {
    await page.mouse.wheel(0, Math.round(vh * 0.6));
    await sleep(220);
    const pos = await page.evaluate((k) => {
      if (k === 'inner') { const e = document.querySelector('[data-cap-scroller]'); return e ? e.scrollTop + e.clientHeight >= e.scrollHeight - 2 ? -2 : e.scrollTop : 0; }
      const d = document.scrollingElement || document.documentElement;
      return scrollY + innerHeight >= d.scrollHeight - 2 ? -2 : scrollY;
    }, model.kind);
    if (pos === -2) break;
    if (pos === last) { if (++still > 6) break; } else still = 0;
    last = pos;
  }
  await sleep(800);
  // Back to the top, in steps so scroll-linked animations settle.
  for (let i = 0; i < 40; i++) {
    await page.mouse.wheel(0, -vh * 2);
    await sleep(60);
  }
  await page.evaluate(() => {
    scrollTo(0, 0);
    const e = document.querySelector('[data-cap-scroller="1"]'); if (e) e.scrollTop = 0;
  });
  await sleep(1000);
}

async function settle(page) {
  await page.evaluate(() => document.querySelectorAll('img[loading="lazy"]').forEach((i) => { i.loading = 'eager'; })).catch(() => {});
  await page.waitForLoadState('networkidle', { timeout: 8000 }).catch(() => {});
  await page.evaluate(async () => {
    await document.fonts.ready;
    const imgs = [...document.images].filter((i) => !i.complete);
    await Promise.race([Promise.all(imgs.map((i) => new Promise((r) => { i.onload = i.onerror = r; }))), new Promise((r) => setTimeout(r, 6000))]);
  }).catch(() => {});
  await sleep(500);
}

function py(args) {
  return execFileSync('python3', ['-I', path.join(__dirname, 'img.py'), ...args], { encoding: 'utf8' }).trim();
}

// Tag fixed "chrome" (small fixed bars) as top- or bottom-anchored so we can control where it appears.
async function tagFixedChrome(page) {
  return page.evaluate(() => {
    const vh = innerHeight; let n = 0;
    for (const el of document.querySelectorAll('body *')) {
      const s = getComputedStyle(el);
      if (s.position !== 'fixed' && s.position !== 'sticky') continue;
      const r = el.getBoundingClientRect();
      // Sticky elements count as chrome only when they're a full-width bar pinned at the top (site headers).
      if (s.position === 'sticky' && !(/^(HEADER|NAV)$/.test(el.tagName) || (r.top + scrollY <= 5 && r.width >= innerWidth * 0.8 && r.height < 200))) continue;
      if (!r.width || !r.height || r.height > vh * 0.4) continue; // keep full-screen backgrounds
      if (el.parentElement && el.parentElement.closest('[data-cap-fixed]')) continue;
      el.setAttribute('data-cap-fixed', r.top + r.height / 2 < vh / 2 ? 'top' : 'bottom'); n++;
    }
    return n;
  });
}
const showFixed = (page, which) => page.evaluate((which) => {
  for (const el of document.querySelectorAll('[data-cap-fixed]')) {
    if (which.includes(el.getAttribute('data-cap-fixed'))) el.style.removeProperty('visibility');
    else el.style.setProperty('visibility', 'hidden', 'important');
  }
}, which);

async function waitViewportImages(page) {
  await page.evaluate(async () => {
    const imgs = [...document.images].filter((i) => { const r = i.getBoundingClientRect(); return !i.complete && r.bottom > 0 && r.top < innerHeight; });
    await Promise.race([Promise.all(imgs.map((i) => new Promise((r) => { i.onload = i.onerror = r; }))), new Promise((r) => setTimeout(r, 3000))]);
  }).catch(() => {});
}

// Viewport screenshots while scrolling, then stitched (for pages where fullPage capture breaks).
// Top-anchored fixed bars show only in the first frame, bottom-anchored ones only in the last.
async function stitchCapture(page, model, out) {
  const vh = page.viewportSize().height;
  const dir = fs.mkdtempSync(path.join(TMP, 'f-'));
  const frames = [];
  await tagFixedChrome(page);
  const height = () => page.evaluate((k) => {
    const e = document.querySelector('[data-cap-scroller]');
    if (k === 'inner' && e) return e.scrollHeight;
    if (k === 'transform' && e) return e.scrollHeight;
    return (document.scrollingElement || document.documentElement).scrollHeight;
  }, model.kind);
  const scrollTo = (y) => page.evaluate(([k, y]) => {
    if (k === 'inner') { const e = document.querySelector('[data-cap-scroller]'); e.scrollTop = y; return e.scrollTop; }
    document.documentElement.style.scrollBehavior = 'auto';
    window.scrollTo({ top: y, behavior: 'instant' }); return null;
  }, [model.kind, y]);
  const readWindowY = () => page.evaluate(() => Math.round(scrollY));
  let y = 0, prevOffset = -1, total = model.height;
  for (let i = 0; i < Math.ceil((2 * MAX_H) / vh) + 2; i++) { // half-viewport steps
    let actual = await scrollTo(y);
    if (model.kind === 'transform') {
      // Drive the smooth-scroll library with the wheel and read back the wrapper's translateY.
      if (i) await page.mouse.wheel(0, Math.round(vh / 2));
      await sleep(1000);
      actual = await page.evaluate(() => {
        const e = document.querySelector('[data-cap-scroller]');
        const m = new DOMMatrixReadOnly(getComputedStyle(e).transform);
        return Math.round(-m.m42 + scrollY);
      });
    } else {
      await sleep(900);
      if (model.kind === 'window') actual = await readWindowY();
    }
    await waitViewportImages(page);
    if (actual === prevOffset) break;
    total = Math.min(Math.max(total, await height()), MAX_H);
    const last = actual + vh >= total - 2;
    await showFixed(page, [i === 0 ? 'top' : '', last ? 'bottom' : '']);
    await sleep(100);
    const f = path.join(dir, `${String(i).padStart(3, '0')}.png`);
    await page.screenshot({ path: f });
    frames.push(`${f}:${actual}`);
    prevOffset = actual;
    if (last) break;
    // Half-viewport steps: each region is finally pasted from a frame where it sits in the top half,
    // i.e. after it has already been on screen long enough for reveal-on-scroll animations to finish.
    y = actual + Math.round(vh / 2);
  }
  await showFixed(page, ['top', 'bottom']);
  py(['stitch', out, String(page.viewportSize().width), String(total), ...frames]);
  fs.rmSync(dir, { recursive: true, force: true });
}

// For full-page shots: move bottom-anchored fixed bars to the end of the document
// (where a visitor sees them at the end of the scroll) instead of over mid-page content.
async function relocateBottomFixed(page) {
  await tagFixedChrome(page);
  await page.evaluate(() => {
    const vh = innerHeight, docH = (document.scrollingElement || document.documentElement).scrollHeight;
    for (const el of document.querySelectorAll('[data-cap-fixed="bottom"]')) {
      const r = el.getBoundingClientRect();
      el.dataset.capStyle = el.getAttribute('style') || '';
      el.style.setProperty('position', 'absolute', 'important');
      el.style.setProperty('top', '0px', 'important'); el.style.setProperty('left', '0px', 'important');
      el.style.setProperty('bottom', 'auto', 'important'); el.style.setProperty('right', 'auto', 'important');
      el.style.setProperty('width', r.width + 'px', 'important');
      const r2 = el.getBoundingClientRect();
      el.style.setProperty('top', (docH - (vh - r.top) - (r2.top + scrollY)) + 'px', 'important');
      el.style.setProperty('left', (r.left - r2.left) + 'px', 'important');
    }
  });
}
const restoreBottomFixed = (page) => page.evaluate(() => {
  for (const el of document.querySelectorAll('[data-cap-fixed="bottom"]')) el.setAttribute('style', el.dataset.capStyle || '');
});

// Compare the full-page shot against live viewport shots at a few scroll positions.
async function fullPageLooksBroken(page, out, height) {
  const vh = page.viewportSize().height;
  if (height <= vh * 1.2) return 0;
  const dir = fs.mkdtempSync(path.join(TMP, 'v-'));
  let worst = 0;
  for (const frac of [0.25, 0.5, 0.75]) {
    const target = Math.round((height - vh) * frac);
    const actual = await page.evaluate((y) => { scrollTo(0, y); return Math.round(scrollY); }, target);
    await sleep(1200);
    await waitViewportImages(page);
    const f = path.join(dir, `s${frac}.png`);
    await page.screenshot({ path: f });
    worst = Math.max(worst, Number(py(['compare', out, f, String(actual)])));
  }
  await page.evaluate(() => scrollTo(0, 0)); await sleep(600);
  fs.rmSync(dir, { recursive: true, force: true });
  return worst;
}

async function capturePage(ctx, spec, out, width) {
  const rec = { url: spec.url };
  let page;
  // Load, run any page actions, dismiss popups, slow-scroll to trigger lazy content, wait for fonts/images.
  const prepare = async () => {
    if (page) await page.close();
    page = await ctx.newPage();
    const resp = await page.goto(spec.url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    rec.status = resp ? resp.status() : null;
    await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
    await sleep(1200);
    for (const a of spec.actions || []) {
      // Actions (e.g. an intro gate) may already be gone on a repeat visit in the same context.
      if (a.click) await page.locator(a.click).filter({ visible: true }).first().click({ timeout: 8000 }).catch(() => {});
      await sleep(a.wait || 2000);
    }
    await dismissPopups(page);
    rec.final_url = page.url();
    rec.title = await page.title();
    rec.password_screen = await page.locator('input[type=password]').count() > 0;
    if (rec.status && rec.status >= 400) throw new Error(`HTTP ${rec.status}`);
    let model = await scrollModel(page);
    await slowScroll(page, model);
    await dismissPopups(page);
    await settle(page);
    return scrollModel(page);
  };
  try {
    let model = await prepare();
    rec.scroll = model.kind;
    let method = 'fullpage';
    // viewport: true for every width, or a list of widths (e.g. ["390"]) for fixed overlays that don't scroll with the page.
    const viewportOnly = spec.viewport === true || (Array.isArray(spec.viewport) && spec.viewport.includes(String(width)));
    if (viewportOnly) {
      method = 'viewport';
      await page.evaluate(() => scrollTo(0, 0)); await sleep(500);
      await page.screenshot({ path: out });
    } else if (model.kind === 'window' && model.height <= MAX_H) {
      await relocateBottomFixed(page);
      await page.screenshot({ path: out, fullPage: true, timeout: 90000 });
      await restoreBottomFixed(page);
      const [, h] = py(['size', out]).split(' ').map(Number);
      // vh-based sections can balloon during full-page capture; fall back to stitching if so.
      if (h > model.height * 1.3 + 200) { method = 'stitched'; rec.fallback_reason = 'full-page height ballooned'; }
      else {
        const diff = await fullPageLooksBroken(page, out, h);
        rec.fullpage_diff = Number(diff.toFixed(3));
        if (diff > 0.15) { method = 'stitched'; rec.fallback_reason = 'full-page shot differed from live viewport'; }
      }
      // The full-page attempt can leave the page in a bad state (reset reveal animations), so start fresh.
      if (method === 'stitched') model = await prepare();
    } else method = 'stitched';
    if (method === 'stitched') await stitchCapture(page, model, out);

    rec.method = method;
    if (model.height > MAX_H) rec.truncated_at = MAX_H;
    const [w, h] = py(['size', out]).split(' ').map(Number);
    rec.width = w; rec.height = h;
  } catch (e) {
    rec.error = e.message.split('\n')[0];
  }
  if (page) await page.close();
  return rec;
}

(async () => {
  const sites = JSON.parse(fs.readFileSync(path.join(ROOT, 'sites.json'), 'utf8'));
  const only = process.argv.slice(2);
  fs.mkdirSync(TMP, { recursive: true });
  const browser = await chromium.launch();

  for (const site of sites) {
    if (only.length && !only.includes(site.id)) continue;
    console.log(`\n# ${site.id}`);
    const entry = { id: site.id, name: site.name, input: site.input, pages: {} };
    // Page list: [type, key, spec, index]
    const jobs = [];
    for (const t of ['home', 'case', 'about', 'contact']) jobs.push([t, t, site[t] || { missing: 'none found' }]);
    (site.other || []).forEach((o, i) => jobs.push(['other', `other-${i + 1}`, o, i + 1]));

    const ctxs = {};
    for (const w of Object.keys(WIDTHS)) ctxs[w] = await browser.newContext({ ...WIDTHS[w], ignoreHTTPSErrors: false });

    for (const [type, key, spec, n] of jobs) {
      const rec = { type, label: spec.label || null, url: spec.url || null, note: spec.note || null };
      if (spec.missing) { rec.missing = spec.missing; entry.pages[key] = rec; console.log(`  ${key}: ${spec.missing}`); continue; }
      if (spec.same_as) { rec.same_as = spec.same_as; entry.pages[key] = rec; console.log(`  ${key}: same as ${spec.same_as}`); continue; }
      rec.shots = {};
      for (const w of Object.keys(WIDTHS)) {
        const name = n ? `${site.id}-${n}-${w}` : `${site.id}-${w}`;
        const rel = `shots/${type}/${name}.png`;
        fs.mkdirSync(path.join(SHOTS, type), { recursive: true });
        const r = await capturePage(ctxs[w], spec, path.join(ROOT, rel), w);
        if (!r.error) {
          const web = `shots/_web/${type}/${name}.jpg`;
          fs.mkdirSync(path.join(SHOTS, '_web', type), { recursive: true });
          const [tw, th] = py(['thumb', path.join(ROOT, rel), path.join(ROOT, web), w === '1440' ? '640' : '390']).split(' ').map(Number);
          Object.assign(r, { file: rel, web, web_width: tw, web_height: th });
        }
        rec.shots[w] = r;
        rec.final_url = rec.final_url || r.final_url;
        // A password field on a short page is a password screen; long pages may just carry a hidden form.
        if (r.password_screen && type === 'case' && r.height && r.height < 2.2 * (w === '1440' ? 900 : 844)) rec.locked = true;
        console.log(`  ${key} @${w}: ${r.error ? 'FAILED ' + r.error : `${r.method} ${r.width}x${r.height} (${r.scroll})`}`);
      }
      if (Object.values(rec.shots).every((s) => s.error)) rec.failed = Object.values(rec.shots)[0].error;
      entry.pages[key] = rec;
    }
    for (const c of Object.values(ctxs)) await c.close();
    entry.captured_at = new Date().toISOString();
    fs.mkdirSync(path.join(SHOTS, '_manifest'), { recursive: true });
    fs.writeFileSync(path.join(SHOTS, '_manifest', `${site.id}.json`), JSON.stringify(entry, null, 2));
  }
  await browser.close();
  // Run tools/build-canvas.js afterwards to merge shots/_manifest/*.json into manifest.json.
})();
