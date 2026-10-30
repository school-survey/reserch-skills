#!/usr/bin/env python3
"""koboyo 손그림 아이콘 검색·내려받기 (계정·API키 불필요).

라이선스: 개인·상업용 무료, 출처 표기 불필요 (https://koboyo.com/icons/license)
  가능   : 웹·앱·문서·발표자료·다이어그램·영상·인쇄물, 수정·재색, 클라이언트 작업
  불가   : 아이콘 모음 자체의 재판매·재배포, 경쟁 아이콘/캔버스 제품 제작

사용:
  python3 koboyo.py search 책            # 검색(한국어 입력 시 영어로 바꿔 넣을 것)
  python3 koboyo.py get book-open        # SVG를 stdout으로
  python3 koboyo.py get book-open -o assets/icons/   # 파일로 저장
  python3 koboyo.py get book-open pencil sparkles -o assets/icons/   # 여러 개
  python3 koboyo.py get book-open --color "#1a1a1a" --size 48 -o .
"""
import argparse, json, os, sys, urllib.parse, urllib.request

API = "https://api.koboyo.com/v1-icons/search"
SVG = "https://koboyo.com/icons/svg/{slug}.svg"
UA = {"User-Agent": "Mozilla/5.0 (koboyo-icons skill)"}


def _get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")


def search(query, limit):
    data = json.loads(_get(f"{API}?q={urllib.parse.quote(query)}"))
    icons = data.get("icons", [])[:limit]
    if not icons:
        print(f"'{query}' 결과 없음. 영어 단어로 다시 시도해 보라.", file=sys.stderr)
        return 1
    print(f"'{query}' — {len(icons)}개 (전체 {len(data.get('icons', []))}개 중)")
    for i in icons:
        print(f"  {i['slug']:42} {i.get('name','')}")
    print("\n스타일 변형은 슬러그 접두어로 구분된다: cartoon-*, solid-*, inkbrush-*")
    return 0


def style_svg(svg, color, size):
    if color:
        svg = svg.replace('fill="currentColor"', f'fill="{color}"', 1)
    if size:
        svg = svg.replace("<svg ", f'<svg width="{size}" height="{size}" ', 1)
    return svg


def get(slugs, outdir, color, size):
    rc = 0
    for slug in slugs:
        try:
            svg = style_svg(_get(SVG.format(slug=slug)), color, size)
        except Exception as e:
            print(f"[실패] {slug}: {e}", file=sys.stderr)
            rc = 1
            continue
        if outdir:
            os.makedirs(outdir, exist_ok=True)
            path = os.path.join(outdir, f"{slug}.svg")
            with open(path, "w", encoding="utf-8") as f:
                f.write(svg)
            print(f"저장: {path}")
        else:
            print(svg)
    return rc


def main():
    p = argparse.ArgumentParser(description="koboyo 아이콘 검색·내려받기")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="키워드로 검색")
    s.add_argument("query")
    s.add_argument("-n", "--limit", type=int, default=40)
    g = sub.add_parser("get", help="슬러그로 SVG 받기")
    g.add_argument("slugs", nargs="+")
    g.add_argument("-o", "--outdir")
    g.add_argument("--color", help='예: "#1a1a1a" (기본은 currentColor)')
    g.add_argument("--size", type=int, help="px 단위 width/height 부여")
    a = p.parse_args()
    sys.exit(search(a.query, a.limit) if a.cmd == "search" else get(a.slugs, a.outdir, a.color, a.size))


if __name__ == "__main__":
    main()
