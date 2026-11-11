// Overview thumbnails: node tools/thumbs.js a-clarity a1-serif ...  (folders under redesigns/)
// Writes redesigns/thumbs/{dir}-{index,case-pmi,about}.jpg (1440×900 viewport → 960×600) and {dir}-index-m.jpg (390×844 → 260×563).
// Pass dir@anchor to shoot the home page scrolled to an anchor, e.g. a3-grid@work.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
const ROOT = path.resolve(__dirname, '..'); const OUT = path.join(ROOT, 'redesigns', 'thumbs');
async function shot(ctx, file, out, size, anchor) {
  const p = await ctx.newPage();
  await p.goto('file://' + file, { waitUntil: 'networkidle' }).catch(() => {});
  await p.evaluate(async (anchor) => {
    await document.fonts.ready;
    document.querySelectorAll('.pre').forEach((el) => el.classList.remove('pre'));
    if (anchor) document.getElementById(anchor)?.scrollIntoView({ behavior: 'instant' });
  }, anchor);
  await p.waitForTimeout(500);
  const png = await p.screenshot();
  await p.close();
  const tmp = out + '.png'; fs.writeFileSync(tmp, png);
  require('child_process').execFileSync('python3', ['-c', `from PIL import Image; Image.open(${JSON.stringify(tmp)}).convert('RGB').resize((${size[0]}, ${size[1]}), Image.LANCZOS).save(${JSON.stringify(out)}, quality=86)`]);
  fs.unlinkSync(tmp);
}
(async () => {
  const b = await chromium.launch();
  const desk = await b.newContext({ viewport: { width: 1440, height: 900 } });
  const phone = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 1 });
  for (const arg of process.argv.slice(2)) {
    const [dir, anchor] = arg.split('@'); const base = path.join(ROOT, 'redesigns', dir);
    await shot(desk, path.join(base, 'index.html'), path.join(OUT, `${dir}-index.jpg`), [960, 600], anchor);
    await shot(desk, path.join(base, 'case-pmi.html'), path.join(OUT, `${dir}-case-pmi.jpg`), [960, 600]);
    await shot(desk, path.join(base, 'about.html'), path.join(OUT, `${dir}-about.jpg`), [960, 600]);
    await shot(phone, path.join(base, 'index.html'), path.join(OUT, `${dir}-index-m.jpg`), [260, 563]);
    console.log('thumbs', dir);
  }
  await b.close();
})();
