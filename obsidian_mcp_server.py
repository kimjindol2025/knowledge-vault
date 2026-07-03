#!/usr/bin/env python3
"""
Obsidian MCP Server
Claude Code가 Obsidian Vault와 직접 통신하기 위한 MCP 서버
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

class ObsidianMCPServer:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)

    def read_note(self, filepath: str) -> str:
        """메모 파일 읽기"""
        note_path = self.vault_path / filepath
        if note_path.exists():
            return note_path.read_text(encoding='utf-8')
        return f"Note not found: {filepath}"

    def create_note(self, title: str, content: str, folder: str = "notes") -> dict:
        """새 메모 생성"""
        filename = title.lower().replace(" ", "-").replace(":", "") + ".md"
        folder_path = self.vault_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)

        note_path = folder_path / filename
        note_path.write_text(content, encoding='utf-8')

        return {
            "status": "created",
            "filepath": f"{folder}/{filename}",
            "title": title
        }

    def update_note(self, filepath: str, content: str) -> dict:
        """메모 수정"""
        note_path = self.vault_path / filepath
        if note_path.exists():
            note_path.write_text(content, encoding='utf-8')
            return {"status": "updated", "filepath": filepath}
        return {"status": "error", "message": f"Note not found: {filepath}"}

    def create_link(self, from_file: str, to_file: str) -> dict:
        """두 메모 간 링크 생성"""
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
        return {"status": "error", "message": f"Source file not found: {from_file}"}

    def add_tags(self, filepath: str, tags: list) -> dict:
        """메모에 태그 추가"""
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
            else:
                frontmatter = f"---\ntags: {json.dumps(tags)}\n---\n"
                new_content = frontmatter + content
                note_path.write_text(new_content, encoding='utf-8')

            return {"status": "tagged", "tags": tags}
        return {"status": "error", "message": f"Note not found: {filepath}"}

    def list_notes(self, folder: str = "notes") -> list:
        """폴더의 모든 메모 나열"""
        folder_path = self.vault_path / folder
        if folder_path.exists():
            return [f.name for f in folder_path.glob("*.md")]
        return []

    def search_notes(self, query: str) -> list:
        """메모 검색"""
        results = []
        for note_file in self.vault_path.rglob("*.md"):
            if ".obsidian" in str(note_file):
                continue
            content = note_file.read_text(encoding='utf-8')
            if query.lower() in content.lower():
                results.append(str(note_file.relative_to(self.vault_path)))
        return results

    def get_graph(self) -> dict:
        """그래프 데이터 생성"""
        nodes = []
        links = []
        processed_nodes = set()

        for note_file in self.vault_path.rglob("*.md"):
            if ".obsidian" in str(note_file):
                continue

            title = note_file.stem
            if title not in processed_nodes:
                nodes.append({"id": title, "label": title, "file": str(note_file.relative_to(self.vault_path))})
                processed_nodes.add(title)

            content = note_file.read_text(encoding='utf-8')
            for match in re.finditer(r'\[\[([^\]]+)\]\]', content):
                target = match.group(1)
                if target not in processed_nodes:
                    nodes.append({"id": target, "label": target})
                    processed_nodes.add(target)
                links.append({"source": title, "target": target})

        return {"nodes": nodes, "links": links}

    def get_stats(self) -> dict:
        """Vault 통계"""
        total_notes = len(list(self.vault_path.rglob("*.md"))) - 1
        total_words = 0
        total_links = 0

        for note_file in self.vault_path.rglob("*.md"):
            if ".obsidian" in str(note_file):
                continue
            content = note_file.read_text(encoding='utf-8')
            total_words += len(content.split())
            total_links += len(re.findall(r'\[\[([^\]]+)\]\]', content))

        return {
            "total_notes": total_notes,
            "total_words": total_words,
            "total_links": total_links,
            "created_at": datetime.now().isoformat()
        }


def main():
    """테스트 실행"""
    vault = ObsidianMCPServer("/home/kim/OurKnowledgeVault")

    # 기본 정보
    print("📊 Knowledge Vault 통계:")
    stats = vault.get_stats()
    print(f"  메모: {stats['total_notes']}개")
    print(f"  단어: {stats['total_words']}개")
    print(f"  링크: {stats['total_links']}개")
    print()

    # 그래프
    print("🔗 지식 네트워크:")
    graph = vault.get_graph()
    print(f"  노드: {len(graph['nodes'])}개")
    print(f"  링크: {len(graph['links'])}개")
    print()

    # 메모 목록
    print("📝 프로젝트 메모:")
    projects = vault.list_notes("projects")
    for proj in projects:
        print(f"  - {proj}")


if __name__ == "__main__":
    main()
