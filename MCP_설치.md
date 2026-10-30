# MCP 서버 설치 지시서 (클로드코드가 읽고 실행)

> INSTALL.md 3단계에서 이 문서를 불러 읽는다.
> MCP는 스킬이 아니라 **클로드코드에 붙는 외부 도구 서버**다. 스킬 폴더에 복사하는 방식이 아니라
> `claude mcp add` 명령으로 등록하고, **등록 후 클로드코드를 새로 켜야** 도구가 뜬다.
>
> 등록 범위는 모두 `-s user`(사용자 전역)로 한다. 이렇게 해야 어느 폴더에서 클로드코드를 켜도 쓸 수 있다.

---

## 목록

| MCP | 용도 | API 키 | 선행 조건 |
|-----|------|--------|-----------|
| playwright | 웹페이지 열기·클릭·입력·스크린샷·데이터 수집 | 불필요 | Node.js |
| korean-law | 한국 법령·조문·판례 원문 조회 | 필요(무료) | Node.js |

Node.js가 없으면 두 MCP 모두 설치할 수 없다. 그 경우 설치를 멈추지 말고 건너뛴 뒤,
마지막 요약에서 "Node.js 설치 후 MCP_설치.md만 다시 실행"이라고 안내한다.

---

## A · playwright MCP (권장 · 키 불필요)

브라우저를 클로드가 직접 조작하게 해 주는 마이크로소프트 공식 MCP다.
학회 공고 수집, 포털 반복 조회, 만든 웹페이지 확인 등에 쓴다.

### A-1. Node.js 확인

```
node -v
```
버전이 나오지 않으면 https://nodejs.org 에서 LTS를 설치하도록 안내하고, 이 절은 건너뛴다.

### A-2. 브라우저 내려받기

첫 실행 때 크로미움이 필요하다. 미리 받아 두면 처음 사용할 때 멈추지 않는다.

```
npx -y playwright install chromium
```

### A-3. MCP 등록

```
claude mcp add -s user playwright -- npx -y @playwright/mcp@latest
```

### A-4. 확인

```
claude mcp list
```
목록에 `playwright`가 보이면 성공이다. 클로드코드를 새로 켠 뒤
"이 사이트 열어서 화면 캡처해줘" 같은 요청에 브라우저 도구가 뜬다.

> 이미 `playwright`가 등록되어 있으면 다시 등록하지 말고 그대로 둔다.
> 다시 깔아야 하면 `claude mcp remove -s user playwright` 후 A-3을 실행한다.

---

## B · korean-law MCP (선택 · 무료 API 키 필요)

한국 법령·시행령·조문·판례 원문을 조회한다. 국가법령정보 공동활용 OPEN API 키(OC)가 있어야 동작한다.

### B-1. 패키지 설치

```
npm install -g korean-law-mcp
```

### B-2. API 신청 페이지 열기

사용자에게 "korean-law는 무료 API 신청이 필요합니다. 신청 페이지를 열어 드릴게요"라고 말하고 실행한다.

윈도우:
```powershell
Start-Process "https://open.law.go.kr"
```
맥:
```bash
open "https://open.law.go.kr"
```

### B-3. OC 값 확인

위 사이트에서 회원가입·로그인 후 OPEN API 활용을 신청한다.
발급되는 **OC 값은 가입한 이메일의 @ 앞부분**이다. (예: `hong@abc.com` → OC는 `hong`)

### B-4. MCP 등록

사용자에게 OC 값을 물어본 뒤, 받은 값을 넣어 등록한다.

```
claude mcp add -s user korean-law -e LAW_OC=여기에_발급받은_OC -- korean-law-mcp
```

### B-5. 확인

```
claude mcp list
```

> OC 값을 아직 못 받았으면 B절 전체를 건너뛰고, 마지막 요약에서
> "korean-law는 API 신청 후 MCP_설치.md의 B절만 다시 실행"이라고 안내한다.

---

## 마무리 안내 (설치 후 사용자에게 전달)

- MCP는 **클로드코드를 새로 켜야** 반영된다.
- 등록 상태는 언제든 `claude mcp list` 로 확인한다.
- 회사·학교 보안망에서 `npx` 가 막히면 MCP 등록이 실패할 수 있다. 그때는 개인 네트워크에서 재시도한다.
