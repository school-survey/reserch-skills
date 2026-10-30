# 설치 런북 (클로드코드가 읽고 실행)

> 이 파일은 **사람이 아니라 클로드코드가 읽고 그대로 실행**하는 설치 지시서다.
> 사용자가 zip을 끌어다 놓고 "이거 설치해줘"라고 하면, 클로드는 압축을 푼 뒤 이 문서의 단계를 위에서부터 차례로 수행한다.
> 모든 명령은 **압축을 푼 `research-skills` 폴더를 현재 작업 폴더로** 두고 실행한다.
> 막히는 단계가 있어도 설치를 멈추지 말고 건너뛴 뒤, 마지막 요약에서 무엇이 빠졌는지 알려준다.

---

## 0단계 · 환경 확인

| 구분 | 윈도우 | 맥 / 리눅스 |
|------|--------|-------------|
| 스킬 폴더 | `%USERPROFILE%\.claude\skills` | `~/.claude/skills` |
| 에이전트 폴더 | `%USERPROFILE%\.claude\agents` | `~/.claude/agents` |
| 셸 | PowerShell | bash / zsh |

선행 도구(없어도 설치는 진행되나, 일부 스킬 실행에 필요):
- **클로드코드 CLI** (필수)
- **Node.js / npm**: kordoc, hwp, open-slide-setup, playwright·korean-law MCP
- **Python 3.10+**: hwpx, kosis-stats, pdf-generation, open-slide-setup(검사·내보내기)

```
node -v
python --version
```

이미 같은 이름의 스킬이 있으면 덮어쓰기 전에 사용자에게 한 번 묻는다.

---

## 1단계 · 스킬 39종 복사

`skills\` 안의 폴더 39개(연구 29종 + 범용 10종)를 사용자 스킬 폴더로 복사한다.

**윈도우 (PowerShell)**
```powershell
$dst = "$env:USERPROFILE\.claude\skills"
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item ".\skills\*" $dst -Recurse -Force
```

**맥 / 리눅스 (bash)**
```bash
mkdir -p ~/.claude/skills
cp -R ./skills/* ~/.claude/skills/
```

---

## 2단계 · Im-not-AI 플러그인 (스킬 3종 + 에이전트 12종)

Im-not-AI는 단일 스킬이 아니라 **플러그인**이다. 스킬만 넣으면 에이전트가 없어 실행되지 않으므로 둘을 함께 넣는다.

**윈도우 (PowerShell)**
```powershell
$sdst = "$env:USERPROFILE\.claude\skills"
$adst = "$env:USERPROFILE\.claude\agents"
New-Item -ItemType Directory -Force $sdst,$adst | Out-Null
Copy-Item ".\Im-not-AI\.claude\skills\*" $sdst -Recurse -Force
Copy-Item ".\Im-not-AI\agents\*"        $adst -Recurse -Force
```

**맥 / 리눅스 (bash)**
```bash
mkdir -p ~/.claude/skills ~/.claude/agents
cp -R "./Im-not-AI/.claude/skills/"* ~/.claude/skills/
cp -R ./Im-not-AI/agents/* ~/.claude/agents/
```

인터넷이 되면 클로드코드 안에서 `/plugin marketplace add epoko77-ai/im-not-ai` → `/plugin install humanize-korean@im-not-ai`로 설치해도 된다(업데이트가 쉽다).

---

## 3단계 · MCP 서버 (playwright · korean-law)

이 폴더의 **`MCP_설치.md`를 읽고 그대로 수행한다.**

- **playwright**: 웹페이지 열기·클릭·캡처. 키 불필요.
- **korean-law**: 한국 법령·조문·판례 원문 조회. 무료 OPEN API 키(OC) 필요. OC가 없으면 건너뛰고 요약에 적는다.

---

## 4단계 · 검증

```
claude mcp list
```

**윈도우**
```powershell
Get-ChildItem "$env:USERPROFILE\.claude\skills" -Directory | Measure-Object | Select-Object Count
Get-ChildItem "$env:USERPROFILE\.claude\agents" -File | Measure-Object | Select-Object Count
```
**맥 / 리눅스**
```bash
ls ~/.claude/skills | wc -l
ls ~/.claude/agents | wc -l
```

이 묶음에서 들어간 스킬은 42개(39종 + humanize 3종), 에이전트는 12개다. 원래 있던 스킬이 있으면 그만큼 더 많다.

---

## 5단계 · 스킬별 추가 준비 (설치 후 요약으로 안내)

| 스킬 | 추가 준비 |
|------|-----------|
| kordoc | `npm install -g kordoc`. 한글·PDF·엑셀·워드를 읽는 엔진 |
| hwp | 첫 실행 때 `npx kordoc` 자동 내려받음 |
| hwpx | `pip install python-hwpx` (Python 3.10+). 3.9 이하면 워드(.docx)로 대신 만든다 |
| open-slide-setup | Node.js 20.19 이상, `pip install playwright` 후 `python -m playwright install chromium`. open-slide 자체는 처음 "PPT 만들어줘"라고 할 때 스킬이 설치한다(동기화 폴더 밖에) |
| pdf-generation | pandoc + xelatex(윈도우 MiKTeX / 맥 MacTeX). 없으면 클로드코드 내장 PDF 기능으로 대신 |
| kosis-stats | KOSIS 무료 인증키 신청 후 등록(스킬 폴더의 SKILL.md 참고) |
| gs-search · gs-advanced-search · gs-cited-by · gs-export | 구글 스칼라를 브라우저로 조회한다. 크롬 확장 **Claude in Chrome**이 연결되어 있어야 한다. gs-export는 Zotero 데스크톱도 켜져 있어야 한다 |
| zotero-obsidian-bridge | Zotero와 Obsidian 볼트가 있어야 한다 |

나머지 연구 스킬은 추가 설치 없이 바로 동작한다.

**참고**: 워드·엑셀·파워포인트·PDF를 만드는 기본 기능은 클로드코드에 내장되어 있어 이 묶음에 넣지 않았다.

---

## 6단계 · 마지막 요약 (사용자에게 보고)

1. 복사된 스킬 개수와 에이전트 개수
2. 등록된 MCP 목록
3. 건너뛴 항목과 이유, 사용자가 할 일(예: OC 발급, Node.js 설치, Claude in Chrome 연결)
4. "클로드코드를 새로 켜 주세요" 한 줄
