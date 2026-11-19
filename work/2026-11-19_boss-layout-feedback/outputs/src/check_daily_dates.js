// 日報頁：每一份日報都能正常呈現（無錯誤、無 undefined/NaN），並確認點甘特圖模塊名稱不會改變所選日期
const { chromium } = require('playwright');
const file = process.argv[2];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + file);
  const dates = await p.evaluate(() => REPORTS.map(r => r.date));
  for (const d of dates) {
    await p.evaluate(h => { location.hash = h; }, 'd' + d.replaceAll('-', ''));
    await p.waitForTimeout(150);
    const m = await p.evaluate(() => ({
      h1: document.getElementById('h1').textContent,
      bad: /undefined|NaN|null/.test(document.body.innerText),
      cards: [...document.querySelectorAll('.card')].map(c => c.querySelector('h3').firstChild.textContent + ':' + c.dataset.s + ':' + [...c.querySelectorAll('.rows > dt')].map(x => x.textContent).join('/')),
    }));
    console.log(d, m.h1, m.bad ? '✗ 有 undefined/NaN/null' : 'OK');
    if (d === '2026-10-29' || d === '2026-11-18') m.cards.forEach(c => console.log('   ', c));
  }
  await p.evaluate(() => { location.hash = 'd20261106'; });
  await p.waitForTimeout(150);
  await p.click('a[href="#m-05"]');
  await p.waitForTimeout(800);
  const after = await p.evaluate(() => ({ h1: document.getElementById('h1').textContent, hash: location.hash, top: Math.round(document.getElementById('m-05').getBoundingClientRect().top) }));
  console.log('點甘特圖「05 LabMind 接入」後：', after.h1, 'hash=' + after.hash, '模塊卡距視窗頂端=' + after.top + 'px');
  console.log(errs.length ? 'ERR ' + errs.join(';') : 'console OK');
  await b.close();
})();
