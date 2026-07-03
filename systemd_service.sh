#!/bin/bash
# Knowledge Vault를 systemd 서비스로 등록
# 사용법: sudo bash systemd_service.sh

set -e

VAULT_PATH="/home/kim/OurKnowledgeVault"
PYTHON_BIN=$(which python3)
USER=$(whoami)

echo "🚀 Knowledge Vault systemd 서비스 설정"
echo "=================================================="
echo ""

# 1. systemd 서비스 파일 생성
echo "1️⃣ 서비스 파일 생성..."

sudo tee /etc/systemd/system/knowledge-vault.service > /dev/null << EOF
[Unit]
Description=Knowledge Vault - AI-Optimized Obsidian System
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
User=$USER
WorkingDirectory=$VAULT_PATH
ExecStart=$PYTHON_BIN $VAULT_PATH/vault_server.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "✅ 서비스 파일: /etc/systemd/system/knowledge-vault.service"
echo ""

# 2. systemd 데몬 재로드
echo "2️⃣ systemd 재로드..."
sudo systemctl daemon-reload
echo "✅ 완료"
echo ""

# 3. 서비스 활성화
echo "3️⃣ 서비스 자동 시작 활성화..."
sudo systemctl enable knowledge-vault.service
echo "✅ 완료"
echo ""

# 4. 서비스 시작
echo "4️⃣ 서비스 시작..."
sudo systemctl start knowledge-vault.service
echo "✅ 완료"
echo ""

# 5. 상태 확인
echo "5️⃣ 서비스 상태 확인..."
sudo systemctl status knowledge-vault.service --no-pager

echo ""
echo "=================================================="
echo "✅ Knowledge Vault 서비스 등록 완료!"
echo ""
echo "📊 서비스 명령어:"
echo "   sudo systemctl start knowledge-vault"
echo "   sudo systemctl stop knowledge-vault"
echo "   sudo systemctl restart knowledge-vault"
echo "   sudo systemctl status knowledge-vault"
echo "   sudo journalctl -u knowledge-vault -f"
echo ""
echo "🌐 웹 접속: http://localhost:8000"
