# SW AI 案例總覽 與 Lab Collab Mate 每日進度

給主管與副總查看的進度頁。

- 頁面
  - `public/index.html`：**SW AI 案例總覽**（首頁）。所有 AI 案例的時程、DRI、一句話狀態與本週進展；單屏看完，點卡片展開細節。
  - `public/daily.html`：**Lab Collab Mate 每日進度**。資料在檔案內的 `REPORTS` 陣列，最新一天在最前面；桌機版為摘要格（點開展開），手機版全展開。
  - `public/arch.html`：**架構全貌**。由腳本產生，不可手改（見下）。
- 部署：Cloudflare Workers 靜態資源，設定見 `wrangler.jsonc`；推送到 main 後自動上線
- 網址：https://lab-collab-mate-progress-dashboard-fxhh.alyanna-wu2642.workers.dev
