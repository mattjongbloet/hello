// Usage: node tools/discover.js out.json url1 url2 ...
// For each URL: final URL, title, password field, and links (text, href, zone, y) — written as JSON.
const { chromium } = require('playwright');
const fs = require('fs');
async function probe(ctx, url) {
  const page = await ctx.newPage();
  try {
    const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
    await page.waitForTimeout(1500);
    for (let i = 0; i < 8; i++) { await page.mouse.wheel(0, 1200); await page.waitForTimeout(150); }
    const info = await page.evaluate(() => {
      const links = []; const seen = new Set();
      for (const a of document.querySelectorAll('a[href]')) {
        const href = a.href.split('#')[0] || a.href;
        const text = (a.innerText || a.getAttribute('aria-label') || a.title || '').trim().replace(/\s+/g, ' ').slice(0, 70);
        const k = href + '|' + text; if (seen.has(k)) continue; seen.add(k);
        const r = a.getBoundingClientRect();
        links.push({ text, href, zone: a.closest('nav,header') ? 'nav' : a.closest('footer') ? 'foot' : 'body', y: Math.round(r.top + scrollY) });
      }
      return { title: document.title, final: location.href, pw: !!document.querySelector('input[type=password]'), h: document.documentElement.scrollHeight, text: document.body.innerText.slice(0, 400).replace(/\s+/g, ' '), links };
    });
    info.status = resp && resp.status();
    return info;
  } catch (e) { return { error: e.message.split('\n')[0] }; } finally { await page.close(); }
}
(async () => {
  const [out, ...urls] = process.argv.slice(2);
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const res = {}; let i = 0;
  await Promise.all(Array.from({ length: 5 }, async () => {
    while (i < urls.length) { const u = urls[i++]; res[u] = await probe(ctx, u); process.stderr.write('.'); }
  }));
  fs.writeFileSync(out, JSON.stringify(res, null, 1));
  await browser.close();
})();
