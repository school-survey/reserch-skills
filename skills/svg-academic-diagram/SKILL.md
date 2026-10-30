---
name: svg-academic-diagram
description: Use when creating SVG diagrams for academic research presentations — path models (LGM, SEM), tree/hierarchy structures, or flowcharts — requiring mathematically verified symmetric layout
---

# 학술 연구용 SVG 도형 작성

## Overview

도형 유형별 좌표 공식으로 SVG를 설계하고, 완료 전 대칭성을 수학적으로 검증한다.
**감각이 아닌 공식으로 배치하고, 추정이 아닌 계산으로 검증한다.**

## 도형 유형 선택

```
어떤 구조인가?
├─ 단계별 좌→우 흐름 + 잠재/관측변수
│   → A. 경로 모형 (LGM·SEM)
├─ 상위→하위 계층 분기
│   → B. 트리 구조
└─ 순서 흐름 + 조건 분기
    → C. 플로우차트
```

> 완성 예시 파일: `examples.html` (같은 폴더)

### A. 경로 모형 — 구조 모습
```
[공변량]──→ (I₁)──────────→ (I₂)──→ [결과]
  │     ╔══╧══╗         ╔══╧══╗      │
  └───→ (S₁)──────────→ (S₂)──┘
        ╚═╤═╤═╝         ╚═╤═╤═╝
         [Y1][Y2][Y3]    [Y4][Y5]
    ←─────────────────────────────→
         zone 1              zone 2
     (잠재변수 원, 관측변수 네모, 구역별 zone 박스)
```

### B. 트리 구조 — 구조 모습
```
             [루트]
           ╱    │    ╲
      [A]      [B]      [C]
     ╱   ╲    ╱   ╲    ╱   ╲
  [A1] [A2] [B1] [B2] [C1] [C2]
  (부모 cx = 자식들 cx의 중점)
```

### C. 플로우차트 — 구조 모습
```
      ╭──────────╮
      │  시작/종료  │  ← 타원(rx 큰 rect)
      ╰──────────╯
            │
      ┌──────────┐
      │  처리 단계  │  ← 직사각형
      └──────────┘
            │
      ◇ 조건 분기 ◇  ← 다이아몬드 (polygon 4꼭짓점)
      예↓        아니오→ ┌────────┐
      ┌────────┐         │ 분기처리 │
      │ 처리A   │         └────────┘
      └────────┘              │
            └────────────────┘  ← 재합류
            │
      ╭──────────╮
      │  시작/종료  │
      ╰──────────╯
```

---

## A. 경로 모형 (LGM·SEM·매개모형)

### 핵심 공식

**구역 중심점**
```
center_x = zone_x + zone_w / 2
```

**잠재변수(원) 배치**
- 단일: `cx = center_x`
- 쌍(I/S): `I_cx = center_x - d/2`, `S_cx = center_x + d/2`

**관측변수(네모) 대칭 배치**
```
total_box_w = n × box_w + (n-1) × gap
start_x     = center_x - total_box_w / 2
box[i].x    = start_x + i × (box_w + gap)
```

**구역 높이 역산 (반드시 관측변수 배치 후)**
```
zone_h = (box_y + box_h) - zone_y + 여백(10~15px)
```
> 구역 높이를 먼저 설정하면 Y박스가 경계 밖으로 나간다.

### 표준 도형 참조

| 요소 | SVG | 권장 크기 |
|------|-----|---------|
| 잠재변수 | `<circle>` | r=24~28 |
| 관측변수 | `<rect>` | w=40~42, h=26~28 |
| 구역 경계 | `<rect>` stroke-dasharray | rx=7 |
| 주 경로 | `<line>` + `<marker>` | stroke-width=2 |
| 교차 경로 | `<line>` stroke-dasharray | stroke-width=1 |
| 공분산 호 | `<path>` quadratic Bezier | stroke-width=1.2 |
| 인자부하 | `<line>` 0.8px | 실선=주, 점선=부 |

### 작성 순서
1. viewBox 산정 (구역 합산 + 여백)
2. 구역 분할 → `center_x` 계산
3. 잠재변수 배치 (`cy`는 전 구역 동일)
4. 관측변수 배치 (`y`는 전 구역 동일)
5. 구역 높이 역산
6. 경로·화살표 작성
7. **대칭 검증**

### 대칭 검증 체크리스트
```
□ 잠재변수 중점 = center_x?
     (I_cx + S_cx) / 2  ==  center_x

□ 관측변수 좌우 여백 동일?
     left_gap  = box[0].x - zone_x
     right_gap = (zone_x + zone_w) - (box[n-1].x + box_w)
     left_gap  ==  right_gap

□ 구역 높이: Y박스 포함?
     zone_y + zone_h  >  box_y + box_h

□ 전 구역 수평 정렬 통일?
     모든 구역의 I cy 동일  ✓
     모든 구역의 S cy 동일  ✓
     모든 구역의 Y박스 y 동일  ✓
```

---

## B. 트리 구조 (계층·분류 다이어그램)

### 핵심 공식

**레벨별 y 좌표**
```
node_y[level] = root_y + level × (node_h + v_gap)
```

**자식 노드 균등 배치 (부모 아래 대칭)**
```
subtree_w     = n_children × node_w + (n_children - 1) × h_gap
child_start_x = parent_cx - subtree_w / 2
child[i].cx   = child_start_x + i × (node_w + h_gap) + node_w / 2
```

**형제 노드 간 겹침 방지**
```
min_h_gap = node_w × 0.3   (권장: 20~40px)
```

**연결선 (부모 → 자식)**
```html
<line x1="parent_cx" y1="parent_y + node_h"
      x2="child_cx"  y2="child_y"
      stroke="..." stroke-width="1.5" marker-end="url(#aw)"/>
```
> 꺾이는 연결선이 필요하면 `<path>` + `L` 커맨드로 수직·수평 꺾기

### 표준 도형 참조

| 요소 | SVG | 권장 크기 |
|------|-----|---------|
| 루트 노드 | `<rect>` rx=8 (강조색) | w=120~160, h=40~48 |
| 중간 노드 | `<rect>` rx=6 | w=100~140, h=36~44 |
| 말단 노드 | `<rect>` rx=4 (연한 색) | w=80~120, h=30~38 |
| 연결선 | `<line>` 또는 `<path>` L커맨드 | stroke-width=1.2~1.8 |

### 작성 순서
1. 트리 구조 파악 (레벨 수, 각 레벨 노드 수)
2. 말단 노드(leaf) 기준 전체 너비 산정
3. 말단 → 루트 순으로 각 부모의 `cx` 역산
4. 레벨별 `y` 확정
5. 연결선 작성
6. **대칭 검증**

### 대칭 검증 체크리스트
```
□ 각 부모 cx = 자식들 cx의 중점?
     parent_cx  ==  (child[0].cx + child[n-1].cx) / 2

□ 형제 노드 간격 균등?
     child[i+1].cx - child[i].cx  ==  동일값 (전 형제 쌍)

□ 같은 레벨 노드의 y 동일?
     모든 level-k 노드의 node_y[k]  ==  동일값

□ 노드 겹침 없음?
     인접 노드: child[i].cx + node_w/2  <  child[i+1].cx - node_w/2
```

---

## C. 플로우차트 (순서도·의사결정 흐름)

### 핵심 공식

**수직 흐름 (기본)**
```
node[i].cy = start_y + i × (node_h + v_gap)
모든 노드 cx = canvas_cx  (수직 중심선)
```

**분기 후 재합류 시 y 조정**
```
branch_bottom = max(yes_path_bottom, no_path_bottom) + v_gap
재합류 노드 cy = branch_bottom + node_h / 2
```

**다이아몬드(조건) 꼭짓점 계산**
```
top    = (cx,     cy - hh)
right  = (cx + hw, cy)
bottom = (cx,     cy + hh)
left   = (cx - hw, cy)

SVG: <polygon points="${cx},${cy-hh} ${cx+hw},${cy} ${cx},${cy+hh} ${cx-hw},${cy}"/>
권장 hw=55~70, hh=28~35 (가로:세로 ≈ 2:1)
```

**분기 화살표**
- Yes (아래): `x1=cx, y1=cy+hh → x2=cx, y2=next_top`
- No (오른쪽 또는 왼쪽): `x1=cx+hw, y1=cy → L → x2=branch_node_cx, y2=branch_node_top`

### 표준 도형 참조

| 요소 | SVG | 권장 크기 |
|------|-----|---------|
| 시작/종료 (타원형) | `<rect>` rx=20 또는 `<ellipse>` | w=120, h=40 |
| 처리 (프로세스) | `<rect>` rx=4~6 | w=140~180, h=40~48 |
| 조건 (다이아몬드) | `<polygon>` 4꼭짓점 | hw=60, hh=30 |
| 흐름 화살표 | `<line>` + `<marker>` | stroke-width=1.5 |
| 분기 꺾임 | `<path>` M L L | stroke-width=1.5 |
| 분기 레이블 | `<text>` 화살표 옆 | font-size=10~11 |

### 작성 순서
1. 흐름 단계 목록화 (노드 유형: 시작/처리/조건/종료)
2. 수직 중심선(`canvas_cx`) 확정
3. 분기 없는 구간 `cy` 순차 배정
4. 분기 구간: Yes·No 각 경로 `cy` 따로 계산 → 재합류 `cy` 역산
5. 다이아몬드 꼭짓점 계산
6. 화살표·분기선 작성 + 레이블(예/아니오) 추가
7. **대칭 검증**

### 대칭 검증 체크리스트
```
□ 주 흐름 노드 cx = canvas_cx?
     처리·시작·종료 노드 모두 cx == canvas_cx

□ 분기 레이블 위치 일관?
     Yes 레이블: 아래 화살표 왼쪽 옆
     No  레이블: 옆 화살표 위쪽 옆

□ 같은 유형 노드의 크기 동일?
     모든 처리 박스 width 동일
     모든 다이아몬드 hw·hh 동일

□ 재합류 노드가 분기 아래에 위치?
     재합류 cy  >  max(yes_bottom, no_bottom)
```

---

## 공통: 자주 하는 실수

| 실수 | 증상 | 해결 |
|------|------|------|
| 크기·간격을 감각으로 조정 | 미세 비대칭 | 공식으로 계산 후 배치 |
| 컨테이너 크기 먼저 설정 | 요소가 경계 밖으로 나감 | 요소 배치 후 컨테이너 역산 |
| 화살표를 도형 중심에서 시작 | 화살표가 도형을 뚫음 | 도형 가장자리 좌표에 오프셋 적용 |
| 분기 경로 cy를 독립 계산 | 재합류 노드가 분기 위로 올라감 | max(branch bottoms) + gap으로 역산 |
| 부모 cx를 자식 배치 전 설정 | 부모-자식 정렬 어긋남 | 자식 배치 후 부모 cx 역산 |

---

## 완료 후 CJK 검증 (필수)

```python
with open(path, encoding='utf-8') as f:
    text = f.read()
print(f'총 {len(text)}자')
found = False
for i, ch in enumerate(text):
    code = ord(ch)
    if 0x4E00 <= code <= 0x9FFF:
        print(f'[한자] {repr(ch)} U+{code:04X} 전후: {repr(text[max(0,i-8):i+8])}')
        found = True
    if 0x3040 <= code <= 0x30FF:
        print(f'[일본어] {repr(ch)} U+{code:04X}')
        found = True
if not found:
    print('CJK 검증 통과 ✅')
```
