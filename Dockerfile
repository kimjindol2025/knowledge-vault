# Knowledge Vault Docker Image
FROM python:3.12-slim

LABEL maintainer="Claude Code" \
      description="AI-Optimized Obsidian Knowledge Vault" \
      version="1.0"

# 작업 디렉토리
WORKDIR /app

# 의존성 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 파일 복사
COPY . .

# 포트 노출
EXPOSE 8000

# 헬스 체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/stats || exit 1

# 엔트리포인트
CMD ["python3", "vault_server.py"]
