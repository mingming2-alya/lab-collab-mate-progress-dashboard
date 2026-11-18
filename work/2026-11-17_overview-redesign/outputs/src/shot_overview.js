// 總覽頁驗證：三個桌機解析度單屏不溢出、手機無橫向溢出、console 無錯誤，並截圖。
// 用法：node shot_overview.js <repo 根目錄> <輸出資料夾>
const { chromium } = require('playwright');
const path = require('path');
const [root, out] = process.argv.slice(2);
const url = 'file://' + path.resolve(root, 'public', 'index.html');

(async () => {
  const b = await chromium.launch();
  for (const [w, h] of [[1920, 1080], [1680, 1050], [1440, 900], [820, 1180], [390, 844]]) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: w === 1440 || w === 390 ? 2 : 1 });
    const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await p.goto(url);
    await p.waitForTimeout(400);
    const m = await p.evaluate(() => ({
      sh: document.documentElement.scrollHeight, sw: document.documentElement.scrollWidth,
      rows: document.querySelectorAll('.req').length,
      undef: document.body.innerText.includes('undefined') || document.body.innerText.includes('NaN'),
    }));
    const desktop = w >= 1440;
    console.log(`${w}x${h} scrollHeight=${m.sh}${desktop ? `（溢出 ${m.sh - h}px）` : ''} 橫向溢出=${m.sw - w}px 需求列=${m.rows} undefined/NaN=${m.undef}`, errs.length ? 'ERR ' + errs.join(';') : 'console OK');
    if (w === 1440) await p.screenshot({ path: path.join(out, 'overview-1440.png') });
    if (w === 1920) await p.screenshot({ path: path.join(out, 'overview-1920.png') });
    if (w === 390) await p.screenshot({ path: path.join(out, 'overview-mobile.png'), fullPage: true });
    await p.close();
  }
  await b.close();
})();
