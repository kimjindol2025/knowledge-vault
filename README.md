# Knowledge Vault: AI-Optimized Obsidian System

**완전 자동화된 AI 지식 관리 시스템** - Claude Code + agent-reach + Obsidian + MCP

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![MIT License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 📋 개요

우리의 모든 작업과 학습 내용을 상호 연결된 하나의 지식 시스템으로 관리합니다.

```
Claude Code (AI)
    ↓ (agent-reach)
정보 수집 (YouTube, GitHub, Web)
    ↓
자동 메모 생성
    ↓
자동 링크 생성
    ↓
Obsidian Vault (지식 시스템)
    ↓
웹 인터페이스 & 그래프 뷰
```

## 🚀 빠른 시작

### 1. Obsidian에서 열기

```bash
# Obsidian 다운로드: https://obsidian.md
# 앱 실행 → "Open folder as vault" → /home/kim/OurKnowledgeVault
```

### 2. 웹 인터페이스 사용

```bash
python3 vault_server.py
# 브라우저: http://localhost:8000
```

### 3. 자동 메모 생성

```bash
bash auto_generate_notes.sh
```

## 📂 포함된 파일

### 코드 파일

| 파일 | 설명 |
|------|------|
| `obsidian_mcp_server.py` | MCP 서버 - Vault 제어 API |
| `vault_server.py` | 웹 서버 - 브라우저 인터페이스|
| `auto_generate_notes.sh` | 자동화 스크립트 |

### 메모 파일

```
projects/          # 완성된 프로젝트
├── _index.md
├── codex-image-generation.md
└── obsidian-mcp-integration.md

tools/            # 사용 중인 도구
├── agent-reach.md
└── claude-code.md

concepts/         # 개념 정리
└── multi-agent-workflow.md

guides/           # 가이드 (추가 예정)
youtube/          # 영상 자료 (추가 예정)
github/           # GitHub 분석 (추가 예정)
resources/        # 참고 자료 (추가 예정)
```

## 🔧 코드 사용법

### `obsidian_mcp_server.py` - MCP 서버

**메모 읽기:**
```python
from obsidian_mcp_server import ObsidianMCPServer

vault = ObsidianMCPServer("/home/kim/OurKnowledgeVault")
content = vault.read_note("projects/codex-image-generation.md")
```

**새 메모 생성:**
```python
vault.create_note(
    title="새로운 개념",
    content="메모 내용...",
    folder="concepts"
)
```

**메모 간 링크 생성:**
```python
vault.create_link("projects/_index.md", "concepts/new-concept.md")
```

**태그 추가:**
```python
vault.add_tags("concepts/new-concept.md", ["ai", "automation"])
```

**메모 검색:**
```python
results = vault.search_notes("Python")
```

**그래프 조회:**
```python
graph = vault.get_graph()
print(f"노드: {len(graph['nodes'])}개, 링크: {len(graph['links'])}개")
```

**통계:**
```python
stats = vault.get_stats()
# {total_notes: int, total_words: int, total_links: int}
```

### `vault_server.py` - 웹 서버

**실행:**
```bash
python3 vault_server.py
# http://localhost:8000 에서 확인
```

**API 엔드포인트:**

```bash
# 메모 목록
curl http://localhost:8000/api/notes

# 메모 읽기
curl http://localhost:8000/api/read/projects/codex-image-generation.md

# 그래프 데이터
curl http://localhost:8000/api/graph

# 통계
curl http://localhost:8000/api/stats
```

### `auto_generate_notes.sh` - 자동화

**실행:**
```bash
bash auto_generate_notes.sh
```

**작업 내용:**
1. MCP 서버 검증
2. Vault 통계 확인
3. 새 메모 생성 (예제)
4. 자동 링크 생성
5. 자동 태그 추가
6. 그래프 분석

## 📝 메모 형식

### YAML Frontmatter

```markdown
---
title: "메모 제목"
type: "프로젝트|도구|개념|가이드"
status: "✅ 완료|🔄 진행 중|⏳ 예정"
date: "2026-07-03"
tags: ["태그1", "태그2"]
ai_summary: "한 문장 요약"
priority: "🔴 핵심|🟡 중요|🟢 선택"
---

# 메모 제목

## 개요
메모 내용...

## 관련 메모
- [[메모명1]]
- [[메모명2]]
```

### 양방향 링크

```markdown
[[메모명]]  # Obsidian에서 클릭 가능
```

## 📊 웹 인터페이스

http://localhost:8000 에서:

- 📄 **메모 목록** - 모든 메모 브라우징
- 🔗 **그래프 뷰** - 지식 네트워크 시각화
- 📊 **통계** - 메모/링크/단어 수
- 🔍 **검색** - 메모 검색 및 상세 보기

## 🔄 워크플로우

```
Claude Code 요청
    ↓
agent-reach (정보 수집)
    ↓
Claude Code (메모 작성)
    ↓
obsidian_mcp_server.py (저장)
    ↓
Obsidian (확인)
```

## 🎯 특징

✅ **완전 자동화** - Claude Code와 직접 연동  
✅ **양방향 링크** - 메모 간 상호 연결  
✅ **그래프 뷰** - 지식 네트워크 시각화  
✅ **메타데이터** - YAML 기반 정보 관리  
✅ **API 제공** - 프로그래밍으로 제어 가능  
✅ **웹 인터페이스** - 브라우저에서 확인  
✅ **MCP 준비** - Claude Code 완벽 통합 준비  

## 📈 통계

```
메모: 4개
단어: ~1000개
링크: ~10개
폴더: 7개 (projects, tools, concepts, guides, youtube, github, resources)
```

## 🚀 다음 단계

- [ ] 모든 가이드 메모 추가
- [ ] YouTube 자료 정리
- [ ] GitHub 저장소 분석
- [ ] MCP를 Claude Code에 등록
- [ ] Obsidian Publish로 웹 공개
- [ ] 자동 메모 생성 자동화

## 📚 관련 문서

- [Obsidian 사용법](https://help.obsidian.md)
- [MCP 프로토콜](https://modelcontextprotocol.io)
- [agent-reach](https://github.com/Panniantong/Agent-Reach)

## 📞 사용 방법

```bash
# 웹 서버 시작
python3 vault_server.py
# → http://localhost:8000

# 자동화 실행
bash auto_generate_notes.sh

# MCP 테스트
python3 obsidian_mcp_server.py
```

---

**Made with ❤️ by Claude Code**  
*Claude Code + agent-reach + Obsidian + MCP*
