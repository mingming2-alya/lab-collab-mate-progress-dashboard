// 本週成果重點色候選：注入 CSS 變數覆寫後截圖（1440×900 與 1920×1080 上半部）
// node variants.js <index.html> <outdir>
const { chromium } = require('playwright');
const path = require('path');
const [file, out] = process.argv.slice(2);
const V = {
  A_teal: '',
  B_amber: ':root{--hl:#9A5800;--hl-fg:#FFFFFF;--hl-key:#FFE1A6;--hl-line:rgba(255,255,255,.26);--hl-lab:#7E4800}',
  C_navy: ':root{--hl:#2C4A78;--hl-fg:#FFFFFF;--hl-key:#BFD6F5;--hl-line:rgba(255,255,255,.24);--hl-lab:#223B61}',
};
(async () => {
  const b = await chromium.launch();
  for (const [k, css] of Object.entries(V)) {
    const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
    await p.goto('file://' + file);
    if (css) await p.addStyleTag({ content: css });
    await p.waitForTimeout(400);
    await p.screenshot({ path: path.join(out, `hl-${k}.png`) });
    await p.close();
  }
  await b.close();
})();
