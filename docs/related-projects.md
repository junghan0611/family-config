# Related Projects: Family Life Management Systems

**작성일**: 2025-10-14  
**조사 출처**: Claude Web Research  
**목적**: Family-Config 프로젝트와 유사한 GitHub 프로젝트 조사 및 인사이트 도출

---

## 🔍 조사 개요

**핵심 발견**: "Life OS" 또는 "Personal Operating System" 개념으로 많은 개발자들이 비슷한 고민을 했습니다.

---

## 🌟 최고 추천 프로젝트들

### 1. Monica - Personal Relationship Management ⭐⭐⭐⭐⭐

- **Stars**: 23,504개 (가장 성숙한 프로젝트!)
- **GitHub**: https://github.com/monicahq/monica
- **언어**: PHP (Laravel)
- **철학**: "Personal CRM for your friends and family"

**당신 프로젝트와의 연관성**:
- 가족과 친구들과의 상호작용을 기록하고 조직화하는 웹 애플리케이션
- 경조사 관리에 완벽
- 생일, 기념일 자동 리마인더
- 대화 로그, 선물 추적, 관계 노트

**특징**:
- Self-hosted 가능
- 오픈소스 (MIT)
- Docker 지원
- RESTful API

**적용 가능성**: events/ 모듈 구현 시 참고

---

### 2. PersonalAgent - Priority-Based Calendar ⭐⭐⭐⭐⭐

- **GitHub**: https://github.com/macizomedia/personalagent
- **언어**: Python
- **철학**: "Family events take priority, work adapts to life"

**당신 프로젝트와의 연관성** (거의 똑같은 접근!):
- 우선순위 기반 멀티 캘린더 관리 (가족 > 개인 > 업무)
- AI 기반 작업 자동화
- Google Calendar 통합
- Profile 시스템 (family/personal/work)
- 충돌 감지 및 해결

**핵심 기능**:
```python
# Priority Hierarchy
1. Family Profile (Priority 1) - 최우선, 불변
2. Personal Profile (Priority 2) - 가족과 공존 가능
3. Work Profile (Priority 3) - 여유 시간만 채움
```

**적용 가능성**: calendar/ 모듈의 핵심 로직으로 채택 가능

---

### 3. Personal Management System ⭐⭐⭐⭐

- **Stars**: 3,586개
- **GitHub**: https://github.com/Volmarg/personal-management-system
- **언어**: PHP (Symfony)
- **철학**: "Your central point for managing personal data"

**당신 프로젝트와의 연관성**:
- 모듈식 구조 (당신의 -config 생태계와 유사!)
- Self-hosted
- 개인 데이터 중앙 관리

**모듈들**:
- 📅 Schedules (반복 일정)
- 💸 Payments (예산 관리)
- 📞 Contacts (연락처)
- 🔑 Passwords
- 🌴 Travels (여행 계획)
- 📷 Images/Files/Video
- 📑 Reports

**적용 가능성**: 전체 아키텍처 참고, 모듈 분리 전략

---

### 4. Firefly III - Personal Finance Manager ⭐⭐⭐⭐

- **Stars**: 17,000+ 
- **GitHub**: https://github.com/firefly-iii/firefly-iii
- **언어**: PHP (Laravel)

**당신 프로젝트의 재무 모듈 참고**:
- Double-entry bookkeeping (복식부기)
- Piggy banks for savings goals
- Budget, category, tag 지원
- Self-hosted
- REST API

**적용 가능성**: finance/ 모듈, Ledger CLI 통합 참고

---

### 5. family-organizer ⭐⭐⭐

- **GitHub**: https://github.com/fivestones/family-organizer
- **언어**: TypeScript
- **철학**: "An organizer for our family"

**당신 프로젝트와의 연관성**:
- 가족 구성원별 "봉투(envelopes)" 시스템으로 자금 관리
- 집안일(chores) 추적 시스템
- 용돈 관리 및 자동 계산
- InstantDB로 실시간 동기화
- Offline-first

**적용 가능성**: childcare/ 모듈, 집안일 관리

---

### 6. Facto - Family Accounting Tool ⭐⭐⭐

- **GitHub**: https://github.com/nymanjens/facto
- **언어**: Scala

**특징**:
- 가족 간 내부 부채 계산 (Alice가 공동 비용 지불 → 가족이 Alice에게 빚)
- Cash flow 분석으로 예상치 못한 지출 감지
- 공동 계정(common account) 관리

**적용 가능성**: finance/ 모듈, 가족 간 정산 로직

---

### 7. Life OS 시리즈 ⭐⭐⭐

여러 개발자들이 만든 "Life Operating System" 프로젝트들:

**jornados-life-management (Claruva OS)**
- **GitHub**: https://github.com/heynzar/jornados-life-management
- Task management, Goal tracking, Habit tracker
- Next.js + TypeScript

**다른 Life OS 프로젝트들**:
- Orbithic (Personal Transformation OS)
- AxionOS-Alpha (AI-powered OS)
- 4Eunoia (Next.js productivity system)

**적용 가능성**: 전체 시스템 철학, Life OS 개념

---

### 8. PiggyVault - Family Finance

- **GitHub**: https://github.com/piggyvault/piggyvault
- 가족 재무 관리 앱
- Flutter 모바일 앱
- Multi-tenant 지원

**적용 가능성**: 모바일 앱 확장 시 참고

---

### 9. CRMx - Micro CRM ⭐⭐

- **Stars**: 107개
- **GitHub**: https://github.com/luckyshot/CRMx
- **언어**: PHP

**특징**:
- 초경량 CRM, 단일 PHP/JS/CSS 파일
- config.php에서 모든 설정 (당신의 철학과 유사!)
- 플러그인 시스템
- RESTful API

**적용 가능성**: Config-as-Code 철학 참고

---

## 🎯 Family-Config에 적용할 인사이트

### 1. Priority-Based System (PersonalAgent)

```python
# family-meta-config/profiles.py
PROFILES = {
    'family': {
        'priority': 1,  # 최우선
        'immovable': True,  # 절대 변경 불가
        'calendars': ['family@gmail.com']
    },
    'personal': {
        'priority': 2,
        'immovable': False,
        'calendars': ['personal@gmail.com']
    },
    'work': {
        'priority': 3,
        'immovable': False,
        'calendars': ['work@company.com']
    }
}
```

**적용 방법**: calendar/ 모듈에 우선순위 시스템 구현

---

### 2. Config-as-Code 철학 (CRMx)

```yaml
# family-meta-config/config.yaml
family:
  profiles:
    - name: dad
      role: parent
    - name: mom
      role: parent
    - name: child1
      role: child
      age: 8
  
  modules:
    - finance
    - education
    - travel
  
  automation:
    reminders: true
    budget_alerts: true
```

**적용 방법**: FAMILY.md와 통합, 설정 중앙화

---

### 3. 모듈식 아키텍처 (Personal Management System)

```
family-config/
├── core/
│   ├── module_loader.py
│   └── config_manager.py
├── modules/
│   ├── finance/
│   │   ├── __init__.py
│   │   ├── budget.py
│   │   └── tracking.py
│   ├── education/
│   ├── travel/
│   └── events/
└── templates/
```

**적용 방법**: 현재 구조를 Python/TypeScript 모듈로 확장

---

### 4. 관계 관리 로직 (Monica)

```yaml
# events/templates/ceremony-tracking.org
* 경조사 추적
:PROPERTIES:
:PERSON: 사촌 동생
:RELATION: family
:EVENT_TYPE: wedding
:DATE: [2025-12-15 Sun]
:GIFT_AMOUNT: 100000
:GIFT_TYPE: cash
:NOTES: 축의금은 현금 봉투로
:PAST_EVENTS: 2023년 약혼식 (5만원)
:END:
```

**적용 방법**: events/ 모듈에 관계 기반 추적 시스템

---

### 5. 가족 정산 로직 (Facto)

```python
# finance/debt_tracker.py
class FamilyDebtTracker:
    def calculate_debt(self):
        """
        공동 지출을 누가 먼저 냈는지 추적하고
        가족 간 정산 금액 자동 계산
        """
        pass
    
    def suggest_settlement(self):
        """최소 거래로 정산 제안"""
        pass
```

**적용 방법**: finance/ 모듈에 가족 정산 기능

---

## 💡 차별화 포인트

### Family-Config가 더 나은 점

1. **Config 생태계 통합**
   - 기존: 독립적인 웹 앱
   - Family-Config: nixos-config, doomemacs-config와 통합

2. **AI-First Approach**
   - 기존: AI는 부가 기능
   - Family-Config: MCP + Claude를 핵심에 배치

3. **Git-Based Memory**
   - 기존: 데이터베이스만
   - Family-Config: Git으로 모든 가족 히스토리 버전 관리

4. **PARA 방법론**
   - 기존: 단순 카테고리
   - Family-Config: Projects/Areas/Resources/Archives

5. **Denote 네이밍**
   - 기존: 일반 파일명
   - Family-Config: `20251014T090000--제주도여행__travel_family.md`

6. **Org-mode 통합**
   - 기존: 웹 UI만
   - Family-Config: Emacs/Org-mode 네이티브

7. **계층적 에이전트**
   - 기존: 단일 애플리케이션
   - Family-Config: Meta Agent ↔ Domain Agents

---

## 🚀 실행 계획

### Phase 1: 학습 및 프로토타입 (1-2주)

```bash
# 1. PersonalAgent 코드 리뷰
git clone https://github.com/macizomedia/personalagent
cd personalagent
# Priority system 로직 학습

# 2. Monica 로컬 설치
docker run -d \
  -p 8080:80 \
  -v monica_data:/var/www/html/storage \
  monicahq/monica
# 경조사 관리 UI/UX 체험

# 3. Firefly III 설치
docker run -d \
  -p 8081:80 \
  fireflyiii/core:latest
# 재무 관리 워크플로우 학습
```

### Phase 2: 핵심 기능 구현 (2-4주)

- [ ] Priority-based calendar system
- [ ] 경조사 관계 추적 시스템
- [ ] 가족 정산 로직
- [ ] Google Calendar MCP 통합

### Phase 3: 모듈 확장 (진행 중)

- [X] travel/ 모듈 (진행 중)
- [ ] finance/ 모듈 (Firefly III 참고)
- [ ] events/ 모듈 (Monica 참고)
- [ ] education/ 모듈
- [ ] childcare/ 모듈

---

## 📚 추가 리소스

### Awesome Lists

- **awesome-selfhosted**: https://github.com/awesome-selfhosted/awesome-selfhosted
  - Calendar & Contacts 섹션
  - Money, Budgeting & Management 섹션
  - 참고할 self-hosted 도구들 총망라

### 관련 검색어

- "personal operating system github"
- "family life management"
- "life os"
- "personal crm"
- "self-hosted family organizer"

---

## 🎨 영감을 주는 Quote

> "Claruva OS Life Management is built to empower individuals to take control of their lives"

> "Family events take priority, work adapts to life" - PersonalAgent

> "Monica is not a social network. It's designed to be the opposite: it's for your eyes only"

> "Config is not just settings. It's a philosophy" - Family-Config

---

## 🔗 관련 문서

- [[file:../README.md][Family-Config README]]
- [[file:../FAMILY.md][FAMILY.md - Agent 지침서]]
- [[file:~/repos/gh/meta-config/README.org][Meta-Config: 계층적 에이전트 아키텍처]]

---

**마지막 업데이트**: 2025-10-14  
**조사자**: Claude Web + junghanacs  
**상태**: 🟢 활성 - 지속적 업데이트 중
