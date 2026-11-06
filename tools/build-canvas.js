// Builds canvas.html (opens locally) from tools/canvas.src.html.
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const src = fs.readFileSync(path.join(__dirname, 'canvas.src.html'), 'utf8');
const head = '<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n';
fs.writeFileSync(path.join(ROOT, 'canvas.html'), head + src + '\n</html>\n');
// Merge per-site capture results (shots/_manifest/{id}.json) into manifest.json, in sites.json order.
const sites = JSON.parse(fs.readFileSync(path.join(ROOT, 'sites.json'), 'utf8'));
const manifest = { generated_at: new Date().toISOString(), order: [], sites: {} };
for (const s of sites) {
  const f = path.join(ROOT, 'shots', '_manifest', `${s.id}.json`);
  if (!fs.existsSync(f)) continue;
  manifest.sites[s.id] = JSON.parse(fs.readFileSync(f, 'utf8'));
  manifest.order.push(s.id);
}
fs.writeFileSync(path.join(ROOT, 'manifest.json'), JSON.stringify(manifest, null, 2));
// manifest.js mirrors manifest.json so the canvas can load it over file://
fs.writeFileSync(path.join(ROOT, 'manifest.js'), `window.MANIFEST = ${JSON.stringify(manifest)};\n`);
console.log('wrote canvas.html, manifest.js');
