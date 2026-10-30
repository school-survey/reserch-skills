"""장마다 1920x1080 화면을 찍고 캔버스 밖으로 넘친 요소를 보고한다.
사용: python shoot.py <port> <slide-id> <장수> <출력폴더>"""
import sys
from playwright.sync_api import sync_playwright
port, sid, n, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
JS = '''() => {
  const els=[...document.querySelectorAll('div')].filter(e=>{const r=e.getBoundingClientRect();return r.width>1500 && Math.abs(r.width/r.height-16/9)<0.02});
  els.sort((a,b)=>b.getBoundingClientRect().width-a.getBoundingClientRect().width);
  const root=els[els.length-1]; if(!root) return 'no root';
  const R=root.getBoundingClientRect(); const bad=[];
  root.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect(); if(r.width===0) return;
    if(r.bottom>R.bottom+1||r.right>R.right+1||r.left<R.left-1) bad.push((e.textContent||e.tagName).slice(0,40));});
  return bad.slice(0,6).join(' | ')||'ok';
}'''
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    pg.goto(f'http://localhost:{port}/s/{sid}', wait_until='networkidle')
    pg.wait_for_timeout(1000)
    pg.get_by_role('button', name='Present', exact=True).click()
    pg.wait_for_timeout(1200)
    for i in range(1, n + 1):
        pg.screenshot(path=f'{out}/p{i:02d}.png')
        print(i, pg.evaluate(JS))
        pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(500)
    b.close()
