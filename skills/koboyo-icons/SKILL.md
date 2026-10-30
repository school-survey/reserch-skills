---
name: koboyo-icons
description: 손그림 느낌의 SVG 아이콘 16만여 개(koboyo)를 검색해 프로젝트에 내려받는다. 강의 슬라이드·카드뉴스·HTML 문서·발표자료에 아이콘이 필요할 때 사용. "아이콘 찾아줘", "아이콘 넣어줘", "손그림 아이콘", "koboyo", "SVG 아이콘", "슬라이드에 아이콘" 등의 요청에 활성화. 계정·API키가 필요 없고, 개인·상업용 무료에 출처 표기도 필요 없다.
---

# koboyo 아이콘

손으로 그린 듯한 SVG 아이콘 16만여 개. 계정 없이 바로 쓴다.

## 검색 → 내려받기

```bash
K=~/.claude/skills/koboyo-icons/koboyo.py

python3 $K search graduation            # 키워드로 검색 (영어로 넣는다)
python3 $K search "book" -n 60

python3 $K get graduation-cap -o assets/icons/
python3 $K get book-open pencil sparkles -o assets/icons/     # 여러 개 한 번에
python3 $K get book-open --color "#1a1a1a" --size 48 -o .     # 색·크기 지정
python3 $K get book-open                                       # stdout으로 (HTML에 인라인)
```

**검색어는 영어로 넣는다.** 한국어를 넣으면 결과가 없다. "졸업" → `graduation`, "책" → `book`, "생각" → `brain`/`idea`.

## 스타일

슬러그 접두어로 구분된다. 검색 결과에 함께 나온다.

| 접두어 | 느낌 |
|---|---|
| (없음) | 기본 선화 |
| `cartoon-` | 만화체 |
| `solid-` | 면으로 채운 것 |
| `inkbrush-` | 붓 느낌 |

한 문서 안에서는 **한 가지 스타일로 통일**한다. 섞으면 바로 티가 난다.

## 문서에 넣는 법

SVG는 `fill="currentColor"`로 나오므로, 인라인으로 넣으면 **주변 글자색을 따라간다**. 다크모드 대응이 저절로 된다.

```html
<span class="ico"><svg ...>…</svg></span>
<style>.ico svg { width: 1.25em; height: 1.25em; vertical-align: -0.15em; }</style>
```

`--color`로 색을 박으면 그 색으로 고정된다. 테마가 바뀌는 문서에는 쓰지 않는다.

pptx로 갈 산출물이면 SVG를 그대로 두지 말고 PNG로 변환해 넣는다.

## 라이선스 (2026-09-02 원문 확인)

출처: https://koboyo.com/icons/license — 전량 개인·상업용 무료, **출처 표기 불필요**.

- **된다**: 웹·앱·문서·발표자료·다이어그램·영상·인쇄물. 수정·재색·크기 변경. 판매하는 산출물에 포함(클라이언트 작업, 템플릿 포함) — 단 아이콘이 부속일 것.
- **안 된다**: 아이콘 모음 자체를 재판매·재배포. 아이콘 라이브러리나 캔버스·화이트보드·다이어그램·발표 앱 같은 경쟁 제품 제작. 사용자가 아이콘을 골라 내려받게 하는 앱에 묶기. 컬렉션 저작자를 자처하기.

강의자료·논문 도식·카드뉴스는 전부 허용 범위 안이다.

## MCP (선택)

koboyo는 MCP 서버도 제공한다(`https://api.koboyo.com/v1-mcp`). 다만 **로그인해서 키를 발급받아야** 한다.
키가 있다면:

```bash
claude mcp add --transport http koboyo "https://api.koboyo.com/v1-mcp?key=kbi_발급받은키"
```

MCP는 아이콘 검색에 더해 koboyo 캔버스에 다이어그램·슬라이드를 그리는 기능까지 준다.
아이콘만 쓸 거라면 **위 CLI로 충분하고, 매 세션 도구 스키마를 물지 않아 더 가볍다.**
