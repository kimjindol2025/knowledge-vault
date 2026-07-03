#!/bin/bash
#
# Knowledge Vault 자동 메모 생성 스크립트
# Claude Code + agent-reach를 사용하여 자동으로 메모를 생성하고 Vault에 추가

set -e

VAULT_PATH="/home/kim/OurKnowledgeVault"
PYTHON_SERVER="$VAULT_PATH/obsidian_mcp_server.py"

echo "🚀 Knowledge Vault 자동 생성 시작"
echo "========================================"
echo ""

# 1. MCP 서버 테스트
echo "1️⃣ MCP 서버 검증..."
python3 "$PYTHON_SERVER"
echo ""

# 2. Vault 통계 업데이트
echo "2️⃣ Vault 상태 확인..."
python3 << 'PYTHON_SCRIPT'
from obsidian_mcp_server import ObsidianMCPServer

vault = ObsidianMCPServer("/home/kim/OurKnowledgeVault")
stats = vault.get_stats()

print(f"   📊 메모: {stats['total_notes']}개")
print(f"   📝 단어: {stats['total_words']}개")
print(f"   🔗 링크: {stats['total_links']}개")
PYTHON_SCRIPT

echo ""

# 3. 새 메모 생성 예제
echo "3️⃣ 새 메모 생성 예제..."
python3 << 'PYTHON_SCRIPT'
from obsidian_mcp_server import ObsidianMCPServer

vault = ObsidianMCPServer("/home/kim/OurKnowledgeVault")

# 새로운 메모 생성
new_note = """---
title: "Obsidian MCP 통합"
type: "프로젝트"
status: "✅ 진행 중"
date: "2026-07-03"
tags: ["obsidian", "mcp", "automation"]
ai_summary: "Claude Code와 Obsidian을 MCP로 직접 연동하는 완전 자동화 시스템"
---

# Obsidian MCP 통합

## 개요
MCP(Model Context Protocol)를 통한 Obsidian과 Claude Code의 완벽한 통합

## 기능
- 자동 메모 생성
- 자동 링크 생성
- 자동 태깅
- 그래프 자동 생성

## 관련 메모
- [[Claude Code]]
- [[Knowledge Management]]
- [[Multi-Agent Workflow]]

## 상태
✅ 구현 중
"""

result = vault.create_note(
    "Obsidian MCP 통합",
    new_note,
    "projects"
)
print(f"   ✅ {result['filepath']} 생성됨")

# 링크 생성
vault.create_link("projects/_index.md", "projects/obsidian-mcp-integration.md")
print("   🔗 링크 생성됨: _index.md → obsidian-mcp-integration.md")

# 태그 추가
vault.add_tags("projects/obsidian-mcp-integration.md", ["obsidian", "mcp", "automation"])
print("   🏷️ 태그 추가됨")
PYTHON_SCRIPT

echo ""

# 4. 그래프 생성
echo "4️⃣ 지식 그래프 분석..."
python3 << 'PYTHON_SCRIPT'
from obsidian_mcp_server import ObsidianMCPServer

vault = ObsidianMCPServer("/home/kim/OurKnowledgeVault")
graph = vault.get_graph()

print(f"   📊 노드: {len(graph['nodes'])}개")
print(f"   🔗 링크: {len(graph['links'])}개")

# 상위 허브 노드 찾기
hub_counts = {}
for link in graph['links']:
    source = link['source']
    hub_counts[source] = hub_counts.get(source, 0) + 1

if hub_counts:
    top_hubs = sorted(hub_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    print(f"   ⭐ 주요 허브:")
    for hub, count in top_hubs:
        print(f"      - {hub}: {count}개 링크")
PYTHON_SCRIPT

echo ""
echo "========================================"
echo "✅ Vault 자동 생성 완료!"
echo ""
echo "📍 위치: $VAULT_PATH"
echo "🌐 GitHub: https://github.com/kimjindol2025/knowledge-vault"
