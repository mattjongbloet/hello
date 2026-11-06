// Builds canvas.html (opens locally) from tools/canvas.src.html.
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const src = fs.readFileSync(path.join(__dirname, 'canvas.src.html'), 'utf8');
const head = '<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n';
fs.writeFileSync(path.join(ROOT, 'canvas.html'), head + src + '\n</html>\n');
// manifest.js mirrors manifest.json so the canvas can load it over file://
const m = fs.readFileSync(path.join(ROOT, 'manifest.json'), 'utf8');
fs.writeFileSync(path.join(ROOT, 'manifest.js'), `window.MANIFEST = ${JSON.stringify(JSON.parse(m))};\n`);
console.log('wrote canvas.html, manifest.js');
