// node crop.js <file> <width> <out> <selector> [index] [scheme]
const { chromium } = require('playwright');
const [file, w, out, sel, idx, scheme] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: 900 }, colorScheme: scheme || 'light' });
  await p.goto('file://' + file);
  await p.waitForTimeout(400);
  const els = await p.$$(sel);
  await els[+(idx || 0)].screenshot({ path: out });
  await b.close();
})();
