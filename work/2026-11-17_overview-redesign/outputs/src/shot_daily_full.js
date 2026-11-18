// 日報頁「桌機預設全展開」驗證：整頁高度、橫向溢出、undefined 字樣、console，並截整頁圖。
// 用法：node shot_daily_full.js <repo 根目錄> <輸出資料夾>
const { chromium } = require('playwright');
const path = require('path');
const [root, out] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  for (const [w, h] of [[1920, 1080], [1440, 900], [390, 844]]) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: w === 1440 ? 2 : 1 });
    const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    await p.goto('file://' + path.resolve(root, 'public', 'daily.html'));
    await p.waitForTimeout(500);
    const m = await p.evaluate(() => ({
      sh: document.documentElement.scrollHeight, sw: document.documentElement.scrollWidth,
      undef: document.body.innerText.includes('undefined'),
      exp: [...document.querySelectorAll('#mods .card')].map(c => c.getAttribute('aria-expanded')).join(','),
    }));
    console.log(`${w}x${h} 整頁高=${m.sh}px（${(m.sh / h).toFixed(1)} 屏） 橫向溢出=${m.sw - w}px undefined=${m.undef} 展開=${m.exp}`, errs.length ? 'ERR ' + errs.join(';') : 'console OK');
    if (w === 1440) await p.screenshot({ path: path.join(out, 'daily-expanded-1440.png'), fullPage: true });
    await p.close();
  }
  await b.close();
})();
