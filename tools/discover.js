// Usage: node tools/discover.js <url> [more urls...]
// Prints internal links found on each page (text + href + whether in nav/header/footer).
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  for (const url of process.argv.slice(2)) {
    const page = await ctx.newPage();
    try {
      const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
      await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
      await page.waitForTimeout(1500);
      const info = await page.evaluate(() => {
        const out = [];
        for (const a of document.querySelectorAll('a[href]')) {
          const r = a.getBoundingClientRect();
          out.push({
            text: (a.innerText || a.getAttribute('aria-label') || a.title || '').trim().replace(/\s+/g, ' ').slice(0, 80),
            href: a.href,
            zone: a.closest('nav,header') ? 'nav' : a.closest('footer') ? 'footer' : 'body',
            y: Math.round(r.top + scrollY),
          });
        }
        return { title: document.title, final: location.href, links: out, pw: !!document.querySelector('input[type=password]') };
      });
      console.log(`\n=== ${url} -> ${info.final} [${resp && resp.status()}] "${info.title}" pw=${info.pw}`);
      const seen = new Set();
      for (const l of info.links) {
        const k = l.href + '|' + l.text;
        if (seen.has(k)) continue; seen.add(k);
        console.log(`${l.zone.padEnd(6)} y=${String(l.y).padStart(5)}  ${l.text.padEnd(40)} ${l.href}`);
      }
    } catch (e) { console.log(`\n=== ${url} ERROR ${e.message.split('\n')[0]}`); }
    await page.close();
  }
  await browser.close();
})();
