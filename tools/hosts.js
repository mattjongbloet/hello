// Lists every host a page requests, and which failed (to find CDN hosts the network policy blocks).
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const ok = new Set(), bad = new Set();
  page.on('requestfinished', r => ok.add(new URL(r.url()).host));
  page.on('requestfailed', r => { try { bad.add(new URL(r.url()).host + ' ' + r.failure().errorText); } catch {} });
  for (const u of process.argv.slice(2)) {
    try { await page.goto(u, { waitUntil: 'networkidle', timeout: 30000 }); } catch (e) { console.log(u, e.message.split('\n')[0]); }
    for (let y = 0; y < 20000; y += 800) { await page.mouse.wheel(0, 800); await page.waitForTimeout(150); }
  }
  console.log('OK:', [...ok].join(' ')); console.log('FAIL:\n' + [...bad].join('\n'));
  await browser.close();
})();
