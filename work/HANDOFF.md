# 交接文件（最新：2026-11-19）

給下一個 session 的 Claude。先讀這份，再讀 `work/INDEX.md` 與各任務的 STATUS.md。
（舊版交接見 `work/2026-11-17_sw-ai-overview-and-daily-density/HANDOFF.md`，**部分內容已過時**，以本檔為準。）

## 一、網站現況（main 已上線）

靜態網站，推 main 自動部署（Cloudflare Workers，`public/`）。三頁：

| 檔案 | 角色 | 讀者 |
|---|---|---|
| `public/index.html` | **總覽首頁**：本週進度（給副總） | 副總，一屏看完 |
| `public/daily.html` | **Lab Collab Mate 每日日報** | 課長，詳細、可捲動 |
| `public/arch.html` | 架構全貌（**由腳本產生，禁手改**） | — |

導覽：首頁**沒有分頁籤**；點首頁「02 案例開發・Lab Collab Mate」整組進日報。日報頁、架構頁上方是「← 總覽｜每日進度｜架構全貌」。

## 二、怎麼更新資料

### 總覽首頁（`index.html` 的 `<script>` 資料區）
- `WEEK`：週次，**週五到隔週四**（目前 11/13–11/19）。`ASOF`：資料截至日（所有時間計算以它為準）。
- `MODULES`：四大模塊（成熟度路線）01 課題研究 → 02 案例開發 → 03 導入試用 → 04 推廣複用；`col` 決定欄（03、04 疊在第三欄）。共 14 個需求。
- 每個需求的 `rep`（本週回報）：`now` 步驟索引、`done` 本週、`next` 下週、`issue` 問題（團隊自理，不算進度）、`help` 需副總幫忙、`conclusion` 研究型結論、`pill` 覆寫狀態標籤、`hideDone` 卡片不顯示本週、`nums` 推廣型數字、`hl` 本週成果 `{i, s:主題, t:短句, o:順序}`。
- 註解在資料區上方有完整欄位說明。

### 每日日報（`daily.html`）
- 新增一天：`const dXXXX = day(前一天, d => {...})`，只改有變動的工作線，插到 `REPORTS` 最前面。
- 時程 `PLAN`：時程版本 11/18；**驗證類工作流 12/11 正式上線是底線**。日期未定寫 `null`（顯示 TBD）。
- 時程狀態以**所選日報日期**為基準，不隨瀏覽當天變動。

### 架構頁
改 `work/2026-11-09_usb-agent-architecture-alignment/outputs/src/build_public_arch.py`（外框）或 `build.py`／`tpl.html`（圖），再執行 `build_public_arch.py` 重產。

## 三、使用者的規則與偏好（必讀）

1. **問使用者一律用互動表單（AskUserQuestion）**。
2. **改 `public/` 先推工作分支＋附截圖，使用者確認「上線」才合併 main。** 紀錄（`work/`）每段結束都同步。
3. **時間未定一律寫「TBD」**。
4. **本週成果**：只列**關鍵成果、最多 4 則**，依重要性排序（目前 Lab Collab Mate → AI Hiring Agent → AAS 系統重構 → InvestGo、PCC）；用詞給**不懂細節的副總**：不用內部術語（例：Bundle→客戶新版軟體）、寫結果與意義。
5. **公司內部文件（PPT 等）只存文字摘要 `inputs/SUMMARY_*.md`，不放原檔。**
6. 版面：總覽首頁桌機**一屏不滾動**（1920／1680／1440）、三欄卡片**底部切齊**；頁面依實際高度自動收緊（寬鬆 → fit1 → fit2）。字體優先**微軟雅黑**；主色深青綠；狀態燈號色（綠／橘／紅／灰）保留。
7. 手機版樣式寫在各頁末尾「手機版（11-19）」段，改桌機時不要動到手機、反之亦然。
8. DRI：AAS＝Tylee；Mac Mini＝萬鋒（不是「万峰」）；Presentation Skill、AI Hiring Agent＝Alyanna；InvestGo、PCC、Development Skill＝Lucas；IDE 串接研究＝Neo。

## 四、驗證腳本（改完必跑）

- `work/2026-11-17_overview-redesign/outputs/src/shot_overview.js`：首頁各寬度溢出、console。
- `.../check_bottoms.js`：三欄底部切齊。
- `.../capacity_overview.js . 30`：壓力測試（每行 30 字）仍單屏。
- `.../shot_daily_full.js`、`check_basedate.js`：日報頁。
- `work/2026-11-19_mobile-readability/outputs/src/shot_mobile.js`：手機可讀性。
- `work/2026-11-19_mobile-readability/outputs/src/desktop_guard.js`：**桌機不變守門**（逐元素比位置／尺寸／樣式；逐像素截圖會偶發不同，不可靠）。

## 五、待辦

- **老闆版面回饋改版（11-19）待確認上線** ← 下一步。見 `work/2026-11-19_boss-layout-feedback/STATUS.md`。改動在工作分支 `claude/gracious-hamilton-cmomxd`，**尚未合併 main**；上線後本檔「一、二」要一起改寫：
  - 首頁：本週成果整塊重點色（CSS 變數 `--hl*`）→ 四個數字獨立一行（`#nums`）→ 模塊卡（標題列改淺色）。一頁收緊多一級 `fit3`。
  - 日報頁：①整體里程碑甘特圖（5 模塊＋共用基礎，`PLAN.groups` 對應首頁 5 個需求）→ ②各模塊執行細節（`MODULES` 定義每張卡的 `lines`／`src`／`items`，同一格式）。甘特圖與卡片都不再收合。
- 每週用 `work/2026-11-17_overview-redesign/outputs/data-template.md` 的訊息範本問負責人，回覆貼來後更新兩頁。
- 未回報需求：產品 Panic 處理、產品測試軟體開發、產品失效分析（皆未開始，預計 12/1、12/14）。
