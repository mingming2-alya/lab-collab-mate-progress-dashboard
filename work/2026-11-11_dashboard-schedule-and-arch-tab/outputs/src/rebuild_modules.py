import re
p='public/index.html'; t=open(p,encoding='utf-8').read()
L=t.split('\n')
style_end=t.index('</style>')
css=t[t.index('<style>')+7:style_end]
plan=t[t.index('/* 整體時程。'):t.index('const SCOPE = [')]
data=t[t.index('/* 每條工作線一筆'):t.index('const LABEL = ')]
# wording
for a,b in [("連續 5 次穩定跑通","正式數據連續 5 次穩定跑通全流程"),("真機連續 5 次穩定跑通","正式數據連續 5 次穩定跑通全流程")]:
    plan=plan.replace(a,b)
plan=plan.replace("真機正式數據連續","正式數據連續")
plan=plan.replace("、失敗時有看得懂的錯誤訊息","、失敗時有看得懂的錯誤訊息")
data=data.replace('title:"Insight 沒有可用的 API",','mod:"開發、FA", title:"Insight 沒有可用的 API",')
css=css.replace("/* Layout: one column. Tabs → status tally → overall schedule (track summary cards + gantt) →",
 "/* Layout: one column. Tabs → tally → one card per module (schedule + today's progress merged) → collapsible full gantt. Older rules kept below where reused:")
css+=r"""
/* module cards (schedule + progress merged) */
.mods{display:flex;flex-direction:column;gap:12px}
.rule{margin:0;font-size:13px;color:var(--muted);border-left:3px solid var(--accent);padding-left:10px}
.sched{display:flex;flex-direction:column;gap:2px;font-size:14px;background:var(--bg);border-radius:8px;padding:8px 12px}
.sched .lbl{font-size:12px;color:var(--muted);font-weight:700;letter-spacing:.06em}
.sched b.mono{font-size:15px}
.sched .dim{color:var(--muted);font-size:13px}
.prog{display:flex;flex-direction:column;gap:4px;margin:0;font-size:15px;max-width:72ch}
.prog b{margin-right:6px}
.mrows{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:8px}
.mrow{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1.25fr);gap:4px 14px;padding:8px 12px;border-top:1px solid var(--line);align-items:center;font-size:14px}
.mrow.two{grid-template-columns:minmax(0,1fr) auto}
.mrow:first-child{border-top:0}
.mrow .nm{font-weight:700;min-width:0}
.mrow .nm small{display:block;font-weight:400;color:var(--muted);font-size:12px}
.mrow .nm i{font-style:normal;font-size:11px;font-weight:700;color:var(--new);background:var(--new-soft);padding:0 6px;border-radius:4px;margin-left:6px;vertical-align:1px}
.mrow .nx{font-size:13px;color:var(--muted);min-width:0}
.mrow .nx b{color:var(--fg)}
.livepill{font-size:12px;font-weight:700;color:var(--ok);background:var(--ok-soft);padding:2px 8px;border-radius:4px;white-space:nowrap}
.card[data-s="idle"] .prog{color:var(--muted)}
.gbox > summary.donehd{display:flex;align-items:baseline;gap:10px;padding:0}
.gbox[open] > summary .chev{transform:rotate(90deg)}
.gbox[open] .hint{display:none}
.gbox .gwrap{margin-top:12px}
@media (max-width:520px){
  .mrow{grid-template-columns:minmax(0,1fr) auto}
  .mrow .nx{grid-column:1 / -1}
}
"""
html_body = r"""<body>

<div class="wrap">
  <header class="page">
    <nav class="tabs" aria-label="頁面"><a href="./" aria-current="page">每日進度</a><a href="arch.html">架構全貌</a></nav>
    <div class="eyebrow">LAB COLLAB MATE ・ 專案進度日報</div>
    <div class="top">
      <h1 id="h1">每日進度</h1>
      <label class="pick"><span>查看日期</span><select id="date"></select></label>
    </div>
    <div class="tally" id="tally"></div>
  </header>

  <section aria-labelledby="s1">
    <h2 id="s1">各模塊進展 <span class="count" id="c1"></span></h2>
    <p class="rule" id="rule"></p>
    <div class="mods" id="mods"></div>
  </section>

  <section aria-labelledby="s2">
    <details class="gbox" id="gbox">
      <summary class="donehd"><h2 id="s2">完整時程 <span class="count" id="c2"></span></h2><span class="chev" aria-hidden="true">›</span><span class="hint">點擊展開甘特圖</span></summary>
      <div class="gwrap"><div class="glegend"><span><i style="background:var(--accent)"></i>開發・串連・設計</span><span><i style="background:var(--ok)"></i>用戶 Try Run</span><span><i style="background:var(--idle-soft);border:1px solid var(--idle)"></i>已過</span><span><i style="border:1px dashed var(--idle)"></i>時程待定</span><span><i class="k" style="border-radius:50%;box-shadow:inset 0 0 0 2px var(--fg)"></i>正式數據首次跑通全流程</span><span><i class="k" style="border-radius:50%;background:var(--fg)"></i>正式數據連續 5 次穩定跑通全流程</span><span><i class="k" style="background:var(--warn);transform:rotate(45deg) scale(.85)"></i>判斷點／定案</span><span><i class="k" style="background:var(--ok);transform:rotate(45deg) scale(.85)"></i>正式上線（用戶驗收）</span><span style="color:var(--bad)">｜今天</span></div><div class="gantt" id="gantt"></div></div>
    </details>
  </section>

  <footer>
    <span>資料來源：工程師當日回報訊息，由 PM 彙整。「排程」依 PM 規劃的時程版本，剩餘天數依瀏覽當天計算；其餘內容依所選日期的日報。</span>
    <span>燈號：● 正常＝依計畫推進；▲ 注意＝有延誤可能，團隊可自行處理；■ 受阻＝需要外部協助；○ 未啟動＝尚未開工，非異常。</span>
    <span>「今日更新」＝與前一份日報相比有變動。</span>
  </footer>
</div>

<script>
"""
logic = r"""const LABEL = {done:"✓ 已完成", green:"● 正常", yellow:"▲ 注意", red:"■ 受阻", idle:"○ 未啟動"};
const TAG = {decide:"需決策", risk:"待追蹤", handled:"已有對策"};
const $ = id => document.getElementById(id);
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const key = d => "d" + d.replaceAll("-","");
const wk = d => "日一二三四五六"[new Date(d+"T00:00:00").getDay()];
const md = d => d.slice(5).replace("-","/");
const issueHTML = x => `<div class="issue ${x.type}"><span class="k">${TAG[x.type]}</span><div class="v"><div class="t">${esc(x.title)}</div><div class="ask">${esc(x.ask)}</div></div></div>`;

/* 模塊＝日報的呈現單位，對應整體時程。src＝整條工作線的進展原話；rows＝工作線裡的單項（工具），track＝對應 PLAN 的時程線。
   工作線 06 Try Run、05 工作流建置已由時程裡的里程碑取代，不再單獨顯示。 */
const MODULES = [
  {name:"環境與框架", track:"環境與框架", src:[{ws:1, label:"本地模型"}, {ws:2, label:"ADK 框架"}]},
  {name:"驗證", rows:[{ws:4, item:"Bundle 驗證", track:"Bundle 驗證"}, {ws:4, item:"proxima 驗證", track:"proxima 驗證"}, {ws:4, item:"EFI 驗證", track:"EFI 驗證"}]},
  {name:"共性工具", note:"各工作流共用；刷機需在 Bundle 首次跑通前（11/18）可用", rows:[{ws:3, item:"郵箱"}, {ws:3, item:"雷達"}, {ws:3, item:"刷機"}, {ws:3, item:"收集 log"}]},
  {name:"Panic", rows:[{ws:3, item:"Panic", label:"Panic 工具", track:"Panic"}]},
  {name:"開發、FA", rows:[{ws:3, item:"Insight", label:"Insight 工具（FA 用）", track:"開發、FA"}]},
  {name:"LabMind 串連", track:"LabMind 串連", src:[{ws:7}]}
];
const HOME = {1:"環境與框架", 2:"環境與框架", 3:"共性工具", 4:"驗證", 5:"驗證", 6:"驗證", 7:"LabMind 串連"};
const RANK = {red:4, yellow:3, green:2, done:1, idle:0};

/* 從某天的日報算出模塊內容 */
function modOf(r, M){
  const P = no => r.projects.find(p => p.no === no);
  const lines = (M.src||[]).map(s => { const p = P(s.ws); return {label:s.label, text:p.update, status:p.status, owners:p.owners||"", next:p.next, eta:p.eta}; });
  const rows = (M.rows||[]).map(s => { const p = P(s.ws); const it = (p.items||[]).find(i => i[0] === s.item) || [s.item, "—"];
    return {...s, owner:it[1], lab:it[2] || "未開始", k:it[3] || "todo", status: it[3] && it[3] !== "todo" ? p.status : "idle"}; });
  const issues = r.projects.flatMap(p => (p.issues||[]).filter(x => (x.mod || HOME[p.no]) === M.name));
  const sts = [...lines, ...rows].map(x => x.status);
  const status = sts.every(s => s === "done") ? "done" : sts.reduce((a,b) => RANK[b] > RANK[a] ? b : a, "idle");
  const owners = [...new Set([...lines.flatMap(l => l.owners.split("、")), ...rows.flatMap(x => x.owner.split("、"))].filter(o => o && o !== "—"))].join("、");
  const sig = JSON.stringify([lines.map(l => [l.text, l.status]), rows.map(x => [x.lab, x.k]), issues.map(x => x.title + x.ask)]);
  return {lines, rows, issues, status, owners, sig};
}
function lastChange(idx, M){
  for (let i = idx; i < REPORTS.length-1; i++) if (modOf(REPORTS[i], M).sig !== modOf(REPORTS[i+1], M).sig) return REPORTS[i].date;
  return REPORTS[REPORTS.length-1].date;
}

/* ---- 時程計算 ---- */
const dn = s => Date.UTC(+s.slice(0,4), +s.slice(5,7)-1, +s.slice(8,10)) / 864e5;
const mdd = s => `${+s.slice(5,7)}/${+s.slice(8,10)}`;
const rng = x => x.s ? (x.e ? `${mdd(x.s)}–${mdd(x.e)}` : `${mdd(x.s)} 起・結束待定`) : "時程待定";
const t0 = new Date(), TODAY = Date.UTC(t0.getFullYear(), t0.getMonth(), t0.getDate()) / 864e5;
const left = d => d === TODAY ? "今天" : d > TODAY ? `剩 ${d - TODAY} 天` : `已過 ${TODAY - d} 天`;
const TRACK = name => PLAN.tracks.find(tr => tr.name === name);
function trackInfo(tr){
  const st = tr.steps;
  const cur = st.filter(x => x.s && dn(x.s) <= TODAY && TODAY <= dn(x.e));
  const last = cur.length ? st.indexOf(cur[cur.length-1]) : -1;
  const nxt = st.find((x,i) => i > last && !(x.s && dn(x.s) <= TODAY));
  const allPast = !cur.length && st.every(x => x.s && dn(x.e) < TODAY);
  const nx = cur.length || allPast ? nxt : st[st.indexOf(nxt)+1];
  const ms = [...(tr.ms||[]), ...st.flatMap(x => x.ms||[])].sort((a,b) => dn(a[0]) - dn(b[0]));
  return {cur, nxt, nx, allPast, m: ms.find(m => dn(m[0]) >= TODAY), live: ms.find(m => m[2] === "live")};
}
function schedHTML(tr){
  const I = trackInfo(tr), out = [];
  if (I.cur.length) I.cur.forEach(x => out.push(`<div>現在：<b>${esc(x.n)}</b>　ETA <b class="mono">${mdd(x.e)}</b> <span class="dim">（${left(dn(x.e))}）</span></div>`));
  else if (I.allPast) out.push(`<div><b>依計畫已結束</b></div>`);
  else if (I.nxt) out.push(`<div>${I.nxt.s ? `<b class="mono">${mdd(I.nxt.s)}</b> 開始` : "時程待定"}：<b>${esc(I.nxt.n)}</b>${I.nxt.s ? ` <span class="dim">（${dn(I.nxt.s) - TODAY} 天後）</span>` : ""}</div>`);
  if (I.m) out.push(`<div>下一個里程碑：<b>${esc(I.m[1])}</b>　<b class="mono">${mdd(I.m[0])}</b> <span class="dim">（${left(dn(I.m[0]))}）${I.m[3] ? "　" + esc(I.m[3]) : ""}</span></div>`);
  if (I.nx) out.push(`<div class="dim">下一階段：${esc(I.nx.n)}（${rng(I.nx)}）</div>`);
  return `<div class="sched"><span class="lbl">排程</span>${out.join("")}</div>`;
}
function rowNext(tr){
  const I = trackInfo(tr);
  const now = I.cur.length ? `${esc(I.cur[0].n)}・ETA ${mdd(I.cur[0].e)}` : I.nxt && I.nxt.s ? `${mdd(I.nxt.s)} 開始` : "";
  return `<span class="nx">${I.m ? `下一個里程碑：<b>${esc(I.m[1])}</b> <b class="mono">${mdd(I.m[0])}</b>` : ""}${now ? `<br>${now}` : ""}</span>`;
}

function render(){
  const idx = Math.max(0, REPORTS.findIndex(x => key(x.date) === location.hash.slice(1)));
  const r = REPORTS[idx], prev = REPORTS[idx+1];
  const [, m, d] = r.date.split("-");
  $("h1").textContent = `${+m} 月 ${+d} 日進度`;
  $("date").innerHTML = REPORTS.map((x,i) => `<option value="${key(x.date)}"${i===idx?" selected":""}>${x.date}（${wk(x.date)}）${i===0?"・最新":""}</option>`).join("");

  const mods = MODULES.map(M => {
    const cur = modOf(r, M), was = prev && modOf(prev, M);
    return {M, ...cur, changed: !!was && was.sig !== cur.sig, was, last: lastChange(idx, M)};
  });
  const n = s => mods.filter(x => s.includes(x.status)).length;
  const nDecide = mods.flatMap(x => x.issues).filter(x => x.type === "decide").length;
  $("tally").innerHTML = `<span>進行中<b>${n(["green","yellow","red"])}</b></span><span>未啟動<b>${n(["idle"])}</b></span><span>已完成<b>${n(["done"])}</b></span><span class="${nDecide?"hot":""}">需老闆決策<b>${nDecide}</b></span>`;
  $("c1").textContent = `${mods.length} 個模塊`;
  $("rule").textContent = PLAN.rule;

  $("mods").innerHTML = mods.map(x => {
    const M = x.M, lives = [...new Set((M.rows||[]).filter(s => s.track).map(s => trackInfo(TRACK(s.track)).live).filter(Boolean).map(l => l[0]))];
    const rowChanged = s => x.was && (() => { const w = x.was.rows.find(y => y.item === s.item); return w && (w.lab !== s.lab || w.k !== s.k); })();
    return `<article class="card" data-s="${x.status}">
      <div class="hd"><h3>${esc(M.name)}</h3>
        ${lives.length ? `<span class="livepill">◆ 上線 ${lives.map(mdd).join("、")}</span>` : ""}
        ${x.changed ? `<span class="badge new">今日更新</span>` : `<span class="badge same">今日無變動</span>`}
        <span class="pill">${LABEL[x.status]}</span></div>
      ${M.track ? schedHTML(TRACK(M.track)) : ""}
      ${x.lines.length ? `<div class="prog">${x.lines.map(l => `<div>${x.lines.length > 1 ? `<b>${esc(l.label)}</b>` : ""}${esc(l.text)}</div>`).join("")}</div>` : ""}
      ${x.lines.filter(l => l.next).map(l => `<dl class="kv"><dt>下一步</dt><dd>${esc(l.next)}</dd><dt>預計時間</dt><dd>${l.eta ? esc(l.eta) : `<em class="tbd">待工程師回報</em>`}</dd></dl>`).join("")}
      ${M.note ? `<div class="sched"><span class="dim">${esc(M.note)}</span></div>` : ""}
      ${x.rows.length ? `<div class="mrows">${x.rows.map(s => `<div class="mrow${s.track ? "" : " two"}">
          <span class="nm">${esc(s.label || s.item)}${rowChanged(s) ? `<i>更新</i>` : ""}<small>${esc(s.owner)}</small></span>
          <span class="st ${s.k}">${esc(s.lab)}</span>${s.track ? rowNext(TRACK(s.track)) : ""}</div>`).join("")}</div>` : ""}
      ${x.issues.map(issueHTML).join("")}
      <div class="foot"><span>負責人：${esc(x.owners || "—")}</span><span>最後更新：<span class="mono">${md(x.last)}</span></span></div>
    </article>`;
  }).join("");
}

/* ---- 甘特圖 ---- */
function renderGantt(){
  const A = dn(PLAN.from), span = PLAN.weeks * 7, pct = d => ((d - A) / span * 100).toFixed(3) + "%";
  const pctEnd = d => ((d + 1 - A) / span * 100).toFixed(3) + "%";
  const pctMid = d => ((d + .5 - A) / span * 100).toFixed(3) + "%";
  const inAxis = TODAY >= A && TODAY < A + span;
  $("c2").textContent = `時程版本 ${mdd(PLAN.updated)}`;
  const todayEl = inAxis ? `<span class="today" style="left:${pct(TODAY)}"></span>` : "";
  let ticks = "";
  for (let w = 0; w < PLAN.weeks; w++) { const x = new Date((A + w*7) * 864e5); ticks += `<span class="wk" style="left:${pct(A+w*7)}">${x.getUTCMonth()+1}/${x.getUTCDate()}</span>`; }
  for (let d = A; d < A + span; d++) { const x = new Date(d * 864e5);
    if (x.getUTCDate() === 1 || d === A) ticks += `<span class="mo" style="left:${pct(d)}">${x.getUTCFullYear()!==2026?x.getUTCFullYear()+" 年 ":""}${x.getUTCMonth()+1} 月</span>`; }
  if (inAxis) ticks += `<span class="todayl" style="left:${pct(TODAY)}">今天 ${t0.getMonth()+1}/${t0.getDate()}</span>${todayEl}`;
  const bar = x => {
    if (!x.s) return `<span class="bar tbdbar" title="${esc(x.n)}">時程待定</span>`;
    const st = dn(x.e) < TODAY ? "past" : (dn(x.s) <= TODAY ? "now" : "");
    return `<span class="bar ${x.kind} ${st}" style="left:${pct(dn(x.s))};width:calc(${pctEnd(dn(x.e))} - ${pct(dn(x.s))})" title="${esc(x.n)}　${rng(x)}">${esc(x.short ?? rng(x))}</span>`;
  };
  const mark = ([d, txt, k, more]) => `<span class="mk ${k}" style="left:${pctMid(dn(d))}" title="${mdd(d)}　${esc(txt)}${more?"："+esc(more):""}"></span>` +
    (k === "live" ? `<span class="msl" style="left:${pctMid(dn(d))}">上線 ${mdd(d)}</span>` : "");
  const row = (label, sub, steps, ms) => `<div class="grow"><div class="lb">${esc(label)}${sub?`<small>${esc(sub)}</small>`:""}</div>
    <div class="trk" style="--wks:${PLAN.weeks}">${steps.map(bar).join("")}${(ms||[]).map(mark).join("")}${todayEl}</div></div>`;
  $("gantt").innerHTML = `<div class="gax"><span></span><div class="ticks">${ticks}</div></div>` +
    PLAN.groups.map((g, gi) => `<div class="ghd"><span>${esc(g.name)}</span><span class="gn">${esc(g.note||"")}</span></div>` +
      PLAN.tracks.filter(tr => tr.group === gi).map(tr => tr.row === "each"
        ? tr.steps.map(x => row(x.n, x.sub, [x], x.ms)).join("")
        : row(tr.label || tr.name, tr.sub, tr.steps, tr.ms)).join("")).join("");
}

/* 甘特圖展開狀態只記在本機瀏覽器 */
try { if (localStorage.getItem("ganttOpen") === "1") $("gbox").open = true; } catch(e) {}
$("gbox").addEventListener("toggle", () => { try { localStorage.setItem("ganttOpen", $("gbox").open ? "1" : "0"); } catch(e) {} });
addEventListener("hashchange", render);
$("date").addEventListener("change", e => { location.hash = e.target.value; });
renderGantt();
render();
</script>
</body>
</html>
"""
head = t[:t.index('<style>')+7]
out = head + css + "</style>\n</head>\n" + html_body + plan + data + logic
open(p,'w',encoding='utf-8').write(out)
print(len(out))
