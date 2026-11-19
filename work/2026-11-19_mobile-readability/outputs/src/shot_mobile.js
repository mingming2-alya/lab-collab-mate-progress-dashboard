// 手機版檢查：總覽頁、日報頁在 390×844（iPhone 一般尺寸）與 360×780（小螢幕安卓）截整頁圖，
// 並量測可讀性指標：最小字級、橫向溢出、被截斷的文字、點擊目標小於 32px 的互動元件。
// 用法：node shot_mobile.js <repo 根目錄> <輸出資料夾> [檔名前綴]
const { chromium } = require('playwright');
const path = require('path');
const [root, out, prefix = 'mobile'] = process.argv.slice(2);

(async () => {
  const b = await chromium.launch();
  for (const f of ['index', 'daily']) for (const [w, h] of [[390, 844], [360, 780]]) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
    const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    await p.goto('file://' + path.resolve(root, 'public', f + '.html'));
    await p.waitForTimeout(800);
    const m = await p.evaluate(() => {
      const vis = [...document.querySelectorAll('body *')].filter(e => {
        const r = e.getBoundingClientRect(); const cs = getComputedStyle(e);
        return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
      });
      const sizes = vis.map(e => parseFloat(getComputedStyle(e).fontSize));
      const small = vis.filter(e => parseFloat(getComputedStyle(e).fontSize) < 12).map(e => e.textContent.trim().slice(0, 20));
      const cut = [...document.querySelectorAll('body *')].filter(e => getComputedStyle(e).textOverflow === 'ellipsis' && e.scrollWidth > e.clientWidth + 1).map(e => e.textContent.trim().slice(0, 30));
      const taps = [...document.querySelectorAll('a, button, select, summary, [role=button]')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height < 32; }).map(e => e.textContent.trim().slice(0, 15));
      return { sh: document.documentElement.scrollHeight, sw: document.documentElement.scrollWidth - innerWidth,
        min: Math.min(...sizes), small: [...new Set(small)].slice(0, 8), cut: cut.slice(0, 8), taps: [...new Set(taps)].slice(0, 8) };
    });
    console.log(`${f} ${w}x${h} 整頁高=${m.sh}px（${(m.sh / h).toFixed(1)} 屏） 橫向溢出=${m.sw}px 最小字級=${m.min}px`, errs.length ? 'ERR ' + errs.join(';') : 'console OK');
    if (m.small.length) console.log('   小於 12px：', m.small.join('｜'));
    if (m.cut.length) console.log('   被截斷：', m.cut.join('｜'));
    if (m.taps.length) console.log('   點擊目標太矮（<32px）：', m.taps.join('｜'));
    if (w === 390) await p.screenshot({ path: path.join(out, `${prefix}-${f}-390.png`), fullPage: true });
    await p.close();
  }
  await b.close();
})();
