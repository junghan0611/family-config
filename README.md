# Family-Config: Actionable Intelligence for Family Life

> "Text as Action. Every heading is executable."

**Family-Config**는 맞벌이 가정을 위한 AI 에이전트 기반 가족 생활 관리 시스템입니다.

## 🎯 핵심 개념

### Actionable Intelligence

전통적인 가족 관리 도구와의 차이:

```
❌ Legacy System: "저장용 문서"
   - 사람이 양식 맞추기 → 재활용 불가
   - 정적 정보 → 행동 불가
   - 분산된 데이터 → 통합 어려움
   
✅ Agent System: "행동 가능한 텍스트"
   - 텍스트 일관성 → 에이전트 이해 가능
   - Actionable Item → MCP로 즉시 실행
   - Property 기반 → Sheet/Ledger/Calendar 연동
   - Git 버전 관리 → 가족 히스토리 영속화
```

### 시간과정신의방 (Time and Mind Room)

- **시간(Time)**: 재현 가능한 환경, 버전 관리, 누적되는 지식
- **정신(Mind)**: 인간지능(Human Intelligence)의 확장
- **방(Room)**: AI Agent와 협업하는 워크스페이스

## 📦 구성 요소

### 영역별 관리 모듈

```
family-config/
├── finance/           # 재무 관리
├── education/         # 교육 관리
├── childcare/         # 육아 관리
├── travel/           # 여행/휴가 관리
├── events/           # 경조사 관리
└── calendar/         # 통합 일정 관리
```

각 영역은:
- **templates/**: 재사용 가능한 Org-mode 템플릿
- **schemas/**: 데이터 구조 정의
- **README.md**: 영역별 사용 가이드

### AI 메모리 시스템 (PARA)

```
memory/
├── projects/         # 활성 프로젝트 (기한 있음)
├── areas/            # 지속적 관심사 (기한 없음)
├── resources/        # 재사용 패턴
└── archives/         # 완료 항목
```

## 🚀 빠른 시작

### 1. 저장소 클론

```bash
git clone https://github.com/junghanacs/family-config.git ~/repos/gh/family-config
cd ~/repos/gh/family-config
```

### 2. 실제 데이터 폴더 생성

```bash
mkdir -p ~/org/family/{finance,education,childcare,travel,events,calendar}
cd ~/org/family
git init
```

### 3. 첫 템플릿 사용

```bash
# 여행 계획 템플릿 복사
cp ~/repos/gh/family-config/travel/templates/trip-planning.org \
   ~/org/family/travel/20251014T120000--여름휴가-제주도__family_travel_active.org
```

### 4. Emacs에서 편집

```bash
emacs ~/org/family/travel/20251014T120000--여름휴가-제주도__family_travel_active.org
```

## 📋 Actionable Item 예시

### Property 기반 실행

```org
* 제주도 항공권 예약 :AGENT:ACTION:
:PROPERTIES:
:AGENT_ACTION: mcp_web_search
:SEARCH_QUERY: 서울-제주 항공권 2025-07-20 4인
:BUDGET: 800000
:DEADLINE: [2025-04-30 Sun]
:STATUS: TODO
:END:

** Agent Instructions
#+begin_src yaml
action: web_search
query: "서울-제주 항공권 2025-07-20 왕복 4명"
budget_max: 800000
preferences:
  - 좌석 인접 배치
  - 아침 출발 (09:00-11:00)
output:
  - format: org_table
  - fields: [airline, departure, price]
#+end_src

** Search Results
[Agent가 실행 후 자동 추가]
```

### MCP 도구 연동

AI Agent (Claude 등)가 자동으로:
1. Property 파싱
2. MCP 도구 실행 (`web_search`)
3. 결과를 Org table로 기록
4. 다음 액션 제안

## 🛠️ 주요 기능

### 1. 재무 관리 (Finance)

- 월별 예산 추적
- 지출 카테고리 분석
- Ledger 통합
- 예산 초과 알림

### 2. 교육 관리 (Education)

- 아이별 학습 계획
- 학원 일정 관리
- 성적 추적
- 교육 자료 추천

### 3. 육아 관리 (Childcare)

- 예방접종 스케줄
- 성장 발달 기록
- 일일 루틴 관리
- 의료 기록

### 4. 여행 관리 (Travel)

- 항공권/숙박 검색 (MCP)
- 일정 자동 생성
- 짐싸기 체크리스트
- 예산 추적

### 5. 경조사 관리 (Events)

- 가족 관계도
- 경조사 알림
- 부조금 가이드
- 과거 기록

### 6. 통합 일정 (Calendar)

- 모든 영역 통합
- Google Calendar 동기화
- 가족 구성원별 뷰
- 충돌 감지

## 🤖 AI Agent 활용

### 일일 루틴

- **06:00**: 오늘 일정 브리핑
- **12:00**: 긴급 알림 체크
- **18:00**: 저녁 준비사항
- **22:00**: 일일 정리

### 주간/월간 리포트

- 예산 사용 분석
- 교육 진도 체크
- 목표 달성도
- 패턴 발견 및 제안

## 📁 파일명 규칙 (Denote)

```
timestamp--한글-제목__family_영역_태그들.org

예시:
20251014T120000--여름휴가-제주도__family_travel_active.org
20251014T120100--월별-예산-2025-10__family_finance_tracking.org
20251014T120200--아이1-학원-스케줄__family_education_child1.org
```

### 태그 시스템

```bash
# Projects (기한 있는 작업)
__active     # 현재 진행 중
__urgent     # 긴급
__blocked    # 차단됨

# Resources
__template   # 템플릿
__pattern    # 패턴

# Archives
__done       # 완료됨
```

## 🏗️ 시간과정신의방: 레이어 아키텍처

### 핵심 철학

> "Config is not just settings. It's a philosophy."
> "Family is not just living together. It's a shared intelligent system."

**시간과정신의방(Time and Mind Room)** 개념:
- **시간(Time)**: 재현 가능한 환경, 버전 관리, 누적되는 가족 히스토리
- **정신(Mind)**: 인간지능(HI) + 인공지능(AI) 협업
- **방(Room)**: AI Agent와 함께 운영하는 가족 운영 공간

### 레이어 구조

```
┌─────────────────────────────────────────────────┐
│  Layer 5: Family Dashboard (가족 대시보드)      │
│  - Org-mode 기반 통합 뷰                        │
│  - 실시간 KPI (예산, 일정, 목표 달성도)         │
│  - 가족 의사결정 지원 시스템                    │
└─────────────────────────────────────────────────┘
                     ↑
┌─────────────────────────────────────────────────┐
│  Layer 4: AI Family Agent (family-config)       │
│  - PARA 메모리 시스템                           │
│    · projects/ (활성 프로젝트)                  │
│    · areas/ (지속적 관심사)                     │
│    · resources/ (재사용 패턴)                   │
│    · archives/ (완료 항목)                      │
│  - Denote naming convention                    │
│  - Git versioning (가족 히스토리 영속화)        │
│  - PM Agent (능동적 관리)                       │
└─────────────────────────────────────────────────┘
                     ↑
┌─────────────────────────────────────────────────┐
│  Layer 3: Domain Configs (영역별 설정)          │
│  - finance/ (재무 관리)                         │
│  - education/ (교육 관리)                       │
│  - childcare/ (육아 관리)                       │
│  - travel/ (여행 관리) ← 여기서 시작!           │
│  - events/ (경조사 관리)                        │
│  - calendar/ (통합 일정)                        │
│                                                 │
│  각 영역: templates/ + schemas/                 │
└─────────────────────────────────────────────────┘
                     ↑
┌─────────────────────────────────────────────────┐
│  Layer 2: Tools & Integrations (도구 통합)      │
│  - MCP 도구 (web_search, calendar, n8n)        │
│  - Google Calendar/Drive API                   │
│  - Emacs/Org-mode (Human Intelligence)         │
│  - Ledger CLI (재무 추적)                       │
│  - ACP/MCP 하이브리드                           │
└─────────────────────────────────────────────────┘
                     ↑
┌─────────────────────────────────────────────────┐
│  Layer 1: Data Infrastructure (데이터 인프라)   │
│  - Git repositories (버전 관리)                 │
│  - Org-mode files (~/org/family/)              │
│  - Denote silo system (일관된 파일명)           │
│  - Backup systems (자동 백업)                   │
└─────────────────────────────────────────────────┘
```

### 데이터 흐름

```
가족 생활 (Family Life)
    ↓
Emacs/Org-mode + AI Agent
    ↓
Property 파싱 (AGENT:ACTION 태그)
    ↓
MCP 도구 실행 (web_search, calendar, n8n, ...)
    ↓
결과를 Org table/Ledger/iCal로 기록
    ↓
~/org/family/ (실제 데이터, Private Git)
    ↓
패턴 발견 및 템플릿화
    ↓
~/repos/gh/family-config/memory/
    ↓
패턴 축적 (resources/)
    ↓
템플릿 개선 (templates/)
    ↓
다음 가족에게 공유 (GitHub Public)
```

### ACP/MCP 통합 전략

```
Emacs (Human Intelligence)
    ↓
ACP (Agent Client Protocol)
    ↓
┌─────────────────────────────────┐
│  AI Agents (Claude, Gemini, …) │
└─────────────────────────────────┘
    ↓
MCP (Model Context Protocol)
    ↓
┌──────────────────────────────────────────┐
│  MCP Tools                               │
│  - mcp__web_search (정보 검색)           │
│  - mcp__n8n (워크플로우 자동화)          │
│  - mcp__playwright (웹 자동화)           │
│  - mcp__git (버전 관리)                  │
│  - mcp__supabase (데이터 쿼리)           │
└──────────────────────────────────────────┘
    ↓
실제 작업 실행 (항공권 검색, 예약, 기록, ...)
    ↓
결과를 Org-mode Property/Table로 저장
```

### -config 생태계 연결

이 프로젝트는 **시간과정신의방** 생태계의 일부입니다:

#### 개인 시스템 (Personal)
- **claude-config**: AI 협업 지휘소 (개인 작업용)
- **nixos-config**: 재현 가능한 OS 환경
- **doomemacs-config**: 터미널 최적화 Emacs
- **emacs-fulllab-config**: 실험실 (Laboratory → Production)
- **zotero-config**: AI 쿼리 가능한 서지 시스템

#### 가족 시스템 (Family)
- **family-config**: 가족 생활 관리 (이 프로젝트)
  - 동일한 철학 (CLAUDE.md 스타일)
  - 동일한 방법론 (Denote + PARA)
  - 동일한 도구 (Emacs + MCP)
  - 독립된 데이터 (~/org/family/)

### 시스템 통합

```
~/claude-config/              (개인 AI 협업)
  ├── CLAUDE.md              (개인 Agent 지침서)
  └── memory/                (개인 메모리)

~/repos/gh/family-config/     (가족 운영)
  ├── FAMILY.md              (가족 Agent 지침서)
  └── memory/                (가족 메모리)

~/org/                        (Denote Silo)
  ├── notes/                 (개인 노트)
  └── family/                (가족 데이터)

~/repos/gh/nixos-config/      (OS 환경)
~/repos/gh/doomemacs-config/  (Emacs 환경)

→ 모두 Git으로 버전 관리
→ 모두 Denote 규칙 준수
→ 모두 AI Agent 친화적
→ 개인/가족 데이터 분리
```

## 📊 기대 효과

### 정량적

- **시간 절약**: 주당 5-10시간 (자동화)
- **비용 절감**: 월 10-20% (예산 최적화)
- **놓친 일정**: 연간 0건 (AI 리마인더)

### 정성적

- **스트레스 감소**: 모든 것이 체계화
- **부부 협업**: 공유된 투명한 시스템
- **가족 기록**: Git으로 영원히 보존
- **의사결정**: 데이터 기반 판단

## 🔐 프라이버시

### 공개 (이 리포지토리)

✅ 템플릿 파일  
✅ 스키마 정의  
✅ 문서화  
✅ 예시 코드  

### 비공개 (개인 관리)

❌ 실제 가족 데이터 (`~/org/family/`)  
❌ 금융 정보  
❌ 개인 식별 정보  
❌ 민감한 일정  

## 📖 문서

- **[FAMILY.md](./FAMILY.md)**: AI Agent 지침서
- **[docs/getting-started.md](./docs/getting-started.md)**: 상세 시작 가이드
- **[docs/agent-guide.md](./docs/agent-guide.md)**: Agent 활용법
- **[docs/mcp-integration.md](./docs/mcp-integration.md)**: MCP 도구 연동

## 🤝 기여

이 프로젝트는 템플릿 저장소입니다. 개선 사항 제안 환영합니다:

1. Fork
2. Feature branch 생성
3. 변경사항 커밋
4. Pull Request

## 📝 라이선스

MIT License

## 👤 작성자

**Junghan Kim** (junghanacs)

- Website: [힣's 디지털가든](https://notes.junghanacs.com)
- GitHub: [@junghanacs](https://github.com/junghan0611)

## 🙏 영감

- **PARA Method**: Tiago Forte
- **Denote**: Protesilaos Stavrou
- **Org-mode**: Carsten Dominik
- **Getting Things Done**: David Allen
- **시간과정신의방**: 개인 컴퓨팅 환경 통합 철학

---

**"Family is not just living together. It's a shared intelligent system."**
