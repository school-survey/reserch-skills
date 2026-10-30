---
name: kordoc
description: HWP·HWPX·PDF·XLSX·DOCX 파일을 마크다운으로 변환해 내용을 읽고 분석한다. "이 hwp 읽어줘", "이 파일 내용 보여줘", "두 문서 비교해줘", "xlsx 데이터 정리해줘", "pdf 내용 추출해줘" 등의 요청에 사용한다. 파일 경로를 받아 ~/.npm-global/bin/kordoc으로 변환 후 결과를 분석한다.
---

# kordoc 파일 변환 스킬

HWP·HWPX·PDF·XLSX·DOCX 파일을 마크다운으로 변환해 내용을 읽고 분석한다.

## 실행 도구

```
~/.npm-global/bin/kordoc [파일경로]
```

지원 형식: `.hwp` `.hwpx` `.hwpml` `.pdf` `.xlsx` `.xls` `.docx`

## 작업 절차

1. 사용자가 파일 경로를 제공하거나 파일명을 언급하면, 경로를 확인한다.
   - 경로가 불분명하면 `find` 또는 `Glob`으로 먼저 파일을 찾는다.
2. Bash로 변환 명령을 실행한다:
   ```
   ~/.npm-global/bin/kordoc "파일경로"
   ```
3. 변환된 마크다운을 읽고 사용자 요청에 맞게 분석·정리·요약한다.

## 요청 유형별 처리

### 단일 파일 읽기·분석
```bash
~/.npm-global/bin/kordoc "파일.hwp"
```
→ 변환 결과를 바탕으로 내용 요약·분석

### 두 파일 비교 (신구대조)
```bash
~/.npm-global/bin/kordoc "구버전.hwp"
~/.npm-global/bin/kordoc "신버전.hwp"
```
→ 두 결과를 비교해 변경사항 정리

### 특정 페이지·범위만 추출
```bash
~/.npm-global/bin/kordoc "파일.pdf" --pages 1-5
```

### JSON 구조로 추출 (표 데이터 등)
```bash
~/.npm-global/bin/kordoc "데이터.xlsx" --format json
```

## 주의사항

- 파일 경로에 한글·공백이 있으면 반드시 따옴표로 감싼다.
- 변환 실패 시 파일 형식·경로·손상 여부를 확인한다.
- HWP 암호화 파일은 변환 불가.
- 대용량 PDF는 `--pages` 옵션으로 범위를 나눠 처리한다.
