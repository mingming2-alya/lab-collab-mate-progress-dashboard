// 總覽頁自我檢查：深色模式截圖、手機截圖（示意資料，用來看資料齊全時的版面），以及被截斷的文字清單。
// 用法：node check_overview_modes.js <repo 根目錄> <輸出資料夾>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const [root, out] = process.argv.slice(2);
const mockSrc = fs.readFileSync(path.join(__dirname, 'mock_overview.js'), 'utf8');
const SAMPLE = eval('(' + mockSrc.match(/const SAMPLE = (\{[\s\S]*?\n\});/)[1] + ')');
const src = fs.readFileSync(path.resolve(root, 'public', 'index.html'), 'utf8');
const html = src.replace('/* ===== 計算與呈現 ===== */',
  `const __S = ${JSON.stringify(SAMPLE)};\nPROJECTS.forEach(p => p.reqs.forEach(r => { if (__S[r.name]) r.rep = __S[r.name]; }));\n/* ===== 計算與呈現 ===== */`);

(async () => {
  const b = await chromium.launch();
  const dark = await b.newPage({ viewport: { width: 1440, height: 900 }, colorScheme: 'dark' });
  await dark.setContent(html); await dark.waitForTimeout(300);
  await dark.screenshot({ path: path.join(out, 'overview-mock-dark-1440.png') });
  const cut = await dark.evaluate(() => [...document.querySelectorAll('.line,.wk,.hl li,.dri')]
    .filter(e => e.scrollWidth > e.clientWidth + 1).map(e => e.textContent.trim().slice(0, 40)));
  console.log('1440 被截斷的文字：', cut.length ? '\n  ' + cut.join('\n  ') : '無');
  const m = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  await m.setContent(html); await m.waitForTimeout(300);
  console.log('手機 橫向溢出', await m.evaluate(() => document.documentElement.scrollWidth - innerWidth), 'px');
  await m.screenshot({ path: path.join(out, 'overview-mock-mobile.png'), fullPage: true });
  await b.close();
})();
