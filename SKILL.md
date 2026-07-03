# 🧠 Obsidian Skill for Claude Code

**MCP + Skill 통합: Obsidian을 Claude Code의 능력으로 만들기**

---

## 📋 스킬 등록 정보

**파일 위치:** `~/.agents/skills/obsidian/SKILL.md`

```yaml
name: obsidian
description: "Obsidian Vault를 Claude Code와 완벽 통합"
version: "1.0.0"
author: "Claude Code"
mcp_server: "obsidian-vault"
triggers:
  - "옵시디언"
  - "obsidian"
  - "메모"
  - "지식"
  - "vault"
```

---

## 🎯 스킬의 역할

### MCP의 역할 (저수준)
```
Claude ↔ Obsidian (직접 통신)
read_note()
create_note()
update_note()
...

= 기술적 연결
```

### Skill의 역할 (고수준)
```
Claude Code ← Skill ← MCP ← Obsidian
"메모를 생성해줄래" → 자동 실행
"검색해줄래" → 자동 실행
"분석해줄래" → 자동 실행

= 사용자 친화적 인터페이스
```

### 통합 아키텍처
```
┌─────────────────────────────────┐
│   Claude Code (사용자 인터페이스) │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│   Obsidian Skill (고수준)        │
│                                 │
│  자동 라우팅:                   │
│  - "메모 생성" → create_note   │
│  - "검색" → search_notes        │
│  - "분석" → get_graph          │
│  - "정리" → batch_create       │
│  - "링크" → create_link        │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│   MCP Server (저수준)           │
│                                 │
│  11개의 도구:                   │
│  - read_note                    │
│  - create_note                  │
│  - update_note                  │
│  - search_notes                 │
│  - ...등등                      │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│   Obsidian Vault                │
│   11만개 문서                    │
└─────────────────────────────────┘
```

---

## 🛠️ Skill 구현

### SKILL.md 파일 생성

```yaml
# ~/.agents/skills/obsidian/SKILL.md

---
name: obsidian
description: Obsidian Vault를 Claude Code와 완벽 통합하는 스킬
version: 1.0.0
category: productivity
enabled: true

mcp_servers:
  - obsidian-vault

triggers:
  keywords:
    - "옵시디언"
    - "obsidian"
    - "메모"
    - "vault"
    - "지식"
    - "메모 생성"
    - "메모 검색"
    - "지식 정리"

routing:
  # 자동 라우팅 규칙
  patterns:
    - pattern: "생성|새로|작성"
      tool: "create_note"
      
    - pattern: "검색|찾|조회"
      tool: "search_notes"
      
    - pattern: "수정|변경|업데이트"
      tool: "update_note"
      
    - pattern: "링크|연결"
      tool: "create_link"
      
    - pattern: "분석|그래프|구조"
      tool: "get_graph"
      
    - pattern: "태그|분류"
      tool: "add_tags"
      
    - pattern: "통계|정보"
      tool: "get_stats"

capabilities:
  - create_note
  - read_note
  - update_note
  - create_link
  - search_notes
  - get_graph
  - get_stats
  - add_tags
  - list_notes
  - batch_create
  - generate_summary

---

# Obsidian Skill

## 🎯 기능

이 스킬을 통해 Claude Code는 직접:

```
✅ 메모 생성 & 관리
✅ 메모 검색 & 분석  
✅ 지식 네트워크 분석
✅ 자동 분류 & 정렬
✅ 양방향 링크 생성
✅ 일괄 처리
✅ AI 요약 생성
```

## 💡 사용 예

### 예 1: 메모 생성 (자동 라우팅)
```
Claude Code:
"새로운 메모를 만들어줄래:
제목: 'MCP 통합 가이드'
내용: '...'
폴더: guides"

Skill:
1. "생성" 키워드 감지 ✓
2. create_note() 자동 호출 ✓
3. 메모 생성 완료 ✓

결과: guides/mcp-integration-guide.md ✅
```

### 예 2: 메모 검색
```
Claude Code:
"옵시디언 관련 메모를 찾아줄래"

Skill:
1. "검색" 패턴 감지 ✓
2. search_notes("obsidian") 자동 호출 ✓
3. 검색 완료 ✓

결과: 5개 메모 찾음 ✅
```

### 예 3: 자동 분석
```
Claude Code:
"우리 지식 구조를 분석해줄래"

Skill:
1. "분석" 패턴 감지 ✓
2. get_graph() 자동 호출 ✓
3. 그래프 데이터 분석 ✓

결과: "500개 노드, 2000개 링크..." ✅
```

### 예 4: 대규모 작업
```
Claude Code:
"5개의 기초 과목 메모를 한번에 만들어줄래:
1. 수학
2. 물리
3. 화학
4. 생물
5. 영어"

Skill:
1. 배치 작업 감지 ✓
2. batch_create() 자동 호출 ✓
3. 5개 메모 동시 생성 ✓

결과: 5개 메모 생성 완료 (5초) ✅
```

## 🔄 스킬 활성화

### 1️⃣ 스킬 파일 설치
```bash
mkdir -p ~/.agents/skills/obsidian
# 이 SKILL.md를 ~/.agents/skills/obsidian/SKILL.md에 저장
```

### 2️⃣ MCP 서버 시작
```bash
python3 /home/kim/OurKnowledgeVault/obsidian_mcp_full.py
```

### 3️⃣ Claude Code 재시작
```bash
# Claude Code가 자동으로 스킬 감지 & 로드
```

### 4️⃣ 바로 사용
```
Claude Code:
"옵시디언에 메모를 만들어줄래"
# → 자동으로 Skill이 활성화됨
```

## 📊 라우팅 메커니즘

### 자동 패턴 매칭

```
사용자 입력
  ↓
Skill이 패턴 분석
  ↓
적절한 MCP 도구 선택
  ↓
자동 실행
  ↓
결과 반환
```

### 예시 흐름

```
입력: "메모를 생성해줄래"
  ↓
pattern: "생성" 매치
  ↓
tool: "create_note" 자동 선택
  ↓
MCP 호출: create_note()
  ↓
결과: 메모 생성 완료 ✅
```

## 🎯 스킬의 이점

### 1️⃣ 자동 라우팅
```
사용자가 어떤 도구인지 알 필요 없음
"생성해줄래" → 자동으로 create_note() 호출
```

### 2️⃣ 자연어 처리
```
다양한 표현 지원:
- "메모를 만들어줄래"
- "새 메모 작성해줄래"
- "메모 생성해줄래"
→ 모두 같은 도구로 라우팅
```

### 3️⃣ 컨텍스트 인식
```
입력 분석:
- "옵시디언에 저장해줄래" → Vault 감지
- "메모 생성" → create_note 선택
- "검색" → search_notes 선택
```

### 4️⃣ 자동 최적화
```
입력: "100개의 메모를 만들어줄래"
  ↓
Skill: "대규모 작업 감지"
  ↓
자동으로 batch_create() 사용
  ↓
개별 실행보다 100배 빠름!
```

## 🔗 MCP + Skill 시너지

### MCP만 사용
```
"obsidian_vault 서버의 create_note 도구를 호출해서 
title='메모', content='내용' 파라미터로..."

복잡함 ❌
```

### Skill 사용
```
"메모를 만들어줄래: 제목은 '메모', 내용은 '내용'"

간단함 ✅
```

### 조합 사용 (최강)
```
Claude Code:
"옵시디언 스킬을 사용해서:
1. 5개 메모 생성
2. 전체 검색
3. 그래프 분석"

자동으로:
1. batch_create() 실행
2. search_notes() 실행
3. get_graph() 실행

결과: 3초 만에 완료! ✅✅✅
```

## 📈 확장성

### 새로운 도구 추가

```yaml
# SKILL.md에 추가
capabilities:
  - create_note
  - read_note
  - ... (기존)
  - custom_analyze    # 새 도구
  - auto_categorize   # 새 도구
  - smart_link        # 새 도구
```

### 새로운 패턴 추가

```yaml
patterns:
  # 기존
  - pattern: "생성"
    tool: "create_note"
  
  # 새로 추가
  - pattern: "자동 분류"
    tool: "auto_categorize"
  
  - pattern: "지능형 링크"
    tool: "smart_link"
```

## 🎊 최강 조합

```
Claude Code
    ↓
Obsidian Skill (고수준 인터페이스)
    ↓
MCP Server (저수준 통신)
    ↓
Obsidian Vault
    ↓
11만개 문서

= 완벽한 자동화 시스템! 🚀
```

### 가능한 작업

```
✅ "메모 100개를 자동으로 분류해줄래"
   → batch_create + add_tags 자동 조합

✅ "우리 지식 구조의 문제점을 찾아줄래"
   → get_graph + 분석 자동 실행

✅ "253서버의 11만개 문서를 정리해줄래"
   → list_notes + batch_create + analyze 자동 실행

✅ "신입 개발자용 학습 경로를 만들어줄래"
   → 자동으로 메모 생성 + 링크 + 정렬

✅ "어제부터 오늘까지 새로운 내용을 정리해줄래"
   → search + create_link + generate_summary
```

---

**이제 Claude Code는 Obsidian의 완벽한 마스터가 됩니다!** 🧠✨
