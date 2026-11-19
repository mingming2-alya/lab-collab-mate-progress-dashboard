// 改版前（main 11-19 版）日報頁「完整時程」甘特圖展開後截圖，用來產生 before-gantt-1440.png；新版已無 #gbox，改用 crop.js 截 section。
// 用法：node shot_gantt.js <repo 根目錄> <輸出資料夾>
const { chromium } = require('playwright');
const path = require('path');
const [root, out] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto('file://' + path.resolve(root, 'public', 'daily.html'));
  await p.evaluate(() => { document.getElementById('gbox').open = true; });
  await p.waitForTimeout(400);
  const el = await p.$('#gbox');
  await el.screenshot({ path: path.join(out, 'gantt-1440.png') });
  await b.close();
})();
