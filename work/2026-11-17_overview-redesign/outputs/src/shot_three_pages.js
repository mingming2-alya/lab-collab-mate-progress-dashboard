// 三頁風格一致性檢查：總覽、每日進度、架構全貌，各截淺色與深色 1440×900 首屏，並檢查橫向溢出與 console 錯誤。
// 用法：node shot_three_pages.js <repo 根目錄> <輸出資料夾>
const { chromium } = require('playwright');
const path = require('path');
const [root, out] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  for (const f of ['index', 'daily', 'arch']) {
    for (const scheme of ['light', 'dark']) {
      const p = await b.newPage({ viewport: { width: 1440, height: 900 }, colorScheme: scheme });
      const errs = [];
      p.on('pageerror', e => errs.push(e.message));
      await p.goto('file://' + path.resolve(root, 'public', f + '.html'));
      await p.waitForTimeout(600);
      const m = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth - innerWidth, font: getComputedStyle(document.body).fontFamily.split(',')[0] }));
      console.log(`${f} ${scheme} 橫向溢出=${m.sw}px 字體首選=${m.font}`, errs.length ? 'ERR ' + errs.join(';') : 'console OK');
      await p.screenshot({ path: path.join(out, `theme-${f}-${scheme}.png`) });
      await p.close();
    }
  }
  await b.close();
})();
