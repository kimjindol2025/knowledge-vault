#!/usr/bin/env python3
"""
Obsidian MCP Server (완전 구현)
Claude Code ↔ Obsidian Vault 양방향 연결

MCP (Model Context Protocol) 기반 서버
Claude가 Obsidian을 직접 제어
"""

import json
import os
import asyncio
from pathlib import Path
from datetime import datetime
import hashlib
import re
from typing import Any, Optional

# MCP 필수 라이브러리 (설치: pip install mcp)
try:
    from mcp.server import Server, stdio_server
    from mcp.types import Tool, TextContent, Resource, ResourceTemplate
except ImportError:
    print("⚠️ MCP 라이브러리 설치 필요: pip install mcp")
    exit(1)


class ObsidianVaultMCP:
    """Obsidian Vault를 MCP 서버로 제공"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.server = Server("obsidian-vault-mcp")
        self.cache = {}  # 간단한 캐싱

        # MCP 핸들러 등록
        self._register_tools()
        self._register_resources()

    def _register_tools(self):
        """Claude가 사용 가능한 도구 등록"""

        @self.server.list_tools()
        async def list_tools():
            return [
                # 읽기 도구
                Tool(
                    name="read_note",
                    description="Obsidian 메모 읽기",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filepath": {"type": "string", "description": "파일 경로 (예: projects/codex.md)"}
                        },
                        "required": ["filepath"]
                    }
                ),

                # 생성 도구
                Tool(
                    name="create_note",
                    description="새 메모 생성",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "content": {"type": "string"},
                            "folder": {"type": "string", "default": "notes"},
                            "tags": {"type": "array", "items": {"type": "string"}},
                            "type": {"type": "string", "enum": ["project", "tool", "concept", "guide"]}
                        },
                        "required": ["title", "content"]
                    }
                ),

                # 수정 도구
                Tool(
                    name="update_note",
                    description="메모 수정",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filepath": {"type": "string"},
                            "content": {"type": "string"},
                            "append": {"type": "boolean", "description": "기존 내용에 추가할지 여부"}
                        },
                        "required": ["filepath", "content"]
                    }
                ),

                # 링크 도구
                Tool(
                    name="create_link",
                    description="두 메모 간 양방향 링크 생성",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "from_file": {"type": "string"},
                            "to_file": {"type": "string"}
                        },
                        "required": ["from_file", "to_file"]
                    }
                ),

                # 검색 도구
                Tool(
                    name="search_notes",
                    description="메모 검색",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "limit": {"type": "integer", "default": 10}
                        },
                        "required": ["query"]
                    }
                ),

                # 분석 도구
                Tool(
                    name="get_graph",
                    description="지식 네트워크 그래프 조회",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "include_stats": {"type": "boolean", "default": True}
                        }
                    }
                ),

                # 통계 도구
                Tool(
                    name="get_stats",
                    description="Vault 통계",
                    inputSchema={"type": "object"}
                ),

                # 태그 도구
                Tool(
                    name="add_tags",
                    description="메모에 태그 추가",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filepath": {"type": "string"},
                            "tags": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["filepath", "tags"]
                    }
                ),

                # 목록 도구
                Tool(
                    name="list_notes",
                    description="폴더의 모든 메모 나열",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "folder": {"type": "string", "default": "notes"},
                            "recursive": {"type": "boolean", "default": False}
                        }
                    }
                ),

                # 고급: 배치 작업
                Tool(
                    name="batch_create",
                    description="여러 메모 한번에 생성",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "notes": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string"},
                                        "content": {"type": "string"},
                                        "folder": {"type": "string"}
                                    }
                                }
                            }
                        },
                        "required": ["notes"]
                    }
                ),

                # 고급: AI 요약
                Tool(
                    name="generate_summary",
                    description="메모의 AI 요약 생성",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filepath": {"type": "string"},
                            "length": {"type": "string", "enum": ["short", "medium", "long"]}
                        },
                        "required": ["filepath"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> Any:
            """도구 실행"""

            if name == "read_note":
                return self.read_note(arguments["filepath"])

            elif name == "create_note":
                return self.create_note(
                    arguments["title"],
                    arguments["content"],
                    arguments.get("folder", "notes"),
                    arguments.get("tags", []),
                    arguments.get("type", "note")
                )

            elif name == "update_note":
                return self.update_note(
                    arguments["filepath"],
                    arguments["content"],
                    arguments.get("append", False)
                )

            elif name == "create_link":
                return self.create_link(
                    arguments["from_file"],
                    arguments["to_file"]
                )

            elif name == "search_notes":
                return self.search_notes(
                    arguments["query"],
                    arguments.get("limit", 10)
                )

            elif name == "get_graph":
                return self.get_graph(arguments.get("include_stats", True))

            elif name == "get_stats":
                return self.get_stats()

            elif name == "add_tags":
                return self.add_tags(
                    arguments["filepath"],
                    arguments["tags"]
                )

            elif name == "list_notes":
                return self.list_notes(
                    arguments.get("folder", "notes"),
                    arguments.get("recursive", False)
                )

            elif name == "batch_create":
                return self.batch_create(arguments["notes"])

            elif name == "generate_summary":
                return self.generate_summary(
                    arguments["filepath"],
                    arguments.get("length", "medium")
                )

    def _register_resources(self):
        """Vault 자원 등록"""

        @self.server.list_resources()
        async def list_resources():
            return [
                ResourceTemplate(
                    uri_template="vault://notes/{path}",
                    name="Notes",
                    description="Obsidian 메모"
                ),
                ResourceTemplate(
                    uri_template="vault://stats",
                    name="Statistics",
                    description="Vault 통계"
                ),
                ResourceTemplate(
                    uri_template="vault://graph",
                    name="Graph",
                    description="지식 네트워크"
                )
            ]

        @self.server.read_resource()
        async def read_resource(uri: str):
            """자원 읽기"""

            if uri.startswith("vault://notes/"):
                filepath = uri.replace("vault://notes/", "")
                content = self.read_note(filepath)
                return [TextContent(type="text", text=json.dumps(content))]

            elif uri == "vault://stats":
                return [TextContent(type="text", text=json.dumps(self.get_stats()))]

            elif uri == "vault://graph":
                return [TextContent(type="text", text=json.dumps(self.get_graph()))]

    # ========== 구현 메서드 ==========

    def read_note(self, filepath: str) -> dict:
        """메모 읽기"""
        note_path = self.vault_path / filepath
        if note_path.exists():
            content = note_path.read_text(encoding='utf-8')
            return {
                "status": "success",
                "filepath": filepath,
                "content": content,
                "size": len(content),
                "updated": datetime.fromtimestamp(note_path.stat().st_mtime).isoformat()
            }
        return {"status": "error", "message": f"메모를 찾을 수 없습니다: {filepath}"}

    def create_note(self, title: str, content: str, folder: str = "notes",
                   tags: list = None, note_type: str = "note") -> dict:
        """새 메모 생성"""
        filename = title.lower().replace(" ", "-").replace(":", "") + ".md"
        folder_path = self.vault_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)

        # YAML frontmatter 생성
        frontmatter = f"""---
title: "{title}"
type: "{note_type}"
created: {datetime.now().isoformat()}
tags: {json.dumps(tags or [])}
---

"""

        note_path = folder_path / filename
        note_path.write_text(frontmatter + content, encoding='utf-8')

        return {
            "status": "created",
            "filepath": f"{folder}/{filename}",
            "title": title,
            "size": len(frontmatter + content)
        }

    def update_note(self, filepath: str, content: str, append: bool = False) -> dict:
        """메모 수정"""
        note_path = self.vault_path / filepath
        if note_path.exists():
            if append:
                existing = note_path.read_text(encoding='utf-8')
                new_content = existing + "\n\n" + content
            else:
                new_content = content

            note_path.write_text(new_content, encoding='utf-8')
            return {"status": "updated", "filepath": filepath}
        return {"status": "error", "message": f"메모를 찾을 수 없습니다: {filepath}"}

    def create_link(self, from_file: str, to_file: str) -> dict:
        """링크 생성"""
        from_path = self.vault_path / from_file
        if from_path.exists():
            content = from_path.read_text(encoding='utf-8')
            to_title = Path(to_file).stem.replace("-", " ").title()
            link = f"[[{to_title}]]"

            if link not in content:
                content += f"\n\n- {link}\n"
                from_path.write_text(content, encoding='utf-8')
                return {"status": "linked", "from": from_file, "to": to_title}
            return {"status": "already_linked"}
        return {"status": "error", "message": f"파일을 찾을 수 없습니다: {from_file}"}

    def search_notes(self, query: str, limit: int = 10) -> dict:
        """메모 검색"""
        results = []
        for note_file in self.vault_path.rglob("*.md"):
            if ".obsidian" in str(note_file):
                continue
            content = note_file.read_text(encoding='utf-8')
            if query.lower() in content.lower():
                results.append({
                    "filepath": str(note_file.relative_to(self.vault_path)),
                    "title": note_file.stem,
                    "matches": content.count(query.lower())
                })

        # 매칭 많은 순으로 정렬
        results.sort(key=lambda x: x["matches"], reverse=True)
        return {
            "query": query,
            "found": len(results),
            "results": results[:limit]
        }

    def get_graph(self, include_stats: bool = True) -> dict:
        """그래프 데이터"""
        nodes = []
        links = []
        processed = set()

        for note_file in self.vault_path.rglob("*.md"):
            if ".obsidian" in str(note_file):
                continue

            title = note_file.stem
            if title not in processed:
                nodes.append({
                    "id": title,
                    "label": title,
                    "file": str(note_file.relative_to(self.vault_path))
                })
                processed.add(title)

            content = note_file.read_text(encoding='utf-8')
            for match in re.finditer(r'\[\[([^\]]+)\]\]', content):
                target = match.group(1)
                if target not in processed:
                    nodes.append({"id": target, "label": target})
                    processed.add(target)
                links.append({"source": title, "target": target})

        result = {"nodes": nodes, "links": links}

        if include_stats:
            result["stats"] = {
                "total_nodes": len(nodes),
                "total_links": len(links),
                "avg_connections": len(links) / max(len(nodes), 1)
            }

        return result

    def get_stats(self) -> dict:
        """통계"""
        total_notes = 0
        total_words = 0
        total_links = 0

        for note_file in self.vault_path.rglob("*.md"):
            if ".obsidian" in str(note_file):
                continue
            total_notes += 1
            content = note_file.read_text(encoding='utf-8')
            total_words += len(content.split())
            total_links += len(re.findall(r'\[\[([^\]]+)\]\]', content))

        return {
            "total_notes": total_notes,
            "total_words": total_words,
            "total_links": total_links,
            "avg_words_per_note": total_words // max(total_notes, 1),
            "timestamp": datetime.now().isoformat()
        }

    def add_tags(self, filepath: str, tags: list) -> dict:
        """태그 추가"""
        note_path = self.vault_path / filepath
        if note_path.exists():
            content = note_path.read_text(encoding='utf-8')

            if content.startswith("---"):
                match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
                if match:
                    frontmatter = match.group(1)
                    frontmatter = re.sub(
                        r'tags: \[.*?\]',
                        f'tags: {json.dumps(tags)}',
                        frontmatter
                    ) if 'tags:' in frontmatter else frontmatter + f"\ntags: {json.dumps(tags)}"

                    new_content = f"---\n{frontmatter}\n---\n{content[match.end():]}"
                    note_path.write_text(new_content, encoding='utf-8')

            return {"status": "tagged", "filepath": filepath, "tags": tags}
        return {"status": "error", "message": f"메모를 찾을 수 없습니다: {filepath}"}

    def list_notes(self, folder: str = "notes", recursive: bool = False) -> dict:
        """메모 나열"""
        folder_path = self.vault_path / folder
        if folder_path.exists():
            if recursive:
                files = list(folder_path.rglob("*.md"))
            else:
                files = list(folder_path.glob("*.md"))

            return {
                "folder": folder,
                "count": len(files),
                "files": [f.name for f in files]
            }
        return {"status": "error", "message": f"폴더를 찾을 수 없습니다: {folder}"}

    def batch_create(self, notes: list) -> dict:
        """배치 생성"""
        created = []
        for note_data in notes:
            result = self.create_note(
                note_data["title"],
                note_data["content"],
                note_data.get("folder", "notes")
            )
            created.append(result)

        return {
            "status": "batch_created",
            "count": len(created),
            "results": created
        }

    def generate_summary(self, filepath: str, length: str = "medium") -> dict:
        """요약 생성"""
        note_content = self.read_note(filepath)

        if note_content["status"] == "error":
            return note_content

        content = note_content["content"]

        # 간단한 요약 (실제는 Claude 사용)
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]

        if length == "short":
            summary = ' '.join(lines[:3])
        elif length == "long":
            summary = ' '.join(lines[:10])
        else:  # medium
            summary = ' '.join(lines[:5])

        return {
            "filepath": filepath,
            "length": length,
            "summary": summary[:200] + "..." if len(summary) > 200 else summary
        }


async def run_server():
    """MCP 서버 실행"""
    vault_path = "/home/kim/OurKnowledgeVault"
    mcp = ObsidianVaultMCP(vault_path)

    # stdio 기반 서버 시작
    async with stdio_server(mcp.server) as (read_stream, write_stream):
        await mcp.server.run(read_stream, write_stream)


if __name__ == "__main__":
    print("🚀 Obsidian MCP Server 시작")
    print(f"📍 Vault: /home/kim/OurKnowledgeVault")
    print()

    asyncio.run(run_server())
