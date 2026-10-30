"""Download 메뉴로 편집용 PPTX를 받는다. (이미지 PPTX는 기본 제외, --image를 붙일 때만.)
사용: python export.py <port> <slide-id> <출력폴더> [--image]  → edit.pptx (--image면 image.pptx도)"""
import sys, os
from playwright.sync_api import sync_playwright
port, sid, out = sys.argv[1], sys.argv[2], sys.argv[3]
want_image = '--image' in sys.argv[4:]
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 1920, 'height': 1080}, accept_downloads=True)
    pg = ctx.new_page()
    pg.goto(f'http://localhost:{port}/s/{sid}', wait_until='networkidle')
    pg.wait_for_timeout(1500)
    targets = [('Export as PPTX', 'edit.pptx')] + ([('Export as image PPTX', 'image.pptx')] if want_image else [])
    for label, name in targets:
        pg.get_by_role('button', name='Download').click()
        pg.wait_for_timeout(600)
        with pg.expect_download(timeout=300000) as d:
            pg.get_by_role('menuitem', name=label, exact=True).click()
        d.value.save_as(os.path.join(out, name)); print(label, '->', name)
        pg.wait_for_timeout(1000)
    b.close()
