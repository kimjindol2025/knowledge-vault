---
title: "Agent-Reach: AI 인터넷 접근"
type: "도구"
version: "v1.5.0"
status: "✅ 설치 완료"
tags: ["ai-tools", "web-scraping", "automation", "claude-code"]
channels_active: "5/15"
ai_summary: "Agent-reach는 15개+ 플랫폼에서 정보를 수집하는 CLI 도구. API 비용 0원, Claude Code와 완벽 통합."
---

# Agent-Reach: AI를 위한 인터넷 접근

## 개요
[[Claude Code]]가 인터넷의 모든 정보에 접근할 수 있도록 하는 도구

## 주요 특징
- 15개+ 플랫폼 지원
- API 비용 0원
- Self-healing router (차단 시 자동 우회)
- [[Claude Code]] 완벽 통합

## 활성화된 채널 (5/15)
- ✅ YouTube (yt-dlp)
- ✅ V2EX (API)
- ✅ RSS/Atom
- ✅ Web Search (Exa)
- ✅ Web Reader (Jina)

## 가능한 작업
- [[YouTube 자막 추출]]
- [[GitHub 저장소 분석]]
- [[웹 의미론적 검색]]
- [[V2EX 커뮤니티 검색]]
- [[웹페이지 읽기]]

## 사용 예
```bash
# YouTube 자막 추출
yt-dlp --write-auto-subs --sub-lang ko https://youtu.be/VIDEO_ID

# V2EX 검색
curl "https://www.v2ex.com/api/topics/hot.json"

# 웹 검색 (Exa)
mcporter call 'exa.web_search_exa(query: "검색어", numResults: 5)'
```

## 관련 메모
- [[Claude Code]]
- [[Web Automation]]
- [[Information Gathering]]

## 리소스
- **GitHub**: https://github.com/Panniantong/Agent-Reach
- **Guide**: [[AGENT_REACH_INTEGRATION_GUIDE]]
