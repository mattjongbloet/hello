// Review helper: node tools/shoot.js outdir page.html [...]
// Full-page screenshots at 1440 and 390, plus console errors, horizontal overflow and broken images.
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [out, ...pages] = process.argv.slice(2);
  const b = await chromium.launch();
  for (const [w, opts] of [[1440, { viewport: { width: 1440, height: 900 } }], [390, { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }]]) {
    const ctx = await b.newContext(opts);
    for (const f of pages) {
      const p = await ctx.newPage(); const errs = [];
      p.on('pageerror', (e) => errs.push('pageerror: ' + e.message));
      p.on('console', (m) => m.type() === 'error' && errs.push('console: ' + m.text()));
      await p.goto('file://' + path.resolve(f), { waitUntil: 'networkidle' }).catch(() => {});
      await p.evaluate(async () => { await document.fonts.ready; for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); } scrollTo(0, 0); });
      await p.waitForTimeout(900);
      const info = await p.evaluate(() => ({
        overflow: document.documentElement.scrollWidth - innerWidth,
        broken: [...document.images].filter((i) => i.complete && !i.naturalWidth).map((i) => i.src.split('/').pop()),
        h: document.documentElement.scrollHeight,
      }));
      const name = f.replace(/[\/.]/g, '_') + '-' + w + '.png';
      await p.screenshot({ path: path.join(out, name), fullPage: true });
      console.log(`${w} ${f} h=${info.h} overflow=${info.overflow}${info.broken.length ? ' BROKEN=' + info.broken : ''}${errs.length ? ' ERR=' + errs.join(' | ') : ''}`);
      await p.close();
    }
    await ctx.close();
  }
  await b.close();
})();
