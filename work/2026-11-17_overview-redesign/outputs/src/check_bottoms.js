// 驗證總覽頁三欄卡片底部切齊：量每一欄最後一張模塊卡的下緣座標（真實資料與示意資料各量一次）。
// 用法：node check_bottoms.js <repo 根目錄>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const root = process.argv[2];
const src = fs.readFileSync(path.resolve(root, 'public', 'index.html'), 'utf8');
const mockSrc = fs.readFileSync(path.join(__dirname, 'mock_overview.js'), 'utf8');
const SAMPLE = eval('(' + mockSrc.match(/const SAMPLE = (\{[\s\S]*?\n\});/)[1] + ')');
const mock = src.replace('/* ===== 計算與呈現 ===== */',
  `const __S = ${JSON.stringify(SAMPLE)};\nMODULES.forEach(p => p.reqs.forEach(r => { if (__S[r.name]) r.rep = __S[r.name]; }));\n/* ===== 計算與呈現 ===== */`);

(async () => {
  const b = await chromium.launch();
  for (const [label, html] of [['真實資料', src], ['示意資料', mock]]) {
    for (const [w, h] of [[1920, 1080], [1440, 900]]) {
      const p = await b.newPage({ viewport: { width: w, height: h } });
      await p.setContent(html);
      await p.waitForTimeout(300);
      const bottoms = await p.evaluate(() => [...document.querySelectorAll('.col')]
        .map(c => { const m = c.querySelectorAll('.mod'); return Math.round(m[m.length - 1].getBoundingClientRect().bottom); }));
      const spread = Math.max(...bottoms) - Math.min(...bottoms);
      console.log(`${label} ${w}x${h} 三欄下緣=${JSON.stringify(bottoms)} 差距=${spread}px ${spread <= 1 ? '✓ 切齊' : '✗ 未切齊'}`);
      await p.close();
    }
  }
  await b.close();
})();
