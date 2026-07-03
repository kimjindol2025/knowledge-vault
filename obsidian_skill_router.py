#!/usr/bin/env python3
"""
Obsidian Skill Router
Claude Code의 자연어 입력을 MCP 도구로 자동 라우팅
"""

import re
import json
from typing import Dict, List, Tuple, Optional


class ObsidianSkillRouter:
    """자연어 → MCP 도구 자동 라우팅"""

    def __init__(self):
        # 패턴 → 도구 매핑
        self.patterns = {
            # 생성 도구
            "생성|만들|작성|추가": {
                "tool": "create_note",
                "priority": 10,
                "description": "새 메모 생성"
            },
            "배치|여러|다중": {
                "tool": "batch_create",
                "priority": 9,
                "description": "여러 메모 한번에 생성"
            },

            # 읽기 도구
            "읽기|조회|보기|읽어": {
                "tool": "read_note",
                "priority": 8,
                "description": "메모 읽기"
            },

            # 검색 도구
            "검색|찾|조회|검색해": {
                "tool": "search_notes",
                "priority": 8,
                "description": "메모 검색"
            },

            # 수정 도구
            "수정|변경|업데이트|편집": {
                "tool": "update_note",
                "priority": 8,
                "description": "메모 수정"
            },

            # 링크 도구
            "링크|연결|관계": {
                "tool": "create_link",
                "priority": 7,
                "description": "메모 간 링크 생성"
            },

            # 분석 도구
            "분석|구조|네트워크|그래프": {
                "tool": "get_graph",
                "priority": 7,
                "description": "지식 네트워크 분석"
            },

            # 통계 도구
            "통계|정보|현황|상태": {
                "tool": "get_stats",
                "priority": 7,
                "description": "Vault 통계"
            },

            # 태그 도구
            "태그|분류|카테고리": {
                "tool": "add_tags",
                "priority": 6,
                "description": "태그 추가 & 분류"
            },

            # 목록 도구
            "목록|나열|리스트": {
                "tool": "list_notes",
                "priority": 6,
                "description": "메모 목록"
            },

            # 요약 도구
            "요약|정리|축약": {
                "tool": "generate_summary",
                "priority": 6,
                "description": "AI 요약 생성"
            }
        }

        # 파라미터 추출 규칙
        self.param_patterns = {
            "title": r"제목[:\s]*['\"]?([^'\"]+)['\"]?",
            "content": r"내용[:\s]*['\"]?(.+?)['\"]?(?:$|폴더|태그|타입)",
            "folder": r"폴더[:\s]*([^\s]+)|위치[:\s]*([^\s]+)",
            "tags": r"태그[:\s]*\[?([^\]]+)\]?|분류[:\s]*\[?([^\]]+)\]?",
            "query": r"검색[:\s]*['\"]?([^'\"]+)['\"]?|찾기[:\s]*['\"]?([^'\"]+)['\"]?",
            "filepath": r"파일[:\s]*([^\s]+)|경로[:\s]*([^\s]+)"
        }

    def parse_input(self, user_input: str) -> Dict:
        """사용자 입력 분석"""
        result = {
            "original": user_input,
            "matched_patterns": [],
            "selected_tool": None,
            "confidence": 0,
            "parameters": {},
            "action_type": None
        }

        # 패턴 매칭 (우선순위 순)
        matched = []
        for pattern, info in self.patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                matched.append({
                    "pattern": pattern,
                    "tool": info["tool"],
                    "priority": info["priority"],
                    "description": info["description"]
                })

        result["matched_patterns"] = matched

        # 가장 높은 우선순위 도구 선택
        if matched:
            best = max(matched, key=lambda x: x["priority"])
            result["selected_tool"] = best["tool"]
            result["confidence"] = min(100, best["priority"] * 10)
            result["action_type"] = best["description"]

        # 파라미터 추출
        params = self._extract_parameters(user_input)
        result["parameters"] = params

        return result

    def _extract_parameters(self, text: str) -> Dict:
        """파라미터 자동 추출"""
        params = {}

        for param_name, pattern in self.param_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                # 그룹 중 첫 번째 비어있지 않은 값 선택
                for group in match.groups():
                    if group:
                        params[param_name] = group.strip()
                        break

        return params

    def route_to_mcp(self, user_input: str) -> Dict:
        """사용자 입력을 MCP 도구로 라우팅"""
        parsed = self.parse_input(user_input)

        if not parsed["selected_tool"]:
            return {
                "status": "error",
                "message": "적절한 도구를 찾을 수 없습니다",
                "input": user_input
            }

        # 도구별 MCP 호출 생성
        tool = parsed["selected_tool"]
        params = parsed["parameters"]

        mcp_call = self._generate_mcp_call(tool, params)

        return {
            "status": "success",
            "input": user_input,
            "tool": tool,
            "description": parsed["action_type"],
            "confidence": parsed["confidence"],
            "mcp_call": mcp_call,
            "parameters": params,
            "hints": self._generate_hints(tool, params)
        }

    def _generate_mcp_call(self, tool: str, params: Dict) -> Dict:
        """MCP 호출 생성"""
        calls = {
            "create_note": {
                "tool": "create_note",
                "args": {
                    "title": params.get("title", "새 메모"),
                    "content": params.get("content", "내용"),
                    "folder": params.get("folder", "notes"),
                    "tags": self._parse_tags(params.get("tags", ""))
                }
            },
            "read_note": {
                "tool": "read_note",
                "args": {
                    "filepath": params.get("filepath", "")
                }
            },
            "update_note": {
                "tool": "update_note",
                "args": {
                    "filepath": params.get("filepath", ""),
                    "content": params.get("content", ""),
                    "append": True
                }
            },
            "create_link": {
                "tool": "create_link",
                "args": {
                    "from_file": params.get("filepath", ""),
                    "to_file": params.get("target", "")
                }
            },
            "search_notes": {
                "tool": "search_notes",
                "args": {
                    "query": params.get("query", ""),
                    "limit": 10
                }
            },
            "get_graph": {
                "tool": "get_graph",
                "args": {
                    "include_stats": True
                }
            },
            "get_stats": {
                "tool": "get_stats",
                "args": {}
            },
            "add_tags": {
                "tool": "add_tags",
                "args": {
                    "filepath": params.get("filepath", ""),
                    "tags": self._parse_tags(params.get("tags", ""))
                }
            },
            "list_notes": {
                "tool": "list_notes",
                "args": {
                    "folder": params.get("folder", "notes"),
                    "recursive": True
                }
            },
            "batch_create": {
                "tool": "batch_create",
                "args": {
                    "notes": self._parse_batch_notes(params.get("content", ""))
                }
            },
            "generate_summary": {
                "tool": "generate_summary",
                "args": {
                    "filepath": params.get("filepath", ""),
                    "length": "medium"
                }
            }
        }

        return calls.get(tool, {"tool": tool, "args": params})

    def _parse_tags(self, tags_str: str) -> List[str]:
        """태그 문자열 파싱"""
        if not tags_str:
            return []
        return [t.strip() for t in tags_str.split(",")]

    def _parse_batch_notes(self, content: str) -> List[Dict]:
        """배치 메모 파싱"""
        notes = []
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.strip():
                notes.append({
                    "title": f"메모 {i+1}",
                    "content": line.strip(),
                    "folder": "notes"
                })
        return notes

    def _generate_hints(self, tool: str, params: Dict) -> List[str]:
        """사용자를 위한 힌트"""
        hints = []

        if tool == "create_note" and "title" not in params:
            hints.append("💡 제목을 명시하면 더 정확합니다: '제목: ...'")

        if tool == "search_notes" and "query" not in params:
            hints.append("💡 검색어를 명시하면 더 정확합니다: '검색: ...'")

        if "filepath" in self.param_patterns and "filepath" not in params:
            hints.append("💡 파일 경로를 명시하면 더 정확합니다: '파일: ...'")

        return hints

    def create_claude_prompt(self, user_input: str) -> str:
        """Claude가 실행할 프롬프트 생성"""
        routed = self.route_to_mcp(user_input)

        if routed["status"] == "error":
            return f"오류: {routed['message']}"

        tool = routed["mcp_call"]["tool"]
        args = routed["mcp_call"]["args"]

        prompt = f"""
[Obsidian Skill 자동 라우팅]

사용자 요청: {user_input}
선택된 도구: {tool}
작업: {routed['description']}
신뢰도: {routed['confidence']}%

MCP 호출:
{json.dumps(args, indent=2, ensure_ascii=False)}

이제 MCP 서버의 '{tool}' 도구를 호출하세요.
"""

        if routed["hints"]:
            prompt += "\n💡 힌트:\n"
            for hint in routed["hints"]:
                prompt += f"  {hint}\n"

        return prompt


def main():
    """테스트 실행"""
    router = ObsidianSkillRouter()

    # 테스트 입력들
    test_inputs = [
        "옵시디언에 새 메모를 만들어줄래: 제목은 'Python 학습', 내용은 '기초부터 심화까지', 폴더는 'concepts'",
        "메모를 검색해줄래: 'AI'라는 단어로",
        "우리 지식 구조를 분석해줄래",
        "5개의 기초 과목 메모를 만들어줄래: 수학, 물리, 화학, 생물, 영어",
        "projects/codex.md 파일을 읽어줄래",
        "최근 생성된 메모들을 목록으로 보여줄래",
        "AI 관련 메모에 ['ai', 'machine-learning'] 태그를 추가해줄래"
    ]

    for user_input in test_inputs:
        print(f"\n{'='*60}")
        print(f"📝 사용자 입력: {user_input}")
        print(f"{'='*60}")

        result = router.route_to_mcp(user_input)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
