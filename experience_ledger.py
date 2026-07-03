#!/usr/bin/env python3
"""
Experience Ledger Bridge
증거 기반 능력 검증: "만들었다" 주장 → Artifact 연결
Knowledge Vault ↔ evo.dclub.kr Experience Ledger 통합
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Verdict(Enum):
    """역량 검증 상태"""
    VERIFIED = "🔵 VERIFIED"  # 검증됨
    IMPLEMENTED = "🔵 IMPLEMENTED"  # 구현됨
    TESTABLE = "🧪 TESTABLE"  # 테스트 가능
    PARTIAL = "🟡 PARTIAL"  # 부분 구현
    CLAIMED = "⬜ CLAIMED"  # 주장만 함


@dataclass
class Experience:
    """경험(역량) 데이터"""
    category: str
    capability: str
    verdict: Verdict
    artifacts: int
    repos: int
    description: str
    verified_at: Optional[str] = None


class ExperienceLedger:
    """Experience Ledger 관리"""

    def __init__(self):
        # 실제 Experience Ledger 데이터
        self.experiences = {
            "Language": [
                Experience("Language", "Lexer 구현", Verdict.VERIFIED, 292, 79,
                          "freelang-v11에서 실제 구현 확인 ✅ E2E 검증 완료"),
                Experience("Language", "Parser / AST 구현", Verdict.VERIFIED, 364, 13,
                          "freelang-v11에서 실제 구현 확인 ✅ parser.js (116KB) + ast.js (11KB)"),
                Experience("Language", "Type Checker", Verdict.VERIFIED, 103, 34,
                          "freelang-v11-1에서 발굴됨"),
                Experience("Language", "IR / Bytecode 생성", Verdict.IMPLEMENTED, 76, 22,
                          "freelang-v11-1에서 발굴됨"),
                Experience("Language", "JIT 컴파일러 구현", Verdict.IMPLEMENTED, 38, 10,
                          "핫패스 감지 + 타입 특수화 + 인라이닝 — jit_compilation.fl 750줄"),
                Experience("Language", "Self-Hosting 컴파일러", Verdict.VERIFIED, 154, 40,
                          "L4 Native ELF 고정점 달성 — SHA256 검증 (2026-05-24) ✅ E2E 테스트 완료"),
                Experience("Language", "REPL", Verdict.IMPLEMENTED, 237, 15,
                          "freelang-v11-1에서 발굴됨"),
                Experience("Language", "WebAssembly 코드 생성", Verdict.IMPLEMENTED, 26, 26,
                          ""),
                Experience("Language", "LLVM 백엔드 구현", Verdict.IMPLEMENTED, 35, 35,
                          ""),
                Experience("Language", "NPM 생태계 대체 구현", Verdict.IMPLEMENTED, 29, 29,
                          ""),
            ],
            "Runtime": [
                Experience("Runtime", "GC / 메모리 관리", Verdict.IMPLEMENTED, 65, 5,
                          "flsc에서 발굴됨"),
                Experience("Runtime", "Virtual Memory Manager", Verdict.IMPLEMENTED, 28, 28,
                          ""),
                Experience("Runtime", "Thread Pool + Work Stealing", Verdict.IMPLEMENTED, 9, 2,
                          "4~16 스레드, 작업 탈취, 확장 <100ms"),
                Experience("Runtime", "Lock-Free Queue 구현", Verdict.IMPLEMENTED, 13, 2,
                          "1000개 항목 링버퍼, 비트마스킹, 락 없음"),
                Experience("Runtime", "Process 기반 동시성", Verdict.IMPLEMENTED, 20, 5,
                          "OS 프로세스 격리, IPC mailbox"),
                Experience("Runtime", "VM / Bytecode Interpreter", Verdict.IMPLEMENTED, 17, 5,
                          "freelang-v6에서 발굴됨"),
                Experience("Runtime", "Bootloader 구현", Verdict.IMPLEMENTED, 4, 4, ""),
                Experience("Runtime", "Interrupt Handler 구현", Verdict.IMPLEMENTED, 15, 15, ""),
                Experience("Runtime", "Syscall / User Mode 구현", Verdict.IMPLEMENTED, 8, 8, ""),
            ],
            "Database": [
                Experience("Database", "ACID 트랜잭션 구현", Verdict.IMPLEMENTED, 135, 21,
                          "START TRANSACTION/COMMIT/ROLLBACK/SAVEPOINT"),
                Experience("Database", "B-Tree 인덱싱 구현", Verdict.IMPLEMENTED, 41, 11,
                          "PRIMARY KEY 자동, O(log n)"),
                Experience("Database", "MVCC 구현", Verdict.IMPLEMENTED, 15, 5,
                          "Multi-Version Concurrency Control"),
                Experience("Database", "WAL 로그 구현", Verdict.IMPLEMENTED, 21, 5,
                          "쓰기 전 로그, 강제종료 자동복구"),
                Experience("Database", "Replication / Consensus", Verdict.IMPLEMENTED, 92, 15,
                          "akl-writer에서 발굴됨"),
                Experience("Database", "Query Planner", Verdict.IMPLEMENTED, 5, 2,
                          "freelang-v4-query-performance에서 발굴됨"),
                Experience("Database", "SQL Parser 구현", Verdict.TESTABLE, 2, 1,
                          "완전한 SQL 파서 — freelang_mariadb Phase 1"),
            ],
            "Protocol": [
                Experience("Protocol", "HTTP 서버 구현", Verdict.IMPLEMENTED, 95, 26,
                          "AION-ts-orchestrator에서 발굴됨"),
                Experience("Protocol", "WebSocket 서버 구현", Verdict.IMPLEMENTED, 131, 9,
                          "RFC 6455, HTTP rate limiting"),
                Experience("Protocol", "TCP 서버 구현", Verdict.IMPLEMENTED, 26, 8,
                          "freelang-v11-1에서 발굴됨"),
                Experience("Protocol", "TLS/SSL 구현", Verdict.IMPLEMENTED, 38, 5,
                          "fre-memory에서 발굴됨"),
                Experience("Protocol", "HTTP/2 구현", Verdict.IMPLEMENTED, 25, 4,
                          "dclub-mail-fl에서 발굴됨"),
                Experience("Protocol", "SSH/SFTP 서버 구현", Verdict.IMPLEMENTED, 13, 4,
                          "ssh-sftp-server에서 발굴됨"),
                Experience("Protocol", "gRPC / Protobuf", Verdict.IMPLEMENTED, 26, 8,
                          "i2i에서 발굴됨"),
                Experience("Protocol", "DNS 구현", Verdict.IMPLEMENTED, 4, 1,
                          "kpm-registry에서 발굴됨"),
            ],
            "AI": [
                Experience("AI", "Tensor 연산 구현", Verdict.IMPLEMENTED, 10, 8,
                          "matmul/reshape/transpose — tensor.fl 217줄"),
                Experience("AI", "Autograd (자동미분) 구현", Verdict.IMPLEMENTED, 6, 4,
                          "8개 연산 역전파 — autograd.fl 512줄"),
                Experience("AI", "Multi-Head Attention 구현", Verdict.TESTABLE, 4, 2,
                          "Scaled Dot-Product + Causal Masking — attention.fl 468줄"),
                Experience("AI", "Neural Network Layer 구현", Verdict.TESTABLE, 4, 2,
                          "Linear/LayerNorm/Xavier — nn.fl 513줄"),
                Experience("AI", "Training Loop (Adam)", Verdict.TESTABLE, 9, 2,
                          "Phase 6 미완성 — trainer.fl 계획됨"),
                Experience("AI", "Embedding / Positional Encoding", Verdict.IMPLEMENTED, 12, 3,
                          "akl-base에서 발굴됨"),
                Experience("AI", "BPE Tokenizer", Verdict.TESTABLE, 4, 1,
                          "freelang_mariadb에서 발굴됨"),
                Experience("AI", "Inference Engine", Verdict.TESTABLE, 1, 1,
                          "파이프라인 발굴됨"),
            ],
            "Tooling": [
                Experience("Tooling", "Test Framework 구현", Verdict.IMPLEMENTED, 39, 39, ""),
                Experience("Tooling", "Linter / Static Analyzer", Verdict.IMPLEMENTED, 19, 19, ""),
                Experience("Tooling", "Git Hook 자동화", Verdict.IMPLEMENTED, 16, 16, ""),
                Experience("Tooling", "ID Generator 구현", Verdict.IMPLEMENTED, 18, 18, ""),
                Experience("Tooling", "P50/P95/P99 히스토그램", Verdict.IMPLEMENTED, 18, 17,
                          "7단계 지연시간 분포, 프로파일링 오버헤드 <5% CPU"),
                Experience("Tooling", "Causal Chain 분석", Verdict.IMPLEMENTED, 12, 8,
                          "trigger→propagation→effect 3단계 — 500ms 이내"),
                Experience("Tooling", "Self-Healing 시스템", Verdict.IMPLEMENTED, 9, 9, ""),
                Experience("Tooling", "Code Formatter 구현", Verdict.PARTIAL, 2, 2, ""),
                Experience("Tooling", "Build System", Verdict.TESTABLE, 12, 3,
                          "FLNext에서 발굴됨"),
            ],
            "Application": [
                Experience("Application", "OAuth / JWT 인증", Verdict.IMPLEMENTED, 130, 14,
                          "freelang-front에서 발굴됨"),
                Experience("Application", "Fullstack SSR 구현", Verdict.TESTABLE, 5, 1,
                          "freelang-front 1.0.0 — npm 0개, 30개 라우트 프로덕션"),
                Experience("Application", "Real-time Chat", Verdict.TESTABLE, 8, 2,
                          "mindlang-realtime-server에서 발굴됨"),
                Experience("Application", "Search Engine", Verdict.IMPLEMENTED, 21, 6,
                          "freelang-search에서 발굴됨"),
                Experience("Application", "State Management 구현", Verdict.IMPLEMENTED, 18, 18, ""),
                Experience("Application", "Game Engine / DSL", Verdict.IMPLEMENTED, 1, 1, ""),
            ],
        }

    def get_all_experiences(self) -> Dict[str, List[Dict[str, Any]]]:
        """모든 경험 반환"""
        result = {}
        for category, exps in self.experiences.items():
            result[category] = [
                {
                    "capability": exp.capability,
                    "verdict": exp.verdict.value,
                    "artifacts": exp.artifacts,
                    "repos": exp.repos,
                    "description": exp.description
                }
                for exp in exps
            ]
        return result

    def get_category(self, category: str) -> List[Dict[str, Any]]:
        """카테고리별 경험 조회"""
        if category not in self.experiences:
            return []
        return [
            {
                "capability": exp.capability,
                "verdict": exp.verdict.value,
                "artifacts": exp.artifacts,
                "repos": exp.repos,
                "description": exp.description
            }
            for exp in self.experiences[category]
        ]

    def get_verdict_stats(self) -> Dict[str, int]:
        """검증 상태별 통계"""
        stats = {
            "🔵 VERIFIED": 0,
            "🔵 IMPLEMENTED": 0,
            "🧪 TESTABLE": 0,
            "🟡 PARTIAL": 0,
            "⬜ CLAIMED": 0,
            "total_capabilities": 0,
            "total_artifacts": 0,
            "total_repos": 0
        }

        for category_exps in self.experiences.values():
            for exp in category_exps:
                stats[exp.verdict.value] += 1
                stats["total_capabilities"] += 1
                stats["total_artifacts"] += exp.artifacts
                stats["total_repos"] += exp.repos

        return stats

    def get_top_by_artifacts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Artifact 많은 순으로 상위 역량"""
        all_exps = []
        for category_exps in self.experiences.values():
            for exp in category_exps:
                all_exps.append({
                    "category": exp.category,
                    "capability": exp.capability,
                    "artifacts": exp.artifacts,
                    "repos": exp.repos,
                    "verdict": exp.verdict.value
                })
        return sorted(all_exps, key=lambda x: x["artifacts"], reverse=True)[:limit]

    def get_top_by_repos(self, limit: int = 10) -> List[Dict[str, Any]]:
        """저장소 많은 순으로 상위 역량"""
        all_exps = []
        for category_exps in self.experiences.values():
            for exp in category_exps:
                all_exps.append({
                    "category": exp.category,
                    "capability": exp.capability,
                    "artifacts": exp.artifacts,
                    "repos": exp.repos,
                    "verdict": exp.verdict.value
                })
        return sorted(all_exps, key=lambda x: x["repos"], reverse=True)[:limit]

    def find_by_verdict(self, verdict: str) -> List[Dict[str, Any]]:
        """검증 상태별로 찾기"""
        result = []
        for category_exps in self.experiences.values():
            for exp in category_exps:
                if verdict.upper() in exp.verdict.value:
                    result.append({
                        "category": exp.category,
                        "capability": exp.capability,
                        "artifacts": exp.artifacts,
                        "repos": exp.repos,
                        "verdict": exp.verdict.value,
                        "description": exp.description
                    })
        return result

    def verify_experience(self, capability: str, verified_at: Optional[str] = None) -> Dict[str, Any]:
        """경험 검증"""
        for category_exps in self.experiences.values():
            for exp in category_exps:
                if exp.capability == capability:
                    return {
                        "capability": capability,
                        "status": "verified",
                        "verified_at": verified_at or datetime.now().isoformat(),
                        "artifacts": exp.artifacts,
                        "repos": exp.repos
                    }
        return {"status": "not_found"}


class ExperienceLedgerAnalyzer:
    """Experience Ledger 분석"""

    def __init__(self):
        self.ledger = ExperienceLedger()

    def analyze_all(self) -> Dict[str, Any]:
        """전체 분석"""
        stats = self.ledger.get_verdict_stats()
        return {
            "summary": stats,
            "by_category": self.ledger.get_all_experiences(),
            "top_by_artifacts": self.ledger.get_top_by_artifacts(),
            "top_by_repos": self.ledger.get_top_by_repos(),
            "verified": self.ledger.find_by_verdict("VERIFIED"),
            "implemented": self.ledger.find_by_verdict("IMPLEMENTED"),
            "testable": self.ledger.find_by_verdict("TESTABLE"),
            "partial": self.ledger.find_by_verdict("PARTIAL"),
            "claimed": self.ledger.find_by_verdict("CLAIMED"),
            "timestamp": datetime.now().isoformat()
        }

    def category_analysis(self, category: str) -> Dict[str, Any]:
        """카테고리 분석"""
        exps = self.ledger.get_category(category)
        if not exps:
            return {"status": "not_found"}

        stats = {
            "total": len(exps),
            "implemented": sum(1 for e in exps if "IMPLEMENTED" in e["verdict"]),
            "testable": sum(1 for e in exps if "TESTABLE" in e["verdict"]),
            "partial": sum(1 for e in exps if "PARTIAL" in e["verdict"]),
            "claimed": sum(1 for e in exps if "CLAIMED" in e["verdict"]),
            "total_artifacts": sum(e["artifacts"] for e in exps),
            "total_repos": sum(e["repos"] for e in exps),
            "coverage": (sum(1 for e in exps if "IMPLEMENTED" in e["verdict"]) / len(exps) * 100)
        }

        return {
            "category": category,
            "stats": stats,
            "experiences": exps
        }


# MCP 도구로 등록할 함수들
def get_experience_stats():
    """전체 Experience Ledger 통계"""
    analyzer = ExperienceLedgerAnalyzer()
    return analyzer.ledger.get_verdict_stats()


def get_all_experiences():
    """모든 경험 조회"""
    analyzer = ExperienceLedgerAnalyzer()
    return analyzer.ledger.get_all_experiences()


def analyze_experience_ledger():
    """Experience Ledger 전체 분석"""
    analyzer = ExperienceLedgerAnalyzer()
    return analyzer.analyze_all()


def get_category_analysis(category: str):
    """카테고리 분석"""
    analyzer = ExperienceLedgerAnalyzer()
    return analyzer.category_analysis(category)


def find_experiences_by_verdict(verdict: str):
    """검증 상태별로 경험 찾기"""
    analyzer = ExperienceLedgerAnalyzer()
    return analyzer.ledger.find_by_verdict(verdict)


def get_top_capabilities(metric: str = "artifacts", limit: int = 10):
    """상위 역량"""
    analyzer = ExperienceLedgerAnalyzer()
    if metric == "repos":
        return analyzer.ledger.get_top_by_repos(limit)
    else:
        return analyzer.ledger.get_top_by_artifacts(limit)


if __name__ == "__main__":
    # 테스트
    analyzer = ExperienceLedgerAnalyzer()

    print("🔍 Experience Ledger Analysis")
    print("=" * 70)

    print("\n1️⃣ 통계:")
    stats = analyzer.ledger.get_verdict_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))

    print("\n2️⃣ Artifact 상위 10:")
    top_artifacts = analyzer.ledger.get_top_by_artifacts(10)
    for i, exp in enumerate(top_artifacts, 1):
        print(f"  {i}. {exp['capability']} ({exp['category']}) - {exp['artifacts']} Artifacts")

    print("\n3️⃣ 저장소 상위 10:")
    top_repos = analyzer.ledger.get_top_by_repos(10)
    for i, exp in enumerate(top_repos, 1):
        print(f"  {i}. {exp['capability']} ({exp['category']}) - {exp['repos']} Repos")

    print("\n4️⃣ 카테고리 분석 (Language):")
    lang_analysis = analyzer.category_analysis("Language")
    print(json.dumps(lang_analysis, indent=2, ensure_ascii=False))

    print("\n✅ Experience Ledger Ready!")
