import sys
out, tpl = sys.argv[1], sys.argv[2]

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

# ---------- shared primitives ----------
def group(x,y,w,h,title,kind="plat",tx=None):
    s = f'<rect class="g-{kind}" x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/>'
    if title:
        cx = tx if tx is not None else x+w/2
        s += f'<text class="gt gt-{kind}" x="{cx}" y="{y+26}" text-anchor="middle">{esc(title)}</text>'
    return s

def chip(x,y,w,h,label,kind="solid",tag=None,size=13):
    cls = {"gap":"c-gap","user":"c-user","comp":"c-comp","stn":"c-stn","dark":"c-dark","new":"c-new"}.get(kind,"c-solid")
    s = f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
    lines = label if isinstance(label,(list,tuple)) else [label]
    n = len(lines); lh = size+4
    y0 = y + h/2 - (n-1)*lh/2 + size*0.36
    tcls = "ct-dark" if kind=="dark" else ("ct-gap" if kind=="gap" else ("ct-new" if kind=="new" else "ct"))
    for i,l in enumerate(lines):
        s += f'<text class="{tcls}" x="{x+w/2}" y="{y0+i*lh}" text-anchor="middle" style="font-size:{size}px">{esc(l)}</text>'
    if tag:
        tw = len(tag)*11+12
        s += f'<rect class="tagr" x="{x+w-tw/2-6}" y="{y-9}" width="{tw}" height="18" rx="9"/><text class="tagt" x="{x+w-6}" y="{y+4}" text-anchor="middle">{esc(tag)}</text>'
    return s

def harrow(x1,x2,y,both=True,kind="flow"):
    hl, sh, hh = 12, 7, 14
    if both:
        pts = [(x1,y),(x1+hl,y-hh),(x1+hl,y-sh),(x2-hl,y-sh),(x2-hl,y-hh),(x2,y),(x2-hl,y+hh),(x2-hl,y+sh),(x1+hl,y+sh),(x1+hl,y+hh)]
    else:
        pts = [(x1,y-sh),(x2-hl,y-sh),(x2-hl,y-hh),(x2,y),(x2-hl,y+hh),(x2-hl,y+sh),(x1,y+sh)]
    return f'<polygon class="ba-{kind}" points="{" ".join(f"{a},{b}" for a,b in pts)}"/>'

def varrow(x,y1,y2,both=True,kind="flow"):
    hl, sh, hh = 12, 7, 14
    if both:
        pts = [(x,y1),(x+hh,y1+hl),(x+sh,y1+hl),(x+sh,y2-hl),(x+hh,y2-hl),(x,y2),(x-hh,y2-hl),(x-sh,y2-hl),(x-sh,y1+hl),(x-hh,y1+hl)]
    else:
        pts = [(x-sh,y1),(x+sh,y1),(x+sh,y2-hl),(x+hh,y2-hl),(x,y2),(x-hh,y2-hl),(x-sh,y2-hl)]
    return f'<polygon class="ba-{kind}" points="{" ".join(f"{a},{b}" for a,b in pts)}"/>'

def cyl(x,y,w,h,lines,kind="solid"):
    cls = {"gap":"cy-gap","new":"cy-new"}.get(kind,"cy")
    ry = 9
    s = f'<path class="{cls}" d="M{x} {y+ry}V{y+h-ry}A{w/2} {ry} 0 0 0 {x+w} {y+h-ry}V{y+ry}A{w/2} {ry} 0 0 0 {x} {y+ry}Z"/>'
    s += f'<path class="{cls}" d="M{x} {y+ry}A{w/2} {ry} 0 0 0 {x+w} {y+ry}"/>'
    tcls = {"gap":"ct-gap","new":"ct-new"}.get(kind,"ct")
    for i,l in enumerate(lines):
        s += f'<text class="{tcls}" x="{x+w/2}" y="{y+h/2+10+i*16-(len(lines)-1)*8}" text-anchor="middle" style="font-size:12.5px">{esc(l)}</text>'
    return s

def person(cx,cy,kind="user"):
    return (f'<circle class="ic-{kind}" cx="{cx}" cy="{cy-14}" r="11"/>'
            f'<path class="ic-{kind}" d="M{cx-20} {cy+20}a20 18 0 0 1 40 0z"/>')

def macmini(cx,cy):
    s = ""
    for dy in (-9,7):
        s += f'<rect class="ic-comp" x="{cx-34}" y="{cy+dy-6}" width="68" height="14" rx="4"/><circle class="ic-dot" cx="{cx+24}" cy="{cy+dy+1}" r="2"/>'
    return s

def station(cx,cy):
    return (f'<rect class="ic-stn" x="{cx-24}" y="{cy-18}" width="48" height="30" rx="3"/>'
            f'<path class="ic-stn" d="M{cx-10} {cy+12}h20v8h-20z"/><path class="ic-stn" d="M{cx-18} {cy+20}h36"/>')

def rowlabel(x,y,w,h,text):
    lines = text if isinstance(text,(list,tuple)) else [text]
    s = f'<rect class="rl" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
    for i,l in enumerate(lines):
        s += f'<text class="rlt" x="{x+w/2}" y="{y+h/2+5+i*17-(len(lines)-1)*8.5}" text-anchor="middle">{esc(l)}</text>'
    return s

def lbl(x,y,text,anchor="middle",cls="al"):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{esc(text)}</text>'

# ---------- Figure 1: overview v7 (three layer bands, guard inside each workflow) ----------
def badge(cx,cy,n,kind="i"):
    return f'<circle class="bd-{kind}" cx="{cx}" cy="{cy}" r="11"/><text class="bdt" x="{cx}" y="{cy+4.5}" text-anchor="middle">{n}</text>'

def sline(d,kind="i"):
    m = {"i":"url(#sah)","u":"url(#sahu)","g":"url(#sahg)"}[kind]
    return f'<path class="sl-{kind}" d="{d}" marker-end="{m}"/>'

SDEFS = '''<defs>
<marker id="sah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="ahp" d="M0 0L10 5L0 10z"/></marker>
<marker id="sahu" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="ahu" d="M0 0L10 5L0 10z"/></marker>
<marker id="sahg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="ahg" d="M0 0L10 5L0 10z"/></marker>
</defs>'''

f = []
f.append(lbl(146,22,"用戶接觸","middle","zone zu"))
f.append(lbl(960,22,"系統內部","middle","zone"))
f.append('<path class="zline zlu" d="M16 30H276"/><path class="zline" d="M300 30H1636"/>')

f.append(group(16,40,100,520,"用戶端","user"))
f.append(group(136,40,140,520,"接入層","user"))
f.append(group(300,40,1062,520,None,"plat"))
f.append('<g transform="translate(16,0)">')
f.append('<text class="gt" x="718" y="66" text-anchor="middle">USB-Agent 平台 · 辦公電腦</text>')

# three bands
f.append('<rect class="band2" x="308" y="80" width="820" height="76" rx="10"/>')
f.append('<rect class="band2" x="308" y="164" width="820" height="136" rx="10"/>')
f.append('<rect class="band2" x="308" y="308" width="820" height="132" rx="10"/>')
f.append(lbl(318,96,"智能體 · 每條工作流一個","start","rowt"))
f.append(lbl(1118,96,"另有 lead 總助理：只聊天、不派發","end","hint"))
f.append(lbl(318,181,"工作流 · 每條內含 AI 產出驗證防線","start","rowt"))
f.append(lbl(1118,181,"需 AI 判斷推理時 →","end","sl"))
f.append(lbl(318,325,"工具 · 專屬工具＋共性工具","start","rowt"))

names = ["Bundle 驗證","EFI 驗證","proxima 驗證","CoreOS Panic","Diags Panic","CoreOS FA","Diags FA","EFI burn-in","EFI diags rel"]
def col(i): return 316 + i*90
for i,n in enumerate(names):
    x = col(i); k = "solid" if i==0 else "gap"
    f.append(chip(x,102,84,44,[n,"agent"],k,size=11))
    # workflow chip with guard block inside
    cls = "c-solid" if i==0 else "c-gap"
    tc = "ct" if i==0 else "ct-gap"
    f.append(f'<rect class="{cls}" x="{x}" y="188" width="84" height="104" rx="8"/>')
    f.append(f'<text class="{tc}" x="{x+42}" y="208" text-anchor="middle" style="font-size:11px">{esc(n)}</text>')
    f.append(f'<text class="{tc}" x="{x+42}" y="224" text-anchor="middle" style="font-size:11px">工作流</text>')
    f.append(f'<rect class="guard" x="{x+6}" y="240" width="72" height="44" rx="6"/>')
    f.append(f'<text class="ct-gap" x="{x+42}" y="258" text-anchor="middle" style="font-size:10.5px">AI 產出</text>')
    f.append(f'<text class="ct-gap" x="{x+42}" y="273" text-anchor="middle" style="font-size:10.5px">驗證防線</text>')
    if i==0:
        f.append(chip(x,330,84,40,["Bundle","專屬工具 ×11"],"solid",size=11))
        f.append(f'<rect class="tagr" x="{x+46}" y="362" width="36" height="16" rx="8"/><text class="tagt" x="{x+64}" y="374" text-anchor="middle">模擬</text>')
    else:
        f.append(chip(x,330,84,40,[n,"專屬工具"],"gap",size=11))

f.append('<rect class="c-gap" x="316" y="378" width="804" height="52" rx="10"/>')
f.append(lbl(328,400,"共性工具","start","sl slg")); f.append(lbl(328,418,"9 條共用","start","hint"))
for i,lab in enumerate(["郵箱","雷達","刷機","Panic","Insight","收集 log"]):
    f.append(chip(412+i*118,386,108,36,lab,"gap",size=12))

# data
f.append(lbl(1118,464,"資料與紀錄","end","rowt"))
for i,(lab,k) in enumerate([(["session.db","事件源"],"solid"),(["運行沙盒","報告 · 日誌"],"solid"),(["審計索引","audit_history"],"solid"),(["知識庫","待確認"],"gap")]):
    f.append(cyl(316+i*200,470,184,76,lab,k))

# link layer
f.append(group(1170,110,160,338,None,"link"))
f.append('<text class="gt gt-link" x="1250" y="132" text-anchor="middle">對外連接層</text>')
f.append(lbl(1250,150,"仍在辦公電腦上","middle","hint"))
f.append('<rect class="g-sub" x="1180" y="164" width="140" height="136" rx="10"/>')
f.append(lbl(1250,184,"往算力電腦","middle","gt-link sub2"))
f.append(chip(1190,194,120,40,["OpenAI 相容","格式請求"],size=11.5))
f.append(lbl(1250,262,"結論回到","middle","hint")); f.append(lbl(1250,278,"驗證防線","middle","hint"))
f.append('<rect class="g-sub" x="1180" y="308" width="140" height="132" rx="10"/>')
f.append(lbl(1250,328,"往產線工站","middle","gt-link sub2"))
f.append(chip(1190,346,120,40,"MCP 協議",size=12.5))

# right column
f.append(group(1420,164,200,136,"算力電腦","comp"))
f.append(chip(1432,196,176,28,"Mac Mini M4 24G ×2","comp",size=11.5))
f.append(chip(1432,230,176,28,"Qwen3.6-35B-A3B","comp",size=11.5))
f.append(chip(1432,264,176,24,"須關閉思考模式","dark",size=11))
f.append(group(1420,308,200,186,"產線工站","stn"))
f.append(chip(1432,341,176,26,"驗證工站 · 刷機、收集 log","stn",size=11.5))
f.append(chip(1432,393,176,26,"Panic 工站 · 已有自動化","stn",size=11.5))
f.append(chip(1432,428,176,24,"工站 MCP 服務（待啟用）","gap",size=11))
f.append(chip(1432,460,176,24,"FA 等工站？","gap",size=11))

f.append("</g>")
# users / access
f.append(person(66,168)); f.append(lbl(66,210,"實驗室","middle","ict")); f.append(lbl(66,226,"工程師","middle","ict"))
f.append(chip(24,262,84,40,["LabMind","A2A 待補"],"gap",size=11.5))
f.append(person(66,500)); f.append(lbl(66,542,"查看結果","middle","ict"))
f.append(chip(148,102,116,44,["對話介面","後端 API"],"user",size=12))
f.append(chip(148,198,116,44,"參數直跑 CLI","user",size=12))
f.append(chip(148,262,116,40,"A2A 對外接口","gap",size=12))
f.append(chip(148,486,116,44,"進度看板 Web","user",size=12))

# story line
f.append(sline("M92 164H120V124H146","u"))
f.append(sline("M92 178H120V220H146","u"))
f.append(sline("M108 282H146","g"))
f.append(sline("M264 124H330","u")); f.append(lbl(288,104,"對話請求","middle","sl slu"))
f.append(sline("M264 220H330","u")); f.append(lbl(288,200,"參數直跑","middle","sl slu"))
f.append('<g transform="translate(16,0)">')
f.append(sline("M1128 214H1188"));
f.append(sline("M1180 270H1130"));
f.append(sline("M1310 214H1418")); f.append(lbl(1364,206,"內網 HTTP","middle","sl"))
f.append(sline("M1128 366H1188"));
f.append(sline("M1320 354H1430")); f.append(lbl(1375,346,"USB 轉網口 ×2","middle","sl")); f.append(lbl(1375,370,"已驗證","middle","hint"))
f.append(sline("M1320 406H1430","g")); f.append(lbl(1375,398,"USB 串口","middle","sl slg")); f.append(lbl(1375,422,"待做","middle","hint"))
f.append("</g>")
f.append(sline("M332 508H266","u")); f.append(lbl(288,548,"SSE 推送","middle","sl slu"))
f.append(sline("M148 508H94","u"));

# base strip
f.append(group(16,580,1620,118,None,"base"))
f.append(rowlabel(32,594,96,40,"框架核心"))
for i,lab in enumerate(["流程註冊表","執行器","Session 服務","事件讀取","LLM 適配器","腳手架"]):
    f.append(chip(142+i*245.3,594,237,40,lab,size=12.5))
f.append(rowlabel(32,644,96,40,"工程保障"))
for i,(lab,k) in enumerate([("配置單一來源","solid"),("契約與架構測試 · 216 例","solid"),("可追溯 · --trace","solid"),("多流程通用測試","gap"),("模型併發排隊","gap")]):
    f.append(chip(142+i*294.4,644,286,40,lab,k,size=12.5))

svg1 = f'<svg viewBox="0 0 1652 712" role="img" aria-label="技術架構全貌：智能體、工作流、工具三層，9 條工作流一一對應且各含 AI 產出驗證防線；工具經 MCP 協議到產線工站，需 AI 判斷時經 OpenAI 相容格式請求到算力電腦">{SDEFS}{"".join(f)}</svg>'

# ---------- Figure P2 variants
# ---------- Figure P2: phase-2 overview (three layer bands, guard inside each workflow) ----------
def _badge_unused(cx,cy,n,kind="i"):
    return f'<circle class="bd-{kind}" cx="{cx}" cy="{cy}" r="11"/><text class="bdt" x="{cx}" y="{cy+4.5}" text-anchor="middle">{n}</text>'

def sline(d,kind="i"):
    m = {"i":"url(#aah)","u":"url(#aahu)","g":"url(#aahg)","n":"url(#aahn)"}[kind]
    return f'<path class="sl-{kind}" d="{d}" marker-end="{m}"/>'

SDEFS = '''<defs>
<marker id="aah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="ahp" d="M0 0L10 5L0 10z"/></marker>
<marker id="aahu" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="ahu" d="M0 0L10 5L0 10z"/></marker>
<marker id="aahg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="ahg" d="M0 0L10 5L0 10z"/></marker>
<marker id="aahn" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="ahn" d="M0 0L10 5L0 10z"/></marker>
</defs>'''


f = []
f.append(lbl(76,22,"用戶","middle","zone"))
f.append(lbl(235,22,"前台","middle","zone zu"))
f.append(lbl(1191,22,"後台 · LabWork（Worker）","middle","zone"))
f.append('<path class="zline" d="M16 30H136"/><path class="zline zlu" d="M150 30H320"/><path class="zline" d="M430 30H1952"/>')

# users
f.append(group(16,40,120,340,"LabMind 用戶","base"))
f.append(chip(26,97,100,34,["公司／客戶系統","工程師 · 其他 Lab"],size=10.5))
f.append(chip(26,176,100,28,"實驗室工程師",size=11))
f.append(chip(26,304,100,28,"主管 / PM",size=11))
f.append(group(16,392,120,164,"後台用戶","base"))
f.append(chip(26,456,100,36,["實驗室工程師","管理者"],size=11))

# front: LabMind
f.append(group(150,40,170,340,"LabMind","user"))
f.append(chip(160,96,150,36,["需求對話 · 預覽","能力卡（Agent Card）"],"user",size=11))
f.append(chip(160,150,150,80,["Kanban 任務領取","領取 · 填參數","退回 · 補問"],"user",size=11))
f.append(chip(160,300,150,36,["進度看板","成果彙整"],"user",size=11))
# front: backend admin platform
f.append(group(150,392,170,164,"後台管理平台","user"))
f.append(chip(160,438,150,28,"工作流與工具管理","new",size=11))
f.append(chip(160,474,150,28,"連線健康","new",size=11))

# LabWork platform container + internals
f.append(group(430,40,1248,520,None,"plat"))
f.append('<text class="gt" x="1050" y="66" text-anchor="middle">USB-Agent 平台 · 辦公電腦</text>')
f.append('<g transform="translate(316,0)">')
f.append('<g transform="translate(16,0)">')

# three bands
f.append('<rect class="band2" x="308" y="80" width="820" height="76" rx="10"/>')
f.append('<rect class="band2" x="308" y="164" width="820" height="136" rx="10"/>')
f.append('<rect class="band2" x="308" y="308" width="820" height="132" rx="10"/>')
f.append(lbl(318,96,"智能體 · 每條工作流一個","start","rowt"))
f.append(lbl(318,181,"工作流 · 每條內含 AI 產出驗證防線","start","rowt"))
f.append(lbl(1118,181,"需 AI 判斷推理時 →","end","sl"))
f.append(lbl(318,325,"工具 · 專屬工具＋共性工具","start","rowt"))

names = ["Bundle 驗證","EFI 驗證","proxima 驗證","CoreOS Panic","Diags Panic","CoreOS FA","Diags FA","EFI burn-in","EFI diags rel"]
def col(i): return 316 + i*90
for i,n in enumerate(names):
    x = col(i); k = "solid" if i==0 else "gap"
    f.append(chip(x,102,84,44,[n,"agent"],k,size=11))
    # workflow chip with guard block inside
    cls = "c-solid" if i==0 else "c-gap"
    tc = "ct" if i==0 else "ct-gap"
    f.append(f'<rect class="{cls}" x="{x}" y="188" width="84" height="104" rx="8"/>')
    f.append(f'<text class="{tc}" x="{x+42}" y="208" text-anchor="middle" style="font-size:11px">{esc(n)}</text>')
    f.append(f'<text class="{tc}" x="{x+42}" y="224" text-anchor="middle" style="font-size:11px">工作流</text>')
    f.append(f'<rect class="guard" x="{x+6}" y="240" width="72" height="44" rx="6"/>')
    f.append(f'<text class="ct-gap" x="{x+42}" y="258" text-anchor="middle" style="font-size:10.5px">AI 產出</text>')
    f.append(f'<text class="ct-gap" x="{x+42}" y="273" text-anchor="middle" style="font-size:10.5px">驗證防線</text>')
    if i==0:
        f.append(chip(x,330,84,40,["Bundle","專屬工具 ×11"],"solid",size=11))
        f.append(f'<rect class="tagr" x="{x+46}" y="362" width="36" height="16" rx="8"/><text class="tagt" x="{x+64}" y="374" text-anchor="middle">模擬</text>')
    else:
        f.append(chip(x,330,84,40,[n,"專屬工具"],"gap",size=11))

f.append('<rect class="c-gap" x="316" y="378" width="804" height="52" rx="10"/>')
f.append(lbl(328,400,"共性工具","start","sl slg")); f.append(lbl(328,418,"9 條共用","start","hint"))
for i,lab in enumerate(["郵箱","雷達","刷機","Panic","Insight","收集 log"]):
    f.append(chip(412+i*118,386,108,36,lab,"gap",size=12))

# data
f.append(lbl(1118,464,"資料與紀錄","end","rowt"))
for i,(lab,k) in enumerate([(["session.db","事件源"],"solid"),(["運行沙盒","報告 · 日誌"],"solid"),(["審計索引","audit_history"],"solid"),(["任務關聯紀錄","任務 ↔ 運行編號"],"new"),(["知識庫","待確認"],"gap")]):
    f.append(cyl(316+i*164,470,150,76,lab,k))

# link layer
f.append(group(1170,110,160,338,None,"link"))
f.append('<text class="gt gt-link" x="1250" y="132" text-anchor="middle">對外連接層</text>')
f.append(lbl(1250,150,"仍在辦公電腦上","middle","hint"))
f.append('<rect class="g-sub" x="1180" y="164" width="140" height="136" rx="10"/>')
f.append(lbl(1250,184,"往算力電腦","middle","gt-link sub2"))
f.append(chip(1190,194,120,40,["OpenAI 相容","格式請求"],size=11.5))
f.append(lbl(1250,262,"結論回到","middle","hint")); f.append(lbl(1250,278,"驗證防線","middle","hint"))
f.append('<rect class="g-sub" x="1180" y="308" width="140" height="132" rx="10"/>')
f.append(lbl(1250,328,"往產線工站","middle","gt-link sub2"))
f.append(chip(1190,346,120,40,"MCP 協議",size=12.5))

# right column
f.append(group(1420,164,200,136,"算力電腦","comp"))
f.append(chip(1432,196,176,28,"Mac Mini M4 24G ×2","comp",size=11.5))
f.append(chip(1432,230,176,28,"Qwen3.6-35B-A3B","comp",size=11.5))
f.append(chip(1432,264,176,24,"須關閉思考模式","dark",size=11))
f.append(group(1420,308,200,186,"產線工站","stn"))
f.append(chip(1432,341,176,26,"驗證工站 · 刷機、收集 log","stn",size=11.5))
f.append(chip(1432,393,176,26,"Panic 工站 · 已有自動化","stn",size=11.5))
f.append(chip(1432,428,176,24,"工站 MCP 服務（待啟用）","gap",size=11))
f.append(chip(1432,460,176,24,"FA 等工站？","gap",size=11))

f.append("</g>")
f.append("</g>")
f.append('<g transform="translate(316,0)">')
f.append('<g transform="translate(16,0)">')
f.append(sline("M1128 214H1188"));
f.append(sline("M1180 270H1130"));
f.append(sline("M1310 214H1418")); f.append(lbl(1364,206,"內網 HTTP","middle","sl"))
f.append(sline("M1128 366H1188"));
f.append(sline("M1320 354H1430")); f.append(lbl(1375,346,"USB 轉網口 ×2","middle","sl")); f.append(lbl(1375,370,"已驗證","middle","hint"))
f.append(sline("M1320 406H1430","g")); f.append(lbl(1375,398,"USB 串口","middle","sl slg")); f.append(lbl(1375,422,"待做","middle","hint"))
f.append("</g>")
f.append("</g>")

# access layer (A2A only) + backend admin (grey) inside platform
f.append(group(442,84,128,296,None,"link"))
f.append('<text class="gt gt-link" x="506" y="104" text-anchor="middle">接入層</text>')
f.append(chip(452,112,108,256,["A2A"],"new",size=16))

# arrows (conditions on arrows)
f.append(sline("M126 114H158","u"))
f.append(sline("M126 190H158","u"))
f.append(sline("M158 318H128","u"))
f.append(sline("M126 474H148","u"))
f.append(sline("M450 122H312","n")); f.append(lbl(384,114,"只列已啟用能力","middle","sl sln"))
f.append(sline("M310 176H450","n")); f.append(lbl(384,168,"人工領取、填好參數","middle","sl sln"))
f.append(sline("M450 212H312","n")); f.append(lbl(384,228,"檢查不過：拒絕或補問","middle","sl sln"))
f.append(sline("M450 318H312","n")); f.append(lbl(384,300,"每完成一個 step","middle","sl sln")); f.append(lbl(384,336,"完成時附成果連結","middle","sl sln"))
f.append(sline("M560 250H638","n")); f.append(lbl(600,242,"參數直跑","middle","sl sln")); f.append(lbl(600,266,"通過檢查才觸發","middle","sl sln"))
f.append(sline("M560 350H612V500H646","n")); f.append(lbl(616,430,"讀寫","start","sl sln")); f.append(lbl(616,444,"紀錄","start","sl sln"))

f.append(sline("M320 474H428","u"))
# base strip
f.append(group(16,580,1936,118,None,"base"))
f.append(rowlabel(32,594,96,40,"框架核心"))
for i,lab in enumerate(["流程註冊表","執行器","Session 服務","事件讀取","LLM 適配器","腳手架"]):
    f.append(chip(142+i*301.7,594,294,40,lab,size=12.5))
f.append(rowlabel(32,644,96,40,"工程保障"))
for i,(lab,k) in enumerate([("配置單一來源","solid"),("契約與架構測試 · 216 例","solid"),("可追溯 · --trace","solid"),("多流程通用測試","gap"),("模型併發排隊","gap")]):
    f.append(chip(142+i*362,644,354,40,lab,k,size=12.5))

svgP2A = f'<svg viewBox="0 0 1968 712" role="img" aria-label="第二階段方案 A：用戶、前台（LabMind 與後台管理平台）、LabWork 平台（內含接入層）">{SDEFS}{"".join(f)}</svg>'

# ---------- Figure P2: phase-2 overview (three layer bands, guard inside each workflow) ----------
def _badge_unused(cx,cy,n,kind="i"):
    return f'<circle class="bd-{kind}" cx="{cx}" cy="{cy}" r="11"/><text class="bdt" x="{cx}" y="{cy+4.5}" text-anchor="middle">{n}</text>'

def sline(d,kind="i"):
    m = {"i":"url(#bah)","u":"url(#bahu)","g":"url(#bahg)","n":"url(#bahn)"}[kind]
    return f'<path class="sl-{kind}" d="{d}" marker-end="{m}"/>'

SDEFS = '''<defs>
<marker id="bah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="ahp" d="M0 0L10 5L0 10z"/></marker>
<marker id="bahu" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="ahu" d="M0 0L10 5L0 10z"/></marker>
<marker id="bahg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="ahg" d="M0 0L10 5L0 10z"/></marker>
<marker id="bahn" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="ahn" d="M0 0L10 5L0 10z"/></marker>
</defs>'''


f = []
f.append(lbl(76,22,"用戶","middle","zone"))
f.append(lbl(235,22,"前台","middle","zone zu"))
f.append(lbl(1249,22,"後台 · LabWork（Worker）","middle","zone"))
f.append('<path class="zline" d="M16 30H136"/><path class="zline zlu" d="M150 30H320"/><path class="zline" d="M430 30H2068"/>')

# users
f.append(group(16,40,120,340,"LabMind 用戶","base"))
f.append(chip(26,97,100,34,["公司／客戶系統","工程師 · 其他 Lab"],size=10.5))
f.append(chip(26,304,100,28,"主管 / PM",size=11))
f.append(group(16,392,120,164,"後台用戶","base"))
f.append(chip(26,456,100,36,["實驗室工程師","管理者"],size=11))

# front: LabMind
f.append(group(150,40,170,340,"LabMind","user"))
f.append(chip(160,96,150,36,["需求對話 · 預覽","能力卡（Agent Card）"],"user",size=11))
f.append(chip(160,150,150,80,["任務派發","人員確認派發"],"user",size=11))
f.append(chip(160,300,150,36,["進度看板","成果彙整"],"user",size=11))
# front: backend admin platform
f.append(group(150,392,170,164,"後台管理平台","user"))
f.append(chip(160,438,150,28,"承接池操作","new",size=11))
f.append(chip(160,474,150,28,"工作流與工具管理","new",size=11))
f.append(chip(160,510,150,28,"連線健康","new",size=11))

# LabWork platform container + internals
f.append(group(430,40,1364,520,None,"plat"))
f.append('<text class="gt" x="1166" y="66" text-anchor="middle">USB-Agent 平台 · 辦公電腦</text>')
f.append('<g transform="translate(432,0)">')
f.append('<g transform="translate(16,0)">')

# three bands
f.append('<rect class="band2" x="308" y="80" width="820" height="76" rx="10"/>')
f.append('<rect class="band2" x="308" y="164" width="820" height="136" rx="10"/>')
f.append('<rect class="band2" x="308" y="308" width="820" height="132" rx="10"/>')
f.append(lbl(318,96,"智能體 · 每條工作流一個","start","rowt"))
f.append(lbl(318,181,"工作流 · 每條內含 AI 產出驗證防線","start","rowt"))
f.append(lbl(1118,181,"需 AI 判斷推理時 →","end","sl"))
f.append(lbl(318,325,"工具 · 專屬工具＋共性工具","start","rowt"))

names = ["Bundle 驗證","EFI 驗證","proxima 驗證","CoreOS Panic","Diags Panic","CoreOS FA","Diags FA","EFI burn-in","EFI diags rel"]
def col(i): return 316 + i*90
for i,n in enumerate(names):
    x = col(i); k = "solid" if i==0 else "gap"
    f.append(chip(x,102,84,44,[n,"agent"],k,size=11))
    # workflow chip with guard block inside
    cls = "c-solid" if i==0 else "c-gap"
    tc = "ct" if i==0 else "ct-gap"
    f.append(f'<rect class="{cls}" x="{x}" y="188" width="84" height="104" rx="8"/>')
    f.append(f'<text class="{tc}" x="{x+42}" y="208" text-anchor="middle" style="font-size:11px">{esc(n)}</text>')
    f.append(f'<text class="{tc}" x="{x+42}" y="224" text-anchor="middle" style="font-size:11px">工作流</text>')
    f.append(f'<rect class="guard" x="{x+6}" y="240" width="72" height="44" rx="6"/>')
    f.append(f'<text class="ct-gap" x="{x+42}" y="258" text-anchor="middle" style="font-size:10.5px">AI 產出</text>')
    f.append(f'<text class="ct-gap" x="{x+42}" y="273" text-anchor="middle" style="font-size:10.5px">驗證防線</text>')
    if i==0:
        f.append(chip(x,330,84,40,["Bundle","專屬工具 ×11"],"solid",size=11))
        f.append(f'<rect class="tagr" x="{x+46}" y="362" width="36" height="16" rx="8"/><text class="tagt" x="{x+64}" y="374" text-anchor="middle">模擬</text>')
    else:
        f.append(chip(x,330,84,40,[n,"專屬工具"],"gap",size=11))

f.append('<rect class="c-gap" x="316" y="378" width="804" height="52" rx="10"/>')
f.append(lbl(328,400,"共性工具","start","sl slg")); f.append(lbl(328,418,"9 條共用","start","hint"))
for i,lab in enumerate(["郵箱","雷達","刷機","Panic","Insight","收集 log"]):
    f.append(chip(412+i*118,386,108,36,lab,"gap",size=12))

# data
f.append(lbl(1118,464,"資料與紀錄","end","rowt"))
for i,(lab,k) in enumerate([(["session.db","事件源"],"solid"),(["運行沙盒","報告 · 日誌"],"solid"),(["審計索引","audit_history"],"solid"),(["任務關聯紀錄","任務 ↔ 運行編號"],"new"),(["知識庫","待確認"],"gap")]):
    f.append(cyl(316+i*164,470,150,76,lab,k))

# link layer
f.append(group(1170,110,160,338,None,"link"))
f.append('<text class="gt gt-link" x="1250" y="132" text-anchor="middle">對外連接層</text>')
f.append(lbl(1250,150,"仍在辦公電腦上","middle","hint"))
f.append('<rect class="g-sub" x="1180" y="164" width="140" height="136" rx="10"/>')
f.append(lbl(1250,184,"往算力電腦","middle","gt-link sub2"))
f.append(chip(1190,194,120,40,["OpenAI 相容","格式請求"],size=11.5))
f.append(lbl(1250,262,"結論回到","middle","hint")); f.append(lbl(1250,278,"驗證防線","middle","hint"))
f.append('<rect class="g-sub" x="1180" y="308" width="140" height="132" rx="10"/>')
f.append(lbl(1250,328,"往產線工站","middle","gt-link sub2"))
f.append(chip(1190,346,120,40,"MCP 協議",size=12.5))

# right column
f.append(group(1420,164,200,136,"算力電腦","comp"))
f.append(chip(1432,196,176,28,"Mac Mini M4 24G ×2","comp",size=11.5))
f.append(chip(1432,230,176,28,"Qwen3.6-35B-A3B","comp",size=11.5))
f.append(chip(1432,264,176,24,"須關閉思考模式","dark",size=11))
f.append(group(1420,308,200,186,"產線工站","stn"))
f.append(chip(1432,341,176,26,"驗證工站 · 刷機、收集 log","stn",size=11.5))
f.append(chip(1432,393,176,26,"Panic 工站 · 已有自動化","stn",size=11.5))
f.append(chip(1432,428,176,24,"工站 MCP 服務（待啟用）","gap",size=11))
f.append(chip(1432,460,176,24,"FA 等工站？","gap",size=11))

f.append("</g>")
f.append("</g>")
f.append('<g transform="translate(432,0)">')
f.append('<g transform="translate(16,0)">')
f.append(sline("M1128 214H1188"));
f.append(sline("M1180 270H1130"));
f.append(sline("M1310 214H1418")); f.append(lbl(1364,206,"內網 HTTP","middle","sl"))
f.append(sline("M1128 366H1188"));
f.append(sline("M1320 354H1430")); f.append(lbl(1375,346,"USB 轉網口 ×2","middle","sl")); f.append(lbl(1375,370,"已驗證","middle","hint"))
f.append(sline("M1320 406H1430","g")); f.append(lbl(1375,398,"USB 串口","middle","sl slg")); f.append(lbl(1375,422,"待做","middle","hint"))
f.append("</g>")
f.append("</g>")

# access layer (A2A only) + backend admin (grey) inside platform
f.append(group(442,84,98,296,None,"link"))
f.append('<text class="gt gt-link" x="491" y="104" text-anchor="middle">接入層</text>')
f.append(chip(450,112,82,256,["A2A"],"new",size=16))

# arrows (conditions on arrows)
f.append(sline("M126 114H158","u"))
f.append(sline("M158 318H128","u"))
f.append(sline("M126 474H148","u"))
f.append(sline("M450 122H312","n")); f.append(lbl(384,114,"只列已啟用能力","middle","sl sln"))
f.append(sline("M310 176H450","n")); f.append(lbl(384,168,"人員確認派發後推送","middle","sl sln"))
f.append(sline("M450 212H312","n")); f.append(lbl(384,228,"回覆接受（附工作編號）","middle","sl sln")); f.append(lbl(384,240,"或拒絕附原因 · 補問","middle","sl sln"))
f.append(sline("M450 318H312","n")); f.append(lbl(384,300,"每完成一個 step","middle","sl sln")); f.append(lbl(384,336,"完成時附成果連結","middle","sl sln"))
# acceptance pool between access layer and bands
f.append('<rect class="c-new" x="596" y="112" width="110" height="218" rx="10"/>')
f.append(lbl(651,138,"承接池","middle","ct-new sub2"))
for k,(yy,lab) in enumerate([(166,"待承接"),(196,"已接受"),(226,"已拒絕"),(256,"待補資料")]):
    f.append(chip(606,yy-14,90,24,lab,size=11))
f.append(sline("M532 190H594","n")); f.append(lbl(563,182,"放入","middle","sl sln"))
f.append(sline("M596 236H534","n")); f.append(lbl(563,252,"確認結果","middle","sl sln"))
f.append(sline("M706 270H754","n")); f.append(lbl(730,262,"參數直跑","middle","sl sln")); f.append(lbl(730,286,"接受後觸發","middle","sl sln"))
f.append(sline("M320 474H428","u"))
f.append(sline("M532 350H740V500H762","n")); f.append(lbl(744,430,"讀寫","start","sl sln")); f.append(lbl(744,444,"紀錄","start","sl sln"))

# base strip
f.append(group(16,580,2052,118,None,"base"))
f.append(rowlabel(32,594,96,40,"框架核心"))
for i,lab in enumerate(["流程註冊表","執行器","Session 服務","事件讀取","LLM 適配器","腳手架"]):
    f.append(chip(142+i*321,594,313,40,lab,size=12.5))
f.append(rowlabel(32,644,96,40,"工程保障"))
for i,(lab,k) in enumerate([("配置單一來源","solid"),("契約與架構測試 · 216 例","solid"),("可追溯 · --trace","solid"),("多流程通用測試","gap"),("模型併發排隊","gap")]):
    f.append(chip(142+i*385,644,377,40,lab,k,size=12.5))

svgP2B = f'<svg viewBox="0 0 2084 712" role="img" aria-label="第二階段方案 B：用戶、前台（LabMind 與後台管理平台）、LabWork 平台（內含接入層）">{SDEFS}{"".join(f)}</svg>'

# ---------- Figure 2: swimlane (kept) ----------
def box(x,y,w,h,title,lines=(),kind="solid",tag=None):
    cls = {"gap":"c-gap","user":"c-user"}.get(kind,"c-solid")
    s = f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>'
    s += f'<text class="tt" x="{x+14}" y="{y+23}">{esc(title)}</text>'
    for i,l in enumerate(lines):
        s += f'<text class="ts" x="{x+14}" y="{y+42+i*16}">{esc(l)}</text>'
    if tag:
        tw = len(tag)*11+12
        s += f'<rect class="tagr" x="{x+w-tw-8}" y="{y+8}" width="{tw}" height="18" rx="9"/><text class="tagt" x="{x+w-8-tw/2}" y="{y+21}" text-anchor="middle">{esc(tag)}</text>'
    return s

def arrow(d,kind="int",label=None,lx=0,ly=0,anchor="start"):
    c = {"int":"ar","gap":"ar gapar","user":"ar userar"}[kind]
    m = {"int":"url(#bah)","gap":"url(#bahg)","user":"url(#bahu)"}[kind]
    s = f'<path class="{c}" d="{d}" marker-end="{m}"/>'
    if label:
        lc = "al ual" if kind=="user" else "al"
        s += f'<text class="{lc}" x="{lx}" y="{ly}" text-anchor="{anchor}">{esc(label)}</text>'
    return s

DEFS = '''<defs>
<marker id="bah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ahp" d="M0 0L10 5L0 10z"/></marker>
<marker id="bahg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ahg" d="M0 0L10 5L0 10z"/></marker>
<marker id="bahu" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ahu" d="M0 0L10 5L0 10z"/></marker>
</defs>'''

def col(i): return 130 + (i-1)*186
W = 170
s = []
s.append('<rect class="g-user" x="20" y="20" width="1220" height="150" rx="14"/><text class="lane" x="34" y="92">實驗室</text><text class="lane" x="34" y="112">工程師</text>')
s.append('<rect class="g-plat" x="20" y="190" width="1220" height="345" rx="14"/><text class="lane" x="34" y="370">系統內部</text>')
s.append(box(col(1),62,W,86,"① 選擇工作流",["對話：找對應 agent","CLI：指定流程"],"user"))
s.append(box(col(2),62,W,86,"② 提供參數",["依工作流而不同","例：機台號、版本"],"user"))
s.append(box(col(3),62,W,86,"或由 LabMind 呼叫",["A2A 接口待補"],"gap"))
s.append(box(col(4),62,col(5)+W-col(4),86,"③ 看即時進度",["看板逐步顯示每個 step 的狀態","出問題時用 --trace 追查完整紀錄"],"user"))
s.append(box(col(6),62,W,86,"④ 拿到結果",["報告與結論","PASS／WARNING／FAIL"],"user"))
s.append(box(col(4),214,col(5)+W-col(4),56,"事件流（ADK session）",["每個 step 結束就寫入，後端用 SSE 推送"]))
s.append(box(col(2),312,W,96,"確認參數",["缺必填就反問","照原話使用，不改寫"]))
s.append(box(col(3),312,W,96,"建立運行資料夾",["每次測試一個資料夾","logs/workflow/<流程>/"]))
s.append(box(col(4),312,W,96,"依序執行 step",["各流程 5–8 個 step","順序固定"]))
s.append(box(col(5),312,W,96,"需判斷的 step",["呼叫模型研判","結論直出"]))
s.append(box(col(6),312,W,96,"產出報告",["reports/ · audit.json","全程留痕可追溯"]))
s.append(box(col(4),452,W,64,"工具",["本機或工站執行"],tag="模擬"))
s.append(box(col(5),452,W,64,"模型服務",["Mac Mini ×2"]))
s.append(box(col(6),452,W,64,"判定防線",["待決策"],"gap"))
s.append(arrow(f"M{col(1)+W} 105H{col(2)-2}","user"))
s.append(arrow(f"M{col(2)+85} 148V308","user",label="送出請求",lx=col(2)+91,ly=186))
s.append(arrow(f"M{col(3)+85} 148V292H{col(2)+150}V308","gap"))
for a,b in [(2,3),(3,4),(4,5),(5,6)]:
    s.append(arrow(f"M{col(a)+W} 360H{col(b)-2}"))
s.append(arrow(f"M{col(4)+85} 312V274",label="寫入",lx=col(4)+91,ly=298))
s.append(arrow(f"M{col(5)+85} 312V274",label="寫入",lx=col(5)+91,ly=298))
mid45 = (col(4)+W+col(5))//2
s.append(arrow(f"M{mid45} 214V152","user",label="SSE 推送",lx=mid45+6,ly=186))
s.append(arrow(f"M{col(6)+85} 312V152","user",label="交付結果",lx=col(6)+79,ly=236,anchor="end"))
s.append(arrow(f"M{col(4)+85} 408V448"))
s.append(arrow(f"M{col(5)+85} 408V448"))
s.append(arrow(f"M{col(6)+85} 452V412","gap"))
svg2 = f'<svg viewBox="0 0 1250 545" role="img" aria-label="9 條工作流共用的執行流程：上排用戶操作，下排系統內部執行">{DEFS}{"".join(s)}</svg>'

# ---------- Figure 3: deployment (left → right) ----------
g = []
g.append(lbl(445,22,"辦公網段","middle","zone"))
g.append(lbl(1190,22,"產線側","middle","zone"))
g.append('<path class="zline" d="M20 30H870"/><path class="zline" d="M1000 30H1380"/>')
g.append(group(20,40,300,380,"算力電腦 · 只做推理","comp"))
g.append(macmini(170,100))
for i,(lab,k) in enumerate([("Mac Mini M4 24G ×2","comp"),("雷電線串接成集群","comp"),("Qwen3.6-35B-A3B","comp"),("OpenAI 相容 API","comp")]):
    g.append(chip(40,134+i*56,260,44,lab,k))
g.append(chip(40,362,260,36,"須關閉思考模式","dark",size=12))

g.append(harrow(324,446,200))
g.append(lbl(385,176,"辦公區網 HTTP")); g.append(lbl(385,234,"不經公網","middle","hint"))

g.append(group(450,40,420,380,"辦公電腦 · 控制平面","plat"))
items = [("後端 API :8000","solid"),("進度看板","solid"),("9 個 agent","solid"),(["9 條工作流","目前 1 條"],"solid"),("logs/ 運行沙盒","solid"),("session.db","solid"),(["本機工具","郵箱 · 雷達 · Insight？"],"gap"),("A2A 對外接口","gap")]
for i,(lab,k) in enumerate(items):
    r,c = divmod(i,2)
    g.append(chip(470+c*195,80+r*82,185,66,lab,k))

g.append(harrow(874,996,150))
g.append(lbl(935,126,"USB 轉網口 ×2")); g.append(lbl(935,184,"已驗證刷機","middle","hint"))
g.append(harrow(874,996,330,kind="gapflow"))
g.append(lbl(935,306,"USB 串口")); g.append(lbl(935,364,"待實作 · 優先級低","middle","hint"))

g.append(group(1000,40,380,380,"產線工站","stn"))
g.append(station(1060,108)); g.append(lbl(1100,104,"驗證工站","start","sub"))
g.append(chip(1016,140,170,44,["Bundle · EFI","proxima 驗證"],"stn",size=12))
g.append(chip(1194,140,170,44,"刷機 · 收集 log","stn",size=12.5))
g.append(chip(1016,192,348,34,"工站 MCP 服務（待啟用）","gap",size=12.5))
g.append(station(1060,282)); g.append(lbl(1100,278,"Panic 工站","start","sub"))
g.append(chip(1016,312,170,44,["CoreOS · Diags","Panic"],"stn",size=12))
g.append(chip(1194,312,170,44,"現場已有自動化","stn",size=12.5))
g.append(chip(1016,364,348,34,"Agent 操作，或只讀取結果？","gap",size=12.5))

g.append(varrow(660,420,456,kind="gapflow"))
g.append(chip(510,458,300,50,["LabMind","透過 A2A 呼叫工作流"],"gap",size=12.5))
g.append(chip(1016,458,348,50,["FA · burn-in · diags rel 工站？","連線方式待確認"],"gap",size=12.5))
svg3 = f'<svg viewBox="0 0 1400 520" role="img" aria-label="部署示意：算力電腦、辦公電腦、產線工站由左至右，虛線為待補齊或待確認">{"".join(g)}</svg>'

html = open(tpl,encoding="utf-8").read().replace("%%SVG1%%",svg1).replace("%%SVGP2A%%",svgP2A).replace("%%SVGP2B%%",svgP2B).replace("%%SVG2%%",svg2).replace("%%SVG3%%",svg3)
open(out,"w",encoding="utf-8").write(html)
