---
name: hwpx
description: "한국어 학술 문서·논문·HWP 파일 생성 스킬. 다음 표현이 나오면 반드시 이 스킬을 사용할 것: 'hwp로 작성해줘', '한글파일로 작성해줘', '한글로 써줘', '한글 문서', '한글파일', '.hwpx', 'HWP', '논문 초안 작성', '한글로 작성', '워드로 작성', 'docx로'. 기본 출력은 Python 버전에 따라 선택: Python 3.10+는 python-hwpx HwpxDocument.new()로 .hwpx 생성, Python 3.9는 python-docx로 .docx 생성. HWPX 특정 요청 또는 사용자 제공 HWPX 양식이 있을 때만 ZIP-level HWPX 처리를 사용한다."
---

# 한국어 학술 문서 생성 스킬

## 개요

한국어 학술 논문·보고서·문서 초안을 생성하는 스킬이다.

- **Python 3.10+**: `python-hwpx` `HwpxDocument.new()` → `.hwpx` (권장)
- **Python 3.9**: `python-docx` → `.docx` (fallback)
- **사용자 제공 HWPX 양식**: ZIP-level 치환 방식

## 설치

```bash
# Python 3.10+
pip install python-hwpx --break-system-packages

# Python 3.9 (fallback)
pip install python-docx --break-system-packages
```

---

## 문서 생성 의사결정 트리

```
출력 경로 폴더에 format.md / design.md / 양식.md 가 있는가?
  → YES: 해당 파일을 먼저 읽고 그 지침을 따른다.
  → NO: 아래 계속

사용자가 HWPX 양식 파일(.hwpx)을 제공했는가?
  → YES: ZIP-level 치환 방식 사용 (아래 참조)
  → NO: 아래 계속

Python 버전 확인
  → 3.10+: HwpxDocument.new() → .hwpx 생성
  → 3.9:   python-docx → .docx 생성
```

### 폴더 형식 파일 탐색

```python
import os, sys

def find_format_guide(output_dir):
    for name in ['format.md', 'design.md', '양식.md', '스타일.md', 'FORMAT.md']:
        path = os.path.join(output_dir, name)
        if os.path.exists(path):
            return path
    return None

def python_version_ok():
    return sys.version_info >= (3, 10)
```

---

## python-hwpx 방식 (Python 3.10+ — 기본 권장)

### HwpxDocument.new() API 요약

```python
from hwpx import HwpxDocument

# 새 빈 문서 생성
doc = HwpxDocument.new()

# 단락 추가 (텍스트, 선택적 스타일 참조)
para = doc.add_paragraph("본문 텍스트")
# para_pr_id_ref, style_id_ref, char_pr_id_ref 로 스타일 지정 가능

# 기존 파일 열기
doc = HwpxDocument.open("경로/파일.hwpx")

# 저장 (경로 지정)
doc.save_to_path("출력경로/파일.hwpx")

# 저장 (bytes 반환)
data = doc.to_bytes()

# 헤더/푸터
doc.set_header_text("헤더 텍스트")
doc.set_footer_text("푸터 텍스트")

# 텍스트 치환 (run 내부)
doc.replace_text_in_runs("검색", "교체")

# 표 추가
table = doc.add_table(rows=3, cols=4)

# 섹션 추가
section = doc.add_section()

# paragraphs 접근
for p in doc.paragraphs:
    print(p.text)
```

### 주의사항 (Python 3.10+)

- `HwpxDocument.new()`는 blank_document_bytes 기반의 최소 골격 문서를 생성한다.
- `add_paragraph()`에서 `inherit_style=True`(기본값)이면 이전 단락의 스타일을 이어받는다.
- `save(path)` 대신 `save_to_path(path)`를 사용한다 (`save()`는 deprecated 예정).
- 스타일 지정은 `para_pr_id_ref`, `style_id_ref`, `char_pr_id_ref`(정수 ID)로 한다.
  새 문서에서는 헤더에 등록된 기존 ID를 먼저 확인해야 한다.

### 학술 논문 구조 예시 (Python 3.10+)

```python
from hwpx import HwpxDocument
import os

doc = HwpxDocument.new()

# 제목
doc.add_paragraph("논문 제목")

# 섹션 제목
doc.add_paragraph("Ⅰ. 서론")

# 본문
doc.add_paragraph("본 연구는 ...")

# 참고문헌
doc.add_paragraph("참고문헌")
doc.add_paragraph("김철수(2024). 논문 제목. 학술지명, 1(1), 1-10.")

# 저장
doc.save_to_path(output_path)
print("Saved:", output_path)
```

---

## python-docx 방식 (Python 3.9 fallback — 학술 논문, 일반 문서)

```python
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

doc = Document()

# 페이지 여백 설정
section = doc.sections[0]
section.left_margin   = Inches(1.2)
section.right_margin  = Inches(1.2)
section.top_margin    = Inches(1.0)
section.bottom_margin = Inches(1.0)

# ── 제목 ──────────────────────────────────────────
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("논문 제목")
run.bold = True
run.font.size = Pt(16)
doc.add_paragraph()  # 빈 줄

# ── 섹션 제목 ─────────────────────────────────────
def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(13 if level == 1 else 12)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after  = Pt(6)
    return p

# ── 본문 단락 ─────────────────────────────────────
def add_body(doc, text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(6)
    for run in p.runs:
        run.font.size = Pt(11)
    return p

# ── 참고문헌 항목 ─────────────────────────────────
def add_ref(doc, text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(4)
    for run in p.runs:
        run.font.size = Pt(10.5)
    return p

# 사용 예시
add_heading(doc, "Ⅰ. 서론")
add_body(doc, "본 연구는 ...")

add_heading(doc, "참고문헌")
add_ref(doc, "김철수(2024). 논문 제목. 학술지명, 1(1), 1-10.")
add_ref(doc, "Bakker, A. B., & Demerouti, E. (2007). The job demands-resources model. Journal of Managerial Psychology, 22(3), 309-328.")

doc.save(output_path)
print("Saved:", output_path)
```

---

## ZIP-level HWPX 치환 방식 (사용자 제공 HWPX 양식용)

사용자가 `.hwpx` 파일을 직접 제공한 경우에만 사용한다.

### 텍스트 추출 함수 (hp:t regex 방식)

```python
import zipfile, re

def find_hwpx_texts(hwpx_path):
    """HWPX 내 hp:t 텍스트 노드를 모두 추출한다. (ET 파싱 불가 → regex 사용)"""
    texts = []
    with zipfile.ZipFile(hwpx_path, "r") as z:
        for name in z.namelist():
            if name.startswith("Contents/") and name.endswith(".xml"):
                data = z.read(name).decode("utf-8")
                for t in re.findall(r'<hp:t[^>]*>([^<]+)</hp:t>', data):
                    if t.strip():
                        texts.append(t)
    return texts
```

### 일괄 치환

```python
def zip_replace(src_path, dst_path, replacements):
    tmp = dst_path + ".tmp"
    with zipfile.ZipFile(src_path, "r") as zin:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename.startswith("Contents/") and item.filename.endswith(".xml"):
                    text = data.decode("utf-8")
                    for old, new in replacements.items():
                        text = text.replace(old, new)
                    data = text.encode("utf-8")
                zout.writestr(item, data)
    if os.path.exists(dst_path):
        os.remove(dst_path)
    os.rename(tmp, dst_path)
```

### 순차 치환 (같은 플레이스홀더가 여러 번 반복될 때)

```python
def zip_replace_seq(src_path, dst_path, old, new_list):
    tmp = dst_path + ".tmp"
    with zipfile.ZipFile(src_path, "r") as zin:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if "section" in item.filename and item.filename.endswith(".xml"):
                    text = data.decode("utf-8")
                    for new_val in new_list:
                        text = text.replace(old, new_val, 1)
                    data = text.encode("utf-8")
                zout.writestr(item, data)
    if os.path.exists(dst_path):
        os.remove(dst_path)
    os.rename(tmp, dst_path)
```

### HWPX 워크플로우

```
[1] 사용자 제공 양식을 /tmp/ 로 복사
     ↓
[2] find_hwpx_texts()로 플레이스홀더 파악
     ↓
[3] zip_replace() / zip_replace_seq()로 치환
     ↓
[4] fix_namespaces.py 실행 (필수!)
     ↓
[5] find_hwpx_texts()로 검증
     ↓
[6] 출력 경로에 저장
```

### fix_namespaces 후처리 (HWPX 전용)

```python
import subprocess, os

fix_script = os.path.expanduser("~/.claude/skills/hwpx/scripts/fix_namespaces.py")
subprocess.run(["python3", fix_script, "output.hwpx"], check=True)
# 반드시 subprocess.run() 사용 — exec() 방식 금지
```

---

## Quick Reference

| 상황 | 방법 |
|------|------|
| 학술 논문, 논문 초안 (Python 3.10+) | **HwpxDocument.new()** → `.hwpx` |
| 학술 논문, 논문 초안 (Python 3.9) | **python-docx** → `.docx` |
| 폴더에 format.md / design.md 있음 | 해당 파일 먼저 읽고 지침 따름 |
| 사용자가 HWPX 양식 파일 제공 | ZIP-level 치환 → fix_namespaces |
| 텍스트 추출·검증 | `find_hwpx_texts()` (hp:t regex) |

---

## 참고 문서 (references/)

| 파일 | 사용 시점 |
|------|----------|
| `references/academic-defaults.md` | format.md 없을 때 기본값 — 여백·폰트·APA 인용·학술 문체 |
| `references/citation-reference-guide.md` | 참고문헌 표기 상세 필요 시 — APA 7th 전체, 통계·표·그림 규범 |
| `references/xml-internals.md` | HWPX XML 저수준 조작 필요 시 |

---

## 주의사항

1. **Python 버전 확인 필수**: `HwpxDocument.new()`는 Python 3.10+에서만 동작한다.
   Python 3.9에서는 `@dataclass(slots=True)` 오류로 import 자체가 실패한다.
   → Python 버전 먼저 확인 후 적절한 방식 선택.
2. **기본은 빈 문서**: 템플릿 강제 없음. 새 문서를 기본으로 작성한다.
3. **폴더 format.md 우선**: 출력 폴더에 형식 가이드 파일이 있으면 반드시 읽는다.
4. **save_to_path() 사용**: `save(path)` 대신 `save_to_path(path)` 사용 (deprecated 방지).
5. **HWPX 후처리**: ZIP-level 치환 후 반드시 `fix_namespaces.py` 실행.
6. **hp:t regex 방식**: HWPX 텍스트 추출 시 ET 파싱 대신 `hp:t` regex 사용 (ET ParseError 방지).
7. **CJK 검증**: 생성 문서에 의도치 않은 한자·일본어 문자가 없는지 완료 전 확인.
