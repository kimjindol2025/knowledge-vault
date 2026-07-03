#!/bin/bash
# Knowledge Vault 배포 스크립트
# 사용법: bash deploy.sh [73|253|company]

set -e

ENVIRONMENT=${1:-73}
VAULT_NAME="knowledge-vault"
VAULT_PORT=50500
VAULT_PATH="/home/kim/OurKnowledgeVault"

echo "🚀 Knowledge Vault 배포"
echo "=================================================="
echo "🎯 환경: $ENVIRONMENT 서버"
echo "📍 포트: $VAULT_PORT"
echo "📁 경로: $VAULT_PATH"
echo ""

# SSH 접속 정보
case $ENVIRONMENT in
  73)
    SSH_HOST="ssh73-direct"
    echo "📡 73서버 (Gogs/DNS) 배포"
    ;;
  253)
    SSH_HOST="ssh253"
    echo "📡 253서버 (메인) 배포"
    ;;
  company)
    SSH_HOST="company"
    echo "📡 회사 WSL 배포"
    ;;
  *)
    echo "❌ 잘못된 환경: $ENVIRONMENT"
    echo "사용법: bash deploy.sh [73|253|company]"
    exit 1
    ;;
esac

echo ""
echo "1️⃣ 로컬 파일 동기화..."
echo "=================================================="

# GitHub에 푸시
git add -A
git commit -m "Deploy: Knowledge Vault to $ENVIRONMENT server" 2>/dev/null || true
git push origin main

echo "✅ GitHub 푸시 완료"
echo ""

echo "2️⃣ $ENVIRONMENT 서버에 배포..."
echo "=================================================="

# 원격 서버에서 실행
ssh $SSH_HOST << REMOTE_SCRIPT
set -e

echo "📥 저장소 복제/업데이트..."
if [ ! -d "/home/kim/OurKnowledgeVault" ]; then
  git clone https://github.com/kimjindol2025/knowledge-vault.git /home/kim/OurKnowledgeVault
else
  cd /home/kim/OurKnowledgeVault
  git pull origin main
fi

cd /home/kim/OurKnowledgeVault

echo "✅ 코드 동기화 완료"
echo ""

echo "📋 dclub으로 서비스 배포..."
dclub deploy $VAULT_NAME $VAULT_PORT

echo "✅ 배포 완료"
echo ""

echo "🔄 PM2 설정..."
pm2 delete $VAULT_NAME 2>/dev/null || true
pm2 start ecosystem.config.js --name $VAULT_NAME
pm2 save

echo "✅ PM2 등록 완료"
echo ""

echo "🌐 서비스 확인..."
echo "   URL: https://$VAULT_NAME.dclub.kr"
echo "   로컬: http://localhost:$VAULT_PORT"
REMOTE_SCRIPT

echo ""
echo "=================================================="
echo "✅ 배포 완료!"
echo ""
echo "🌐 접속 정보:"
echo "   https://$VAULT_NAME.dclub.kr (외부)"
echo "   http://localhost:$VAULT_PORT (로컬)"
echo ""
echo "📊 PM2 관리:"
echo "   ssh $SSH_HOST"
echo "   pm2 list"
echo "   pm2 logs $VAULT_NAME"
echo "   pm2 restart $VAULT_NAME"
echo ""
echo "📡 DNS:"
echo "   dclub dns list"
echo ""
echo "🔧 중단:"
echo "   dclub undeploy $VAULT_NAME"
