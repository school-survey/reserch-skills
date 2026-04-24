---
name: riss-literature
description: 한국외국어대학교(HUFS) 도서관 계정으로 RISS에 접속해 논문을 키워드 검색·PDF 다운로드·주제별 자동 분류한다. "RISS", "논문 수집", "문헌 검색", "riss에서" 등의 키워드가 포함된 요청에 활성화.
---

# RISS 문헌 수집·분류 스킬

> ⚠️ **한국외국어대학교 도서관 계정 전용** 스킬입니다.  
> RISS 앱을 먼저 설치해야 합니다 → [GitHub: goldring-creator/riss-search](https://github.com/goldring-creator/riss-search)

## 앱 경로 설정

설치 후 아래 경로를 본인 환경에 맞게 수정하세요:
```
[RISS 앱 설치 경로]/_app/
```

## 앱 구동 방법

### GUI (권장)
```bash
cd "[RISS 앱 설치 경로]/_app"
node launcher/server.js
# → 브라우저에서 http://localhost:3000 접속
```
2-화면 UI: 로그인 화면 → 메인 화면 (Research Profile + 검색 실행)

### CLI (직접 실행)
```bash
cd "[RISS 앱 설치 경로]/_app"
node core/riss-main.js \
  --keyword "검색어1" [--keyword "검색어2"] \
  --pages 2 \
  --library-id [한국외대 도서관 학번] \
  --library-pw [비밀번호] \
  --output-dir [저장경로]
```

## CLI 옵션 전체

| 플래그 | 설명 | 기본값 |
|--------|------|--------|
| `--keyword` | 검색 키워드 (필수, 여러 개 가능) | — |
| `--pages` | 수집 페이지 수 | 2 |
| `--top-n` | 피인용 상위 N건만 추출 | 전체 |
| `--min-citations` | 최소 KCI 피인용 횟수 | 0 |
| `--exclude` | 제외 키워드 (콤마 구분) | 없음 |
| `--sort` | 정렬: rank / newest / popular | rank |
| `--year-from` | 수집 시작 연도 | 전체 |
| `--year-to` | 수집 종료 연도 | 전체 |
| `--kci-only` | KCI 등재 논문만 수집 | false |
| `--skip-download` | PDF 다운로드 건너뜀 | false |
| `--skip-classify` | AI 분류 건너뜀 | false |
| `--output-dir` | 결과 저장 경로 | _app/output/ |

## 파이프라인 구조

```
1단계: 문헌 검색 및 메타데이터 수집
  ├── Phase A: 검색 결과 목록에서 링크 수집
  └── Phase B: 상세 페이지 병렬 수집 (3 workers)

2단계: Claude 관련도 필터링 (초록 700자 기준, 배치 15편)

3단계: PDF 다운로드
  - 우선순위: KCI > 스콜라 > KISS > DBpia > earticle

4단계: 주제별 자동 분류 (5편 배치)
  - 1차: 전체 초록 기반 카테고리 3~5개 생성
  - 2차: 5편씩 배치로 카테고리 배정 + 한 줄 요약
```

## 결과물 구조

```
output/
├── metadata.json         # 전체 논문 메타데이터
├── report.csv            # 제목·저자·연도·카테고리·요약·다운로드상태
└── pdfs/
    ├── unclassified/     # 분류 전 PDF
    └── classified/
        ├── {카테고리1}/
        └── {카테고리2}/
```

## Research Profile (GUI 전용)

수집 전 연구 프로파일 설정으로 관련도·분류 정확도 향상:
- **A 파일 업로드**: PDF/DOCX/TXT 논문계획서 → 키워드+연구맥락 자동 추출
- **B 연구 맥락 텍스트**: 직접 입력 → 키워드 자동 생성
- **C 키워드 태그**: 수동 입력 (Enter/쉼표로 추가)

## 주의사항

- 국내학술논문(re_a_kor)만 수집 — 학위논문·해외논문 제외
- 초록 미등록 논문은 초록 0자로 저장됨 (RISS 측 이슈)
- DRM 보호 논문은 자동 다운로드 불가
- 자격증명은 macOS Keychain / Windows DPAPI에 안전하게 저장됨
