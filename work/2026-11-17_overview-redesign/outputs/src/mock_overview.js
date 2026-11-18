// 總覽頁「示意版」截圖：在瀏覽器記憶體裡填入示意回報，讓使用者看到資料齊全時的樣子。
// 頁面頂部加紅色橫條標明「示意資料」。不修改 public/index.html；示意內容不是真實回報。
// 用法：node mock_overview.js <repo 根目錄> <輸出 png>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const [root, out, cssPath] = process.argv.slice(2);  // cssPath（選填）：風格示意用的覆寫樣式
const src = fs.readFileSync(path.resolve(root, 'public', 'index.html'), 'utf8');

const SAMPLE = {
  '客戶軟體驗證': { now: [1, 2], subs: [['Bundle', 2], ['proxima', 1], ['EFI', 1]], hl: [{ i: 0, s: 'Bundle', t: '正式數據首次跑通全流程' }],
    done: ['Bundle 正式數據首次跑通全流程', 'proxima 新增 2 個自動化節點'], next: ['Bundle 連續五次跑通', 'proxima 首次跑通'] },
  '產品 Panic 處理': { now: -1, done: ['串口方案比較完成，建議只讀取結果'], next: ['11/27 前與 Simon、Gary 定案串口方案'] },
  '產品測試軟體開發': { now: -1, done: [], next: ['整理 Codio 融入工作流的調研題目'] },
  '產品失效分析': { now: -1, done: [], next: ['取得 AI FA 平台測試帳號'] },
  'LabMind 接入': { now: 0, done: ['完成 LabMind 兩種接法比較，建議方案 B'], next: ['與 LabMind 團隊約定方案評審會'],
    help: '需要副總協調 LabMind 團隊於 12/5 前安排方案評審' },
  '工具腳本類開發': { done: ['IoT Team 新增 3 支 Codio 開發的檢測腳本'], next: ['協助 FA 再導入 1 個腳本情境'], hl: [{ i: 0, s: 'Codio', t: 'IoT Team 新增 3 支檢測腳本' }] },
  '大型系統類開發': { done: ['InvestGo 需求完成需求梳理與 SRS 初稿'], next: ['InvestGo 原型設計評審'] },
  'IDE 串接研究': { conclusion: 'VS Code 可直接呼叫 Codio，開發體驗接近原生', done: ['完成 VS Code 串接測試'], next: ['測試 JetBrains 系列 IDE'] },
  'AAS 系統重構': { done: ['xTrack 既有模組盤點完成，共 18 個'], next: ['完成第一個模組重構'] },
  '開放複用': { nums: { '尋求': 5, '申請': 3, '已上線': 1 }, hl: [{ i: 0, s: 'Hiring Agent', t: '財務處完成部署並開始試用' }], done: ['財務處完成部署並開始試用'], next: ['協助品保處提交申請'] },
  'Presentation Skill': { now: 2, subDone: 1, done: ['內容梳理子階段完成並在 3 份簡報試用'], next: ['完成風格與排版子階段'] },
  'Development Skill': { now: 2, subDone: 2, done: ['需求梳理、SRS 子階段完成，以 InvestGo 驗證'], next: ['完成原型設計子階段'] },
  '驗證兩台': { conclusion: '兩台可穩定運行 32B 模型，每秒約 12 字', done: ['完成 32B 模型 2 小時穩定性測試'], next: ['測試 70B 量化模型'] },
  '驗證四台': { done: ['四台集群環境建置完成'], next: ['以 Hiring Agent 跑第一次端到端測試'] },
};
const inject = `
const __S = ${JSON.stringify(SAMPLE)};
MODULES.forEach(p => p.reqs.forEach(r => { if (__S[r.name]) r.rep = __S[r.name]; }));
/* ===== 計算與呈現 ===== */`;
const banner = '<div style="background:#B3261E;color:#fff;font-weight:700;text-align:center;font-size:13px;padding:3px 0">示意資料：以下內容為版面示意，不是真實回報</div>';
const html = src.replace('/* ===== 計算與呈現 ===== */', inject).replace('<div class="page">', banner + '<div class="page">');
if (!html.includes('示意資料：')) throw new Error('示意橫條沒有插入成功');
const styled = cssPath ? html.replace('</style>', fs.readFileSync(cssPath, 'utf8') + '\n</style>') : html;

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  await p.setContent(styled);
  await p.waitForTimeout(300);
  const sh = await p.evaluate(() => document.documentElement.scrollHeight);
  console.log(`示意版 1440x900 scrollHeight=${sh}（含示意橫條 約 25px）`);
  await p.screenshot({ path: out });
  await b.close();
})();
