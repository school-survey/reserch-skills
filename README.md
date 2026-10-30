# Claude 연구용 스킬 묶음

교육학·사회과학 연구자를 위한 Claude Code 스킬 묶음입니다.
깃허브에 공개된 연구용 스킬 가운데 실제로 쓰는 것만 추린 **연구 스킬 29종**과, 한글·PDF·발표 자료·통계를 다루는 **범용 스킬 10종**, Im-not-AI 플러그인을 함께 담았습니다.

---

## 다운로드

**[⬇ research-skills.zip 다운로드](./research-skills.zip)** (약 1.9MB)

## 설치

1. Claude Code를 켭니다
2. `research-skills.zip`을 창에 끌어다 놓습니다
3. `이거 설치해줘`라고 말합니다 → 클로드가 압축을 풀고 [`INSTALL.md`](./INSTALL.md)를 읽어 순서대로 설치합니다
4. 끝나면 Claude Code를 새로 켭니다. `/`를 치면 스킬 목록이 보입니다

손으로 설치하려면 `skills/` 안의 폴더를 `~/.claude/skills/`(윈도우 `%USERPROFILE%\.claude\skills\`)에 복사합니다. Im-not-AI와 MCP는 [`INSTALL.md`](./INSTALL.md) 2·3단계를 따릅니다.

---

## 연구 스킬 29종

| 분류 | 스킬 |
|---|---|
| 연구 시작 | `research-develop` · `research-ideation` · `deep-research` |
| 문헌 조사 | `literature-review` · `gs-search` · `gs-advanced-search` · `gs-cited-by` · `gs-export` · `zotero-obsidian-bridge` |
| 논문 작성 | `academic-paper` · `academic-writing` · `academic-pipeline` · `survey-writing` · `doc-coauthoring` |
| 검토·수정 | `academic-paper-reviewer` · `review-paper` · `paper-self-review` · `review-response` |
| 방법론 | `research-methodology` · `qualitative-research` · `quantitative-analysis` · `systematic-review` · `ethics-review` |
| 분석·종합 | `research-synthesis` · `critical-analysis` |
| 인용·참고문헌 | `bibliography` · `citation-verification` |
| 연구비 | `grant-writing` · `review-grant` |

`gs-*` 스킬은 크롬 확장 Claude in Chrome이 연결되어 있어야 동작합니다.

## 범용 스킬 10종 + 플러그인

| 분류 | 스킬 |
|---|---|
| 문서 읽기·쓰기 | `kordoc` · `hwp` · `hwpx` · `pdf-generation` |
| 발표·도식 | `open-slide-setup` · `claude-design-skill` · `koboyo-icons` · `svg-academic-diagram` |
| 글쓰기 | `writing-anti-ai` · Im-not-AI 플러그인(`humanize-korean` 등) |
| 공공데이터 | `kosis-stats` |

MCP 2종(playwright, korean-law)은 [`MCP_설치.md`](./MCP_설치.md)대로 등록합니다.

각 스킬 설명은 [`사용 전 읽어주세요.txt`](./사용%20전%20읽어주세요.txt)에 있습니다.

---

## 2026년 10월 판에서 바뀐 것

이전 판(73종)에서 44종을 뺐습니다.

- **수집기**: `riss-literature`, `content-access`, `gs-fulltext`, `gs-navigate-pages`
- **같은 일을 하는 스킬이 있어 더 충실한 쪽만 남김(19종)**: `research`, `research-manager`, `brainstorming`, `idea-to-proposal`, `methodology`, `ethics`, `analyze`, `synthesize`, `grant`, `review`, `peer-review`, `paper-reviewing`, `paper-polishing`, `rebuttal`, `obsidian-literature-workflow`, `literature-infrastructure-lab`, `paper-strategist`, `paper-composer`, `hypothesis-testing`
- **인공지능·뇌과학·경제학 전용이거나 LaTeX 전제(11종)**: `ml-paper-writing`, `daily-paper-generator`, `literature-survey`, `paper-triggered-survey`, `citation-assistant`, `results-analysis`, `results-report`, `review-paper-code`, `review-paper-light`, `review-pap`, `poster-slides-maker`
- **폴더가 비었거나 스킬 머리말이 없어 불리지 않던 것(9종)**: `academic-pptx`, `csv-data-summarizer`, `contribution-architect`, `domain-synthesis-architect`, `evidence-rigor-architect`, `meta-analysis-protocol-architect`, `prisma-compliant-systematic-literature-review`, `prisma-publication-architect`, `senior-qualitative-methodologist`
- `writing-anti-ai`는 범용 쪽 판으로 넣었습니다

`academic-pptx`와 `csv-data-summarizer`는 원 저작자 저장소에서 받습니다: [academic-pptx-skill](https://github.com/Gabberflast/academic-pptx-skill), [csv-data-summarizer-claude-skill](https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill)

---

## 함께 보기

- [Claude 연구 활용 가이드](https://claude-guide-f-e-r.vercel.app): 이 스킬들을 쓰는 법을 포함한 교육학 연구자용 Claude Code 가이드
- 각 스킬의 저작권은 원 저작자에게 있습니다. Im-not-AI(epoko77-ai), claude-design-skill(jiji262), hwp·kosis-stats·writing-anti-ai는 MIT 라이선스입니다.
