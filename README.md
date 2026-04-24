# Claude 연구용 스킬 패키지

연구자를 위한 Claude Code 스킬 72개 모음입니다.  
문헌 조사부터 논문 작성·검토·발표까지 연구의 전 단계를 커버합니다.

---

## 다운로드

**[⬇ research-skills.zip 다운로드](./research-skills.zip)**

zip 파일 안에 72개 스킬 폴더와 `사용 전 읽어주세요.txt`가 포함되어 있습니다.

---

## 설치 방법

### 방법 1 — Claude Code 터미널 (권장)

1. Claude Code(터미널)를 엽니다
2. `research-skills.zip`을 터미널 창에 **드래그 앤 드랍**합니다
3. `이 스킬들 전부 설치해줘` 라고 입력합니다

### 방법 2 — 수동 설치

```bash
unzip research-skills.zip
cp -r skills/* ~/.claude/skills/
```

### 설치 확인

Claude Code에서 `/research-develop` 을 입력해 스킬이 동작하는지 확인합니다.

---

## 포함된 스킬 (72개)

| 카테고리 | 스킬 수 | 주요 스킬 |
|---|---|---|
| 연구 시작 | 7 | `/research-develop`, `/deep-research`, `/idea-to-proposal` |
| 문헌 조사 | 11 | `/literature-review`, `/gs-search`, `/content-access` |
| 논문 작성 | 8 | `/academic-paper`, `/academic-writing`, `/academic-pipeline` |
| 검토·수정 | 12 | `/review-paper`, `/paper-polishing`, `/rebuttal` |
| 방법론 | 9 | `/research-methodology`, `/qualitative-research`, `/systematic-review` |
| 연구비·제안서 | 4 | `/grant`, `/grant-writing`, `/review-grant` |
| 분석·종합 | 7 | `/results-analysis`, `/research-synthesis`, `/csv-data-summarizer` |
| 인용·참고문헌 | 5 | `/citation-assistant`, `/bibliography`, `/zotero-obsidian-bridge` |
| 발표 자료 | 2 | `/academic-pptx`, `/poster-slides-maker` |
| 전문가 에이전트 | 7 | `/evidence-rigor-architect`, `/meta-analysis-protocol-architect` |

각 스킬의 상세 설명은 zip 내 **`사용 전 읽어주세요.txt`** 를 참고하세요.

---

## 함께 보기

- [Claude 연구 활용 가이드](https://github.com/goldring-creator/claude_guide_for_edu-reserch) — 스킬 활용법을 포함한 교육학 연구자용 Claude 사용 가이드
