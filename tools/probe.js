// node tools/probe.js out.json url... : status, final URL, title, short text, 404-ish flag for each URL.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [out, ...urls] = process.argv.slice(2);
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
  const res = {}; let i = 0;
  await Promise.all(Array.from({ length: 6 }, async () => {
    while (i < urls.length) {
      const u = urls[i++]; const p = await ctx.newPage();
      try {
        const r = await p.goto(u, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await p.waitForLoadState('networkidle', { timeout: 8000 }).catch(() => {}); await p.waitForTimeout(800);
        const t = await p.evaluate(() => document.body.innerText.replace(/\s+/g, ' ').slice(0, 160));
        res[u] = { s: r && r.status(), f: p.url(), title: await p.title(), t, pw: await p.locator('input[type=password]').count() };
      } catch (e) { res[u] = { err: e.message.split('\n')[0] }; }
      await p.close();
    }
  }));
  fs.writeFileSync(out, JSON.stringify(res, null, 1)); await b.close();
})();
