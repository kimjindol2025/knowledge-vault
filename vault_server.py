#!/usr/bin/env python3
"""
Knowledge Vault Web Server
Obsidian Vault를 웹 인터페이스로 브라우징하는 서버
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json
import os
from urllib.parse import unquote
import re

class VaultHandler(SimpleHTTPRequestHandler):
    vault_path = Path("/home/kim/OurKnowledgeVault")

    def do_GET(self):
        """GET 요청 처리"""
        if self.path == "/":
            self.serve_index()
        elif self.path.startswith("/api/notes"):
            self.api_list_notes()
        elif self.path.startswith("/api/read/"):
            self.api_read_note()
        elif self.path.startswith("/api/graph"):
            self.api_get_graph()
        elif self.path.startswith("/api/stats"):
            self.api_get_stats()
        elif self.path.startswith("/note/"):
            self.serve_note()
        else:
            self.send_error(404)

    def serve_index(self):
        """메인 페이지"""
        html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Knowledge Vault</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0d1117;
            color: #c9d1d9;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        header {
            border-bottom: 1px solid #30363d;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        h1 { font-size: 2em; margin-bottom: 10px; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }
        .stat-number { font-size: 2em; font-weight: bold; color: #58a6ff; }
        .stat-label { color: #8b949e; font-size: 0.9em; }
        .notes-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .note-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 15px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .note-card:hover {
            border-color: #58a6ff;
            transform: translateY(-2px);
        }
        .note-title { font-weight: bold; margin-bottom: 8px; }
        .note-type {
            display: inline-block;
            background: #238636;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            margin-right: 5px;
        }
        .note-tags {
            margin-top: 10px;
            font-size: 0.85em;
            color: #8b949e;
        }
        .tag {
            display: inline-block;
            background: #1f6feb;
            color: white;
            padding: 2px 6px;
            border-radius: 3px;
            margin-right: 4px;
            margin-top: 4px;
        }
        button {
            background: #238636;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
        }
        button:hover { background: #2ea043; }
        .folder { color: #79c0ff; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🧠 Knowledge Vault</h1>
            <p>AI-Optimized Obsidian Knowledge System</p>
        </header>

        <div class="stats" id="stats"></div>

        <div style="margin: 20px 0;">
            <button onclick="loadNotes()">📄 모든 메모</button>
            <button onclick="loadGraph()">🔗 그래프 뷰</button>
            <button onclick="loadStats()">📊 통계</button>
        </div>

        <div id="content"></div>
    </div>

    <script>
        async function loadStats() {
            const resp = await fetch('/api/stats');
            const data = await resp.json();

            const html = `
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">${data.total_notes}</div>
                        <div class="stat-label">메모</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.total_links}</div>
                        <div class="stat-label">링크</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.total_words}</div>
                        <div class="stat-label">단어</div>
                    </div>
                </div>
            `;
            document.getElementById('stats').innerHTML = html;
        }

        async function loadNotes() {
            const resp = await fetch('/api/notes');
            const notes = await resp.json();

            let html = '<div class="notes-grid">';
            for (const note of notes) {
                const folder = note.folder || 'notes';
                const type = note.type || 'note';
                const tags = note.tags || [];

                html += `
                    <div class="note-card" onclick="viewNote('${note.filepath}')">
                        <div class="folder">📁 ${folder}</div>
                        <div class="note-title">${note.title}</div>
                        <div class="note-type">${type}</div>
                        <div class="note-tags">
                            ${tags.map(t => `<span class="tag">${t}</span>`).join('')}
                        </div>
                    </div>
                `;
            }
            html += '</div>';
            document.getElementById('content').innerHTML = html;
        }

        async function loadGraph() {
            const resp = await fetch('/api/graph');
            const graph = await resp.json();

            let html = `
                <h2>지식 네트워크</h2>
                <p>${graph.nodes.length}개 노드, ${graph.links.length}개 링크</p>
                <div style="background: #161b22; padding: 15px; border-radius: 8px;">
                    <h3>주요 링크:</h3>
                    <ul>
            `;

            graph.links.slice(0, 20).forEach(link => {
                html += `<li><strong>${link.source}</strong> → <strong>${link.target}</strong></li>`;
            });

            html += '</ul></div>';
            document.getElementById('content').innerHTML = html;
        }

        async function viewNote(filepath) {
            const resp = await fetch(`/api/read/${encodeURIComponent(filepath)}`);
            const data = await resp.json();

            let html = `
                <div style="background: #161b22; padding: 20px; border-radius: 8px;">
                    <h2>${data.title || filepath}</h2>
                    <p style="color: #8b949e;">📁 ${filepath}</p>
                    <hr style="border-color: #30363d; margin: 15px 0;">
                    <pre style="background: #0d1117; padding: 15px; border-radius: 6px; overflow-x: auto;">
${data.content}
                    </pre>
                    <button onclick="loadNotes()">← 돌아가기</button>
                </div>
            `;
            document.getElementById('content').innerHTML = html;
        }

        // 초기 로드
        loadStats();
        loadNotes();
    </script>
</body>
</html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def api_list_notes(self):
        """모든 메모 나열"""
        notes = []
        for note_file in self.vault_path.rglob("*.md"):
            if ".obsidian" in str(note_file):
                continue
            content = note_file.read_text(encoding='utf-8')

            # frontmatter 파싱
            meta = {}
            if content.startswith("---"):
                match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
                if match:
                    for line in match.group(1).split('\n'):
                        if ':' in line:
                            k, v = line.split(':', 1)
                            meta[k.strip()] = v.strip().strip('"')

            notes.append({
                "filepath": str(note_file.relative_to(self.vault_path)),
                "folder": note_file.parent.name,
                "title": meta.get('title', note_file.stem),
                "type": meta.get('type', 'note'),
                "tags": meta.get('tags', '').strip('[]').split(',') if meta.get('tags') else []
            })

        self.send_json(sorted(notes, key=lambda x: x['filepath']))

    def api_read_note(self):
        """메모 읽기"""
        filepath = unquote(self.path.replace('/api/read/', ''))
        note_path = self.vault_path / filepath

        if note_path.exists():
            content = note_path.read_text(encoding='utf-8')
            meta = {}
            if content.startswith("---"):
                match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
                if match:
                    for line in match.group(1).split('\n'):
                        if ':' in line:
                            k, v = line.split(':', 1)
                            meta[k.strip()] = v.strip().strip('"')

            self.send_json({
                "filepath": filepath,
                "title": meta.get('title', filepath),
                "content": content,
                "meta": meta
            })
        else:
            self.send_error(404)

    def api_get_graph(self):
        """그래프 데이터"""
        nodes = []
        links = []
        processed = set()

        for note_file in self.vault_path.rglob("*.md"):
            if ".obsidian" in str(note_file):
                continue

            title = note_file.stem
            if title not in processed:
                nodes.append({"id": title, "label": title})
                processed.add(title)

            content = note_file.read_text(encoding='utf-8')
            for match in re.finditer(r'\[\[([^\]]+)\]\]', content):
                target = match.group(1)
                if target not in processed:
                    nodes.append({"id": target, "label": target})
                    processed.add(target)
                links.append({"source": title, "target": target})

        self.send_json({"nodes": nodes, "links": links})

    def api_get_stats(self):
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

        self.send_json({
            "total_notes": total_notes,
            "total_words": total_words,
            "total_links": total_links
        })

    def serve_note(self):
        """메모 페이지"""
        filepath = unquote(self.path.replace('/note/', ''))
        note_path = self.vault_path / filepath

        if note_path.exists():
            content = note_path.read_text(encoding='utf-8')
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{filepath}</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        pre {{ background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>{filepath}</h1>
    <pre>{content}</pre>
</body>
</html>
            """
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_error(404)

    def send_json(self, data):
        """JSON 응답"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def log_message(self, format, *args):
        """로그 출력"""
        print(f"[{self.log_date_time_string()}] {format%args}")


def run_server(port=8000):
    """서버 실행"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, VaultHandler)
    print(f"🌐 Knowledge Vault 서버 시작: http://localhost:{port}")
    print(f"📍 Vault: /home/kim/OurKnowledgeVault")
    print(f"💾 메모 보기, 그래프 뷰, 통계 조회 가능")
    print(f"\nCtrl+C로 종료")
    httpd.serve_forever()


if __name__ == '__main__':
    run_server(8000)
