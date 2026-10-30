---
name: open-slide-setup
description: 발표자료를 새로 만드는 기본 스킬(오픈슬라이드). "PPT 만들어줘", "발표자료 만들어줘", "슬라이드 만들어줘", "덱 만들어줘", "프레젠테이션", "학회 발표", "심사 발표", "회의 발표자료", "presentation", "slides", "deck", "open-slide 설치해줘", "오픈슬라이드" 요청에 먼저 발동한다. 설치가 없으면 설치부터 하고, 있으면 ~/open-slide 아래 프로젝트에서 React 덱을 짜서 화면 검사 뒤 편집용 PPTX(맑은 고딕)와 PDF 두 가지로 내보내 사용자가 정한 폴더에 저장한다(이미지 PPTX는 사용자가 따로 요청할 때만).
---

# open-slide 발표자료 제작 (기본 경로)

발표자료 요청이 오면 이 순서로 한다. 설치가 안 되어 있으면 아래 「open-slide 2.0 설치 안내」를 먼저 한다.

0. **준비**: 검사·내보내기 스크립트는 파이썬 playwright를 쓴다. 없으면 `pip install playwright` 후 `python -m playwright install chromium`.
1. **프로젝트**: `~/open-slide/` 아래 주제별 프로젝트를 쓴다(예: `briefing-deck`, `report-deck`). 새 주제면 `npx -y @open-slide/cli@latest init <이름>`. 구글 드라이브 안에는 만들지 않는다. 첫 실행 때 `npx open-slide sync:skills`.
2. **작성**: 프로젝트의 `.claude/skills/create-slide`, `slide-authoring` 규칙대로 `slides/<id>/index.tsx` 하나에 쓴다. 질문(디자인, 장수, 글 양, 움직임)은 사용자가 이미 정했거나 "알아서"라고 하면 묻지 않고 추천안으로 간다. 발표 대본은 `notes` export에 장별 시간과 함께 쓴다.
   - 글꼴은 `"Malgun Gothic", "Apple SD Gothic Neo", sans-serif`. 본문 26~34px, 각주 22px 이상.
3. **화면 검사**: `npm run dev -- --port <포트>`를 백그라운드로 켜고 `python ~/.claude/skills/open-slide-setup/scripts/shoot.py <포트> <id> <장수> <폴더>`. 장마다 PNG와 넘침 보고가 나온다. 2×2로 이어 붙여 눈으로 보고, 여백이 많으면 글자를 키우고 넘치면 장을 나눈다.
4. **내보내기**: `python ~/.claude/skills/open-slide-setup/scripts/export.py <포트> <id> <폴더>` → `edit.pptx`(편집용). **이미지 PPTX는 기본으로 만들지 않는다**(PDF와 역할이 겹치고 용량만 큼. 사용자가 따로 요청하면 `--image`). 메뉴의 PDF는 인쇄 창이라 헤드리스로 못 받는다.
5. **마감**: 화면 캡처 PNG를 같은 폴더에 두고 `python ~/.claude/skills/open-slide-setup/scripts/finalize.py <폴더> <장수>` → `edit_malgun.pptx`(글꼴을 맑은 고딕으로 교체, 윈도우와 맥 파워포인트 모두 있음), `deck.pdf`(화면 그대로). 한자·가나 0건을 확인한 뒤 사용자 폴더에 한 번에 복사한다.
6. **전달**: 산출물은 편집용 PPTX와 PDF 두 개다. 발표는 PDF가 가장 안전하고, 편집용 PPTX는 파워포인트에서 줄바꿈이 조금 달라질 수 있으니 한 번 열어 보라고 알린다. 덱 원본 경로(`~/open-slide/<프로젝트>/slides/<id>/`)와 다시 켜는 명령도 알린다.

---

# open-slide 2.0 설치 안내

> 이 파일을 클로드(Claude Code)에 넣고 **"이거 뭐야? 설치해줘"** 라고 하면 됩니다.
> 클로드는 아래 「클로드가 할 일」을 순서대로 실행합니다.

## 이게 뭔가요

- **open-slide**는 무료 오픈소스(MIT) 슬라이드 도구입니다. 공식 사이트: https://open-slide.dev
- 순서는 셋입니다.
  1. AI 코딩 도구(클로드 코드·코덱스·커서 등)에게 "발표자료 만들어 줘"라고 하면 슬라이드가 코드로 만들어집니다.
  2. 브라우저 화면에서 마우스로 끌어 옮기고, 글자를 더블클릭해 고칩니다.
  3. **편집 가능한 PPTX**로 내보냅니다. 글자는 글상자, 박스는 도형, 발표자 메모는 슬라이드 노트로 들어갑니다.
- 한계
  - PPTX에는 글꼴 파일이 들어가지 않습니다. 받는 컴퓨터에 그 글꼴이 없으면 다른 글꼴로 바뀝니다.
  - 흐림 같은 효과는 그 요소만 그림으로 들어갑니다.
  - 마우스 편집은 내 컴퓨터에서 개발 서버를 켰을 때만 됩니다.

---

## 클로드가 할 일 (순서대로 실행)

사용자에게 진행 상황을 한 줄씩 알리며 진행한다. 실패하면 멈추고 오류 원문과 함께 알린다.

### 1단계. Node.js 확인

```bash
node -v
```

- **v20.19 이상**이면 다음 단계로 간다.
- 없거나 낮으면 설치한다. 설치 전에 사용자에게 한 번 확인받는다.
  - macOS: Homebrew가 있으면 `brew install node`. 없으면 https://nodejs.org 에서 LTS 설치를 안내한다.
  - Windows: `winget install OpenJS.NodeJS.LTS`. 설치 뒤에는 PowerShell을 새로 열어야 한다.

### 2단계. 작업 폴더 만들기

- 사용자에게 폴더 이름을 묻는다. 답이 없으면 `my-deck`을 쓴다.
- 위치는 **홈 폴더 아래**로 한다(예: `~/open-slide/my-deck`).
- 구글 드라이브·원드라이브 같은 동기화 폴더는 피한다. 수백 MB의 `node_modules`가 동기화된다.

```bash
mkdir -p ~/open-slide && cd ~/open-slide
npx -y @open-slide/cli@latest init my-deck
```

이 명령 하나로 다음이 함께 끝난다. 끝나면 `All set!`이 보인다.

- 폴더 생성과 패키지 설치
- git 초기화
- 에이전트용 스킬(`.agents/skills/`, `.claude/`)과 규칙 파일(`AGENTS.md`, `CLAUDE.md`) 생성

### 3단계. 화면 켜기

```bash
cd ~/open-slide/my-deck
npm run dev
```

- 이 명령은 계속 켜져 있어야 하므로 **백그라운드로 실행**한다.
- `Local http://localhost:5173/`이 뜨면 브라우저로 연다(macOS는 `open http://localhost:5173`).
- 5173번이 쓰이는 중이면 다음 빈 번호로 뜬다. 로그에 찍힌 주소를 쓴다.
- 첫 화면에 예제 덱(`getting-started`)이 보이면 설치 성공이다.

### 4단계. 사용자에게 알려 줄 것

설치가 끝나면 아래 「쓰는 법」을 짧게 요약해 알려 준다. 이어서 첫 덱을 만들지 묻는다.

---

## 쓰는 법

| 하고 싶은 것 | 방법 |
|---|---|
| 새 덱 만들기 | 작업 폴더에서 클로드에게 `/create-slide for "주제, 장수, 글 양, 분위기"`. 분위기·장수·글 양·움직임을 먼저 묻는다 |
| 마우스로 고치기 | 요소 클릭 → 끌기·크기·회전. 글자는 더블클릭(또는 선택 후 Enter). **Cmd/Ctrl + S로 저장**해야 코드에 반영된다 |
| 말로 고치기 | 요소 클릭 → 서식 패널의 Comment에 "제목 더 작게"처럼 적고 저장 → 클로드에게 `/apply-comments` |
| 발표자 메모 | "각 장의 발표 대본을 발표자 메모(notes)에 써 줘" → 발표 모드와 PPTX 슬라이드 노트에 들어간다 |
| PPTX로 받기 | 슬라이드 위쪽 **Export → PPTX**. 모양이 깨지면 이미지 PPTX, PDF, HTML도 같은 메뉴에 있다 |
| 링크로 공유 | `npm run build` → `dist` 폴더를 Vercel·Netlify 같은 무료 호스팅에 올린다 |
| 다시 켜기 | `cd ~/open-slide/my-deck && npm run dev` |

### 기존 HTML 슬라이드를 옮기고 싶을 때

클로드에게 이렇게 시킨다.

> "이 HTML 슬라이드를 open-slide 덱으로 옮겨줘. 문구는 한 글자도 바꾸지 말고, 장 순서와 색도 원본대로."

- 덱은 `slides/<영문-id>/index.tsx` 파일 하나로 만들어진다.
- 화면은 1920×1080 고정이다. 넘치는 부분은 잘리므로, 다 만든 뒤 모든 장이 안 잘렸는지 확인하게 한다.

### 한글 글꼴

- PPTX로 보낼 덱은 **받는 쪽에도 있는 글꼴**로 지정한다(예: Pretendard, 맑은 고딕).
- 내 컴퓨터에만 있는 글꼴을 쓰면, 상대방 파워포인트에서는 다른 글꼴로 바뀐다.

---

## 자주 막히는 곳

| 증상 | 처방 |
|---|---|
| `npx` 명령을 못 찾음 | Node.js 미설치. 1단계로 돌아간다 |
| init 중 버전 오류 | Node가 20.19 미만. LTS로 올린다 |
| 화면이 안 열림 | `npm run dev`가 꺼졌는지 확인. 로그의 실제 포트 번호로 연다 |
| 고쳤는데 저장이 안 됨 | 편집 후 Cmd/Ctrl + S를 눌렀는지 확인 |
| 사파리에서 PDF가 안 됨 | 크롬에서 내보낸다 |
| PPTX 글꼴이 바뀜 | 받는 컴퓨터에 그 글꼴이 없음. 흔한 글꼴로 바꾸거나 이미지 PPTX로 보낸다 |

---

## 이 파일을 스킬로 등록하려면 (선택)

매번 파일을 넣지 않고 "open-slide 설치해줘"라는 말만으로 쓰고 싶을 때 한다.

```bash
mkdir -p ~/.claude/skills/open-slide-setup
cp ~/Downloads/open-slide-2.0-설치.md ~/.claude/skills/open-slide-setup/SKILL.md
```

---

기준: open-slide v2.0 (2026-09-26 공개). 2026-10-02에 macOS에서 위 명령으로 설치·실행을 확인했다(init v2.0.0, dev 서버 v2.0.1).
