# 交接文件：SW AI 案例總覽主頁 與 日報頁（2026-11-17）

給下一個 session 的 Claude。這份說明「現在在哪、接下來可能做什麼、要小心的地雷」。

## 一、專案是什麼

`mingming2-alya/lab-collab-mate-progress-dashboard`：一個給主管／副總看的**靜態網站**，不是產品。

- 託管：Cloudflare Workers 靜態資源（`wrangler.jsonc` 的 `assets.directory = ./public`）。**推 main 自動上線**。
- 線上網址：https://lab-collab-mate-progress-dashboard-fxhh.alyanna-wu2642.workers.dev
- **沒有任何建置流程、沒有後端、沒有 npm 依賴**。就是三個 HTML，資料全寫死在檔案的 JS 常數裡。

## 二、三頁結構（2026-11-17 重組後）

| 檔案 | 角色 | 資料來源 |
|---|---|---|
| `public/index.html` | **SW AI 案例總覽**（首頁，`/`） | `CASES` 陣列（9 個案例）、`DIRS`（4 個方向） |
| `public/daily.html` | **Lab Collab Mate 每日進度** | `REPORTS`（日報）、`PLAN`（時程）、`MODULES`（呈現單位） |
| `public/arch.html` | **架構全貌**（三張 SVG） | **由腳本產生，禁手改** |

三頁上方都有分頁列互通：`總覽 / 每日進度 / 架構全貌`。

### Cloudflare 的 .html 導向（重要）
`/daily.html` 會回 **307 → `/daily`**，`/arch.html` → `/arch`。這是 Workers 的 `html_handling` 行為，**瀏覽器自動跟隨，使用者無感**。分頁列的 `href="daily.html"` 不用改。若要用 curl 驗證頁面內容，記得加 `-L`。

## 三、怎麼改內容

### 改總覽主頁（index.html）
- **增修案例** → 改 `CASES` 陣列。每筆：`{id, dir, status, name, dri, sum, ms, week}`
  - `dir`：`dev` / `deploy` / `codio` / `nomi`（對應 `DIRS`）
  - `status`：`doing`（執行中）/ `done`（已結案）/ `wait`（待規劃）
  - `dri`：負責人；`null` 會顯示「待補」
  - `sum`：一句話狀態
  - `ms`：里程碑陣列 `[{d, n}]`；`d` 為 null 表示日期待補
  - `week`：本週進展 `{tag, who, text}`；`null` 表示本週無變動
- **改資料截止日** → `ASOF` 常數。
- **改方向** → `DIRS` 陣列。

### 改每日進度頁（daily.html）
- **新增一天日報** → 用 `day(前一天, d => {...})` 複製再改變動欄位，插到 `REPORTS` 最前面（日期字串格式 `"2026-MM-DD"`）。
- **改時程** → `PLAN`（`steps` 的 `s`/`e`、`ms` 里程碑、`from`/`weeks` 軸線、`updated` 版本戳）。
- **改模塊呈現** → `MODULES` 陣列。

### 改架構圖（arch.html）
**不要直接改 `public/arch.html`。** 正確產線：
```bash
python3 work/2026-11-09_usb-agent-architecture-alignment/outputs/src/build.py <out.html> work/2026-11-09_usb-agent-architecture-alignment/outputs/src/tpl.html
python3 work/2026-11-09_usb-agent-architecture-alignment/outputs/src/build_public_arch.py
```
座標文字改 `build.py`，版型改 `tpl.html`。已實測此產線可重現（輸出逐位元相同）。

## 四、地雷（必讀）

1. **`rebuild_modules.py` 已失效，不要修成可跑**
   `work/2026-11-11_dashboard-schedule-and-arch-tab/outputs/src/rebuild_modules.py` 是一次性腳本，依賴已刪除的 `const SCOPE = [`，重跑必拋 `ValueError`。**已加 docstring 警示**。若「修成可跑」它會覆寫 `public/index.html`（破壞）。

2. **不要動 main 前先推分支**
   使用者偏好**先推工作分支、給截圖、等確認**再合併 main。`CLAUDE.md` 雖寫「直接推 main」，但實際協作時他都要先看過。（見記憶 `feedback_repo_workflow`）

3. **設計類修改要可量測驗證**
   使用者明確要求：設計類修改要附**可量測驗證**（CSS 座標、色彩對比 WCAG、灰階測試），不可只說「看起來有差」。（見記憶 `feedback_style_design_sourcing`）

4. **收合界線（日報頁）**
   老闆要看的**必須外露**：時程現況（階段→現象→預計完成→下一階段）、風險／需決策、已有對策、DRI。
   **可收合（FYI）**：逐工具明細列、step 步驟條。
   用詞要**主管維度**（「預計完成 11/27」），不要工程口吻（「ETA 剩 10 天」）。

5. **單屏約束**
   總覽主頁與日報頁都要求**單屏看完**（1920×1080 / 1680×1050 / 1440×900 皆 0px 溢出）。改動後務必用 Playwright 重量。

6. **Token**
   使用者會提供 fine-grained PAT 做推送。**測試寫入用 `git push` 才準**——用 `POST /git/refs` 測會回 403 但 token 其實可寫。**提醒他事後撤銷貼在對話裡的 token。**

## 五、目前狀態（2026-11-17）

- **已上線**：main = `27f140d`（合併 `claude/sw-ai-overview`）。
- **線上已驗證**：`/` 標題「SW AI 推動全貌」、`/daily` 與 `/arch` 皆 200。
- **工作分支**：`claude/sw-ai-overview`（已合併，可刪）。

### 待補資料（最可能的下一個任務）
9 個案例中，**除 Lab Collab Mate 外，其餘 8 案的 DRI、里程碑日期、本週成果都標「待補」**。使用者補齊後，填進 `public/index.html` 的 `CASES` 就會自動顯示。

| 方向 | 案例 | 缺什麼 |
|---|---|---|
| 自行開發 | AI Hiring Agent | DRI、里程碑日期 |
| 自行開發 | Lab Collab Mate | DRI（有 11/11 進展） |
| 模型部署研究 | 2 台 Mac Mini 集群上限 | DRI、里程碑 |
| 模型部署研究 | 4 台 Mac Mini 集群上限 | DRI、里程碑 |
| Codio 活化使用 | 工具腳本類開發 | DRI、里程碑 |
| Codio 活化使用 | 大型系統類開發 | DRI、里程碑 |
| Codio 活化使用 | IDE 串接研究 | DRI、里程碑 |
| Nomi 活化使用 | AAS 系統重構 | DRI、里程碑 |
| Nomi 活化使用 | 簡報技能研究 | DRI、里程碑 |

### 其他待確認
- 是否要把「每日進度」的入口放進首頁某張卡（目前 Lab Collab Mate 卡已有摘要，未連到日報頁）。

## 六、驗證腳本（本次用過的）

Playwright 腳本在沙箱 `/tmp/pw/`（**不持久**，新 session 要重建）。量測重點：
```js
// 單屏檢查
document.documentElement.scrollHeight <= innerHeight
// 橫向溢出
document.documentElement.scrollWidth <= innerWidth
// 卡片座標
[...document.querySelectorAll('.card')].map(c => c.getBoundingClientRect())
```
色彩對比公式（WCAG）：相對亮度 → `(L1+0.05)/(L2+0.05)`。
灰階測試：把色票轉灰階後比較亮度差，ΔL < 0.05 視為難辨識。

## 七、相關記憶

新對話會自動載入這些（存在 `memory/`）：
- `project_lab_collab_mate` — 專案架構與演進
- `project_sw_ai_cases` — 9 個案例清單
- `feedback_repo_workflow` — 提交流程
- `feedback_style_design_sourcing` — 設計驗證要求
