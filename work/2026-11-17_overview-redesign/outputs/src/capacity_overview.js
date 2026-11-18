// 總覽頁容量測試：在瀏覽器記憶體中把 14 個需求都填上「本週完成 2 條、下週 2 條、每條約 N 字」，
// 量測三個桌機解析度是否仍單屏。不修改任何檔案；測試文字只存在於這次瀏覽器執行。
// 用法：node capacity_overview.js <repo 根目錄> <每條字數> [截圖路徑]
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const [root, nChars, shot] = process.argv.slice(2);
const src = fs.readFileSync(path.resolve(root, 'public', 'index.html'), 'utf8');
const fill = `
const __n = ${+nChars};
const __t = k => "測試文字".repeat(Math.ceil(__n / 4)).slice(0, __n - 1) + k;
PROJECTS.forEach(p => p.reqs.forEach(r => {
  r.rep = { now: r.steps ? 1 : null, done: [__t("一"), __t("二")], next: [__t("三"), __t("四")],
            conclusion: r.type === "research" ? __t("論") : undefined,
            nums: r.nums ? Object.fromEntries(r.nums.map((k, i) => [k, i + 2])) : undefined };
}));
/* ===== 計算與呈現 ===== */`;
const html = src.replace('/* ===== 計算與呈現 ===== */', fill);

(async () => {
  const b = await chromium.launch();
  for (const [w, h] of [[1920, 1080], [1680, 1050], [1440, 900]]) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: shot && w === 1440 ? 2 : 1 });
    await p.setContent(html);
    await p.waitForTimeout(300);
    const sh = await p.evaluate(() => document.documentElement.scrollHeight);
    console.log(`每條 ${nChars} 字｜${w}x${h} scrollHeight=${sh} 溢出=${sh - h}px`);
    if (shot && w === 1440) await p.screenshot({ path: shot });
    await p.close();
  }
  await b.close();
})();
