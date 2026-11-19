// 桌機版不變守門：在桌機寬度（1920、1680、1440、1101，淺色與深色）逐一記錄頁面上每個元素的
// 位置、尺寸與主要計算樣式，和基準比對。比逐像素截圖可靠：截圖會受動畫、字型重繪等時機影響而偶發不同，
// 版面計算結果則是固定的；只要每個元素的位置、尺寸、樣式都相同，桌機畫面就沒有改變。
// 用法：node desktop_guard.js <repo 根目錄> save <基準檔.json>   → 存基準
//       node desktop_guard.js <repo 根目錄> check <基準檔.json>  → 和基準比對，列出不同的元素
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const [root, mode, file] = process.argv.slice(2);
const PAGES = ['index', 'daily'];
const SIZES = [[1920, 1080], [1680, 1050], [1440, 900], [1101, 900]];
const PROPS = ['display', 'visibility', 'opacity', 'color', 'backgroundColor', 'fontSize', 'fontWeight', 'fontFamily', 'lineHeight',
  'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft', 'marginTop', 'marginRight', 'marginBottom', 'marginLeft',
  'borderTopWidth', 'borderLeftWidth', 'borderTopColor', 'borderLeftColor', 'borderRadius', 'whiteSpace', 'textOverflow', 'gridTemplateColumns', 'gap'];

(async () => {
  const b = await chromium.launch();
  const out = {};
  for (const f of PAGES) for (const [w, h] of SIZES) for (const scheme of ['light', 'dark']) {
    const p = await b.newPage({ viewport: { width: w, height: h }, colorScheme: scheme });
    await p.goto('file://' + path.resolve(root, 'public', f + '.html'), { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(600);
    out[`${f} ${w}x${h} ${scheme}`] = await p.evaluate(props => [...document.querySelectorAll('body *')].map((e, i) => {
      const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
      return `${i}:${e.tagName}.${e.className}|${Math.round(r.x)},${Math.round(r.y)},${Math.round(r.width)},${Math.round(r.height)}|` + props.map(k => cs[k]).join(';');
    }), PROPS);
    await p.close();
  }
  await b.close();
  if (mode === 'save') { fs.writeFileSync(file, JSON.stringify(out)); console.log(`已存基準 ${Object.keys(out).length} 種畫面`); return; }
  const base = JSON.parse(fs.readFileSync(file, 'utf8'));
  let bad = 0;
  for (const k of Object.keys(out)) {
    const a = base[k], c = out[k];
    const diffs = [];
    if (a.length !== c.length) diffs.push(`元素數 ${a.length} → ${c.length}`);
    for (let i = 0; i < Math.min(a.length, c.length) && diffs.length < 3; i++) if (a[i] !== c[i]) diffs.push(`${a[i].slice(0, 120)}\n      → ${c[i].slice(0, 120)}`);
    if (diffs.length) { bad++; console.log(`✗ ${k}\n    ${diffs.join('\n    ')}`); }
  }
  console.log(bad ? `✗ 桌機版有 ${bad} 種畫面不同` : `✓ 桌機版 ${Object.keys(out).length} 種畫面（${PAGES.length} 頁 × ${SIZES.length} 寬度 × 淺色／深色）每個元素的位置、尺寸、樣式都與基準相同`);
})();
