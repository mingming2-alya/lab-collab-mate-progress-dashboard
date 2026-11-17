// 截取三頁最新版本（桌機 1440×900、手機 390）並量測單屏溢出。
// 用法：node shot.js <repo 根目錄> <輸出資料夾>
const { chromium } = require('playwright');
const path = require('path');
const [root, out] = process.argv.slice(2);
const url = f => 'file://' + path.resolve(root, 'public', f);
const jobs = [
  ['index.html', 'overview-desktop', 1440, 900, false],
  ['daily.html', 'daily-desktop', 1440, 900, false],
  ['arch.html', 'arch-desktop', 1440, 900, true],
  ['index.html', 'overview-mobile', 390, 844, true],
  ['daily.html', 'daily-mobile', 390, 844, true],
];
(async () => {
  const b = await chromium.launch();
  for (const [f, name, w, h, full] of jobs) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto(url(f)); await p.waitForTimeout(600);
    const m = await p.evaluate(() => ({ sh: document.documentElement.scrollHeight, sw: document.documentElement.scrollWidth, ih: innerHeight, iw: innerWidth }));
    await p.screenshot({ path: path.join(out, name + '.png'), fullPage: full });
    console.log(name, `scrollHeight=${m.sh}/${m.ih}`, `scrollWidth=${m.sw}/${m.iw}`, errs.length ? 'ERR ' + errs.join(';') : 'console OK');
    await p.close();
  }
  // 日報頁展開第一張卡
  const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  await p.goto(url('daily.html')); await p.waitForTimeout(400);
  const btn = await p.$('[aria-expanded]');
  if (btn) { await btn.click(); await p.waitForTimeout(300); await p.screenshot({ path: path.join(out, 'daily-desktop-expanded.png'), fullPage: true }); console.log('daily-desktop-expanded ok'); }
  await b.close();
})();
