// 日報頁改名後驗證：單屏溢出、console、截圖（收合＋甘特圖展開）。
// 用法：node shot_daily.js <repo 根目錄> <輸出資料夾>
const { chromium } = require('playwright');
const path = require('path');
const [root, out] = process.argv.slice(2);
const url = 'file://' + path.resolve(root, 'public', 'daily.html');

(async () => {
  const b = await chromium.launch();
  for (const [w, h] of [[1920, 1080], [1680, 1050], [1440, 900], [390, 844]]) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: w === 1440 ? 2 : 1 });
    const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await p.goto(url);
    await p.waitForTimeout(500);
    const m = await p.evaluate(() => ({
      sh: document.documentElement.scrollHeight,
      sw: document.documentElement.scrollWidth,
      h3: [...document.querySelectorAll('h3')].map(e => {
        const r = e.getBoundingClientRect();
        return { t: e.textContent, w: Math.round(r.width), h: Math.round(r.height) };
      }),
    }));
    console.log(`${w}x${h} scrollHeight=${m.sh} 垂直溢出=${m.sh - h}px 橫向溢出=${m.sw - w}px`, errs.length ? 'ERR ' + errs.join(';') : 'console OK');
    if (w === 1440) {
      console.log(JSON.stringify(m.h3));
      await p.screenshot({ path: path.join(out, 'daily-renamed-1440.png') });
      for (const s of await p.$$('summary')) {
        if ((await s.textContent()).includes('完整時程')) { await s.click(); break; }
      }
      await p.waitForTimeout(300);
      await p.screenshot({ path: path.join(out, 'daily-renamed-gantt-1440.png'), fullPage: true });
    }
    await p.close();
  }
  await b.close();
})();
