"""從架構全貌頁（lcm-architecture.html）抽出三張全貌圖，產生日報網站的「架構全貌」分頁 public/arch.html。

只取：第一階段全貌、第二階段方案 A、方案 B。泳道圖、部署示意、待補齊清單不放上日報網站。
用法（在 repo 根目錄）：python3 work/2026-11-09_usb-agent-architecture-alignment/outputs/src/build_public_arch.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
SRC = ROOT / "work/2026-11-09_usb-agent-architecture-alignment/outputs/lcm-architecture.html"
OUT = ROOT / "public/arch.html"

t = SRC.read_text(encoding="utf-8")
style = re.search(r"<style>(.*?)</style>", t, re.S).group(1)
legend = re.search(r'<div class="legend">.*?</div>', t, re.S).group(0)
body = t[t.index('<section aria-labelledby="h-arch">'):t.index('<section aria-labelledby="h-flow">')]
# 日報分頁不需要「一、二、」章節編號
body = body.replace("一、第一階段技術架構全貌", "第一階段技術架構全貌").replace("二、第二階段技術架構全貌", "第二階段技術架構全貌")

TABS_CSS = """
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--line);margin-bottom:-8px}
.tabs a{font-size:14px;font-weight:700;color:var(--muted);text-decoration:none;padding:8px 14px;border-bottom:3px solid transparent;margin-bottom:-1px}
.tabs a:hover{color:var(--fg)}
.tabs a[aria-current="page"]{color:var(--fg);border-bottom-color:var(--user)}
.tabs a:focus-visible{outline:2px solid var(--user);outline-offset:2px;border-radius:4px}
.note-src{font-size:12px;color:var(--muted)}
/* 統一風格（與總覽、每日進度頁一致）：礦物暖紙底、深松青主色、微軟雅黑；架構圖本身的配色不動 */
:root{--brand:#154A41;--page-bg:#F4F4F0}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--brand:#59C2AE;--page-bg:#0E1412}}
:root[data-theme="dark"]{--brand:#59C2AE;--page-bg:#0E1412}
body{background:var(--page-bg);font-family:"Microsoft YaHei","微软雅黑","PingFang TC","PingFang SC","Noto Sans TC",system-ui,sans-serif}
.tabs a[aria-current="page"]{border-bottom-color:var(--brand)}
.tabs a:focus-visible{outline-color:var(--brand)}
h1{font-family:inherit;font-weight:900;letter-spacing:.04em;padding-left:14px;border-left:5px solid var(--brand);line-height:1.15}
/* 返回總覽：和分頁區隔開，不是分頁 */
.tabs a.back{border-bottom-color:transparent;margin-right:10px;padding-left:0;padding-right:14px;position:relative;font-weight:500}
.tabs a.back::after{content:"";position:absolute;right:0;top:25%;bottom:25%;border-right:1px solid var(--line)}
/* 橫向捲動容器邊緣漸層陰影，以視覺取代「可左右滑動」文字說明 */
.scroll{
  background:
    linear-gradient(to right, var(--surface) 20%, transparent),
    linear-gradient(to left, var(--surface) 20%, transparent),
    radial-gradient(farthest-side at 0 50%, rgba(20,30,27,.14), transparent),
    radial-gradient(farthest-side at 100% 50%, rgba(20,30,27,.14), transparent);
  background-position: 0 0, 100% 0, 0 0, 100% 0;
  background-repeat: no-repeat;
  background-size: 36px 100%, 36px 100%, 14px 100%, 14px 100%;
  background-attachment: local, local, scroll, scroll;
}
"""

html = f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title>Lab Collab Mate 架構全貌</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap">
<style>{style}{TABS_CSS}</style>
</head>
<body>
<div class="wrap">
<header>
  <nav class="tabs" aria-label="頁面"><a class="back" href="./">← 總覽</a><a href="daily.html">每日進度</a><a href="arch.html" aria-current="page">架構全貌</a></nav>
  <div class="eyebrow">LAB COLLAB MATE ・ USB-AGENT 技術架構</div>
  <h1>技術架構全貌</h1>
  <p class="lede">第一階段依程式碼現況整理；第二階段方案 A／B 尚待和 LabMind 團隊確認。</p>
  {legend}
</header>

{body.strip()}
</div>
</body>
</html>
"""
OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT} ({len(html)} bytes)")
