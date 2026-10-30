"""편집용 PPTX 글꼴을 맑은 고딕으로 바꾸고(윈도우와 맥 파워포인트 모두 있음), 화면 캡처로 PDF를 만든다.
(메뉴의 Export as PDF는 인쇄 창을 띄워 헤드리스에서 받을 수 없다.)
사용: python finalize.py <출력폴더> <장수>  → edit_malgun.pptx, deck.pdf"""
import sys, zipfile, re
from playwright.sync_api import sync_playwright
out, n = sys.argv[1], int(sys.argv[2])
zin = zipfile.ZipFile(f'{out}/edit.pptx'); zout = zipfile.ZipFile(f'{out}/edit_malgun.pptx', 'w', zipfile.ZIP_DEFLATED)
cnt = 0
for it in zin.infolist():
    d = zin.read(it.filename)
    if it.filename.endswith('.xml'):
        t = d.decode('utf-8')
        new = re.sub(r'typeface="[^"]*"', lambda m: m.group(0) if m.group(0) in ('typeface="+mj-lt"', 'typeface="+mn-lt"') else 'typeface="맑은 고딕"', t)
        cnt += t.count('typeface="') ; d = new.encode('utf-8')
    zout.writestr(it, d)
zout.close(); print('typeface 교체', cnt)
imgs = ''.join(f'<img src="file://{out}/p{i:02d}.png">' for i in range(1, n + 1))
open(f'{out}/deck.html', 'w', encoding='utf-8').write('<html><head><style>@page{size:1920px 1080px;margin:0}body{margin:0}img{display:block;width:1920px;height:1080px;page-break-after:always}</style></head><body>' + imgs + '</body></html>')
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(f'file://{out}/deck.html'); pg.wait_for_timeout(1500)
    pg.pdf(path=f'{out}/deck.pdf', width='1920px', height='1080px', print_background=True); b.close()
print('deck.pdf 완료')
