// 驗證日報頁的時程狀態以「所選日報日期」為基準，不隨瀏覽當天變動。
// 對 11/11、11/06 兩份日報，在兩個不同的瀏覽器時鐘下，抓 Bundle 驗證步驟條的標籤與甘特圖基準線文字。
// 用法：node check_basedate.js <repo 根目錄>
const { chromium } = require('playwright');
const path = require('path');
const root = process.argv[2];
const url = 'file://' + path.resolve(root, 'public', 'daily.html');

(async () => {
  const b = await chromium.launch();
  for (const clock of ['2026-11-18T10:00:00', '2026-12-20T10:00:00']) {
    for (const hash of ['', '#d20261106']) {
      const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
      const p = await ctx.newPage();
      await p.clock.setFixedTime(new Date(clock));
      const errs = [];
      p.on('pageerror', e => errs.push(e.message));
      await p.goto(url + hash);
      await p.waitForTimeout(400);
      const r = await p.evaluate(() => {
        const row = [...document.querySelectorAll('.mrow')].find(x => x.textContent.includes('Bundle 驗證'));
        const steps = row ? [...row.querySelectorAll('li')].map(li => li.innerText.replace(/\s+/g, ' ').trim()) : [];
        const line = document.querySelector('.todayl');
        return { h1: document.getElementById('h1').textContent, steps, line: line ? line.textContent : '(不在軸內)' };
      });
      console.log(`時鐘 ${clock.slice(0, 10)}｜${r.h1}｜甘特基準線：${r.line}`, errs.length ? 'ERR ' + errs.join(';') : '');
      r.steps.forEach(s => console.log('   ', s));
      await ctx.close();
    }
  }
  await b.close();
})();
