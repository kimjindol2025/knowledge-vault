# Knowledge Vault 배포 가이드

**프로덕션 환경에 Knowledge Vault를 배포하는 완벽한 가이드**

---

## 🚀 배포 옵션

### 옵션 1: dclub CLI로 자동 배포 (권장) ⭐

**가장 간단하고 빠른 방법 - 모든 것이 자동화됨**

```bash
# 73서버에 배포
bash deploy.sh 73

# 또는 253서버에 배포
bash deploy.sh 253

# 또는 회사 WSL에 배포
bash deploy.sh company
```

**자동으로 수행되는 작업:**
- ✅ GitHub에서 최신 코드 가져오기
- ✅ `dclub deploy`로 서비스 배포
- ✅ PM2로 프로세스 관리
- ✅ HTTPS 자동 설정
- ✅ DNS 자동 등록
- ✅ 외부 접근 가능 (https://knowledge-vault.dclub.kr)

**결과:**
```
✅ 배포 완료!

🌐 접속 정보:
   외부: https://knowledge-vault.dclub.kr
   로컬: http://localhost:50500
   
📊 PM2 관리:
   ssh ssh73-direct
   pm2 list
   pm2 logs knowledge-vault
```

---

### 옵션 2: Docker로 로컬 배포

**Docker/docker-compose 사용**

```bash
# 빌드 & 실행
docker-compose up -d

# 또는
docker build -t knowledge-vault .
docker run -p 8000:8000 knowledge-vault
```

**접속:**
```
http://localhost:8000
```

**관리:**
```bash
docker-compose ps
docker-compose logs -f knowledge-vault
docker-compose stop
docker-compose restart
```

---

### 옵션 3: systemd 서비스로 등록

**Linux systemd로 관리 (자동 시작/재시작)**

```bash
# 1. 권한 설정
chmod +x systemd_service.sh

# 2. 서비스 등록 (관리자 필요)
sudo bash systemd_service.sh

# 3. 상태 확인
sudo systemctl status knowledge-vault
```

**관리:**
```bash
# 시작/중지/재시작
sudo systemctl start knowledge-vault
sudo systemctl stop knowledge-vault
sudo systemctl restart knowledge-vault

# 로그 확인
sudo journalctl -u knowledge-vault -f

# 자동 시작 설정/해제
sudo systemctl enable knowledge-vault
sudo systemctl disable knowledge-vault
```

---

### 옵션 4: PM2로 수동 관리

**PM2 설정 파일 사용**

```bash
# 1. PM2 설치 (필요시)
npm install -g pm2

# 2. 서비스 시작
pm2 start ecosystem.config.js

# 3. 자동 시작 설정
pm2 startup
pm2 save

# 4. 상태 확인
pm2 list
pm2 logs knowledge-vault
```

**관리:**
```bash
pm2 start knowledge-vault
pm2 stop knowledge-vault
pm2 restart knowledge-vault
pm2 delete knowledge-vault
```

---

## 📊 배포 후 확인

### 1️⃣ 웹 접속 확인

```bash
# 로컬
curl http://localhost:8000

# 또는 브라우저
http://localhost:8000
http://localhost:50500  (dclub 배포 시)
https://knowledge-vault.dclub.kr  (외부)
```

### 2️⃣ API 동작 확인

```bash
# 메모 목록
curl http://localhost:8000/api/notes

# 통계
curl http://localhost:8000/api/stats

# 그래프
curl http://localhost:8000/api/graph
```

### 3️⃣ 로그 확인

```bash
# systemd
sudo journalctl -u knowledge-vault -f

# PM2
pm2 logs knowledge-vault

# Docker
docker-compose logs -f knowledge-vault
```

### 4️⃣ 성능 모니터링

```bash
# CPU/메모리 사용량 (PM2)
pm2 monit

# 포트 확인
netstat -tlnp | grep 8000
netstat -tlnp | grep 50500
```

---

## 🔄 자동 메모 생성 (선택)

서버에서 주기적으로 메모를 자동 생성하려면:

```bash
# 1회 실행
bash auto_generate_notes.sh

# 매일 자동 실행 (cron)
crontab -e

# 다음 라인 추가:
0 2 * * * cd /home/kim/OurKnowledgeVault && bash auto_generate_notes.sh
```

---

## 📁 배포 후 파일 구조

```
/home/kim/OurKnowledgeVault/
├── vault_server.py             (실행 중인 웹 서버)
├── obsidian_mcp_server.py      (MCP API)
├── projects/                   (메모 저장소)
├── tools/
├── concepts/
└── .obsidian/                  (Obsidian 설정)

[배포 시에만]
├── ecosystem.config.js         (PM2 설정)
├── Dockerfile                  (Docker 이미지)
├── docker-compose.yml          (Docker Compose)
└── deploy.sh                   (배포 스크립트)
```

---

## ⚡ 빠른 시작 (73서버 기준)

### 1️⃣ SSH 접속

```bash
ssh ssh73-direct
```

### 2️⃣ 배포

```bash
cd /home/kim/OurKnowledgeVault
bash deploy.sh 73
```

### 3️⃣ 확인

```bash
# 서비스 상태
pm2 list

# 로그
pm2 logs knowledge-vault

# 웹 접속
curl http://localhost:50500/api/stats
```

### 4️⃣ 외부 접근

```
https://knowledge-vault.dclub.kr
```

---

## 🔧 트러블슈팅

### 포트 충돌

```bash
# 포트 확인
lsof -i :8000
lsof -i :50500

# 프로세스 종료
kill -9 <PID>

# 또는 다른 포트로 변경
# vault_server.py에서 포트 수정
```

### 메모리 부족

```bash
# 메모리 제한 설정
# ecosystem.config.js에서 max_memory_restart 조정

max_memory_restart: '1G'  # 1GB로 증가
```

### 로그 확인

```bash
# 최근 100줄
pm2 logs knowledge-vault -n 100

# 에러만 보기
pm2 logs knowledge-vault --err

# 파일로 저장
pm2 logs knowledge-vault > /tmp/vault.log
```

---

## 📈 성능 최적화

### 1️⃣ 메모리 최적화

```javascript
// ecosystem.config.js
max_memory_restart: '500M'  // 필요에 따라 조정
```

### 2️⃣ 동시성 설정

```javascript
instances: 2  // CPU 코어 수에 맞게
exec_mode: 'cluster'
```

### 3️⃣ 캐싱 활성화

```python
# vault_server.py 수정
# 나중에 Redis 캐싱 추가 가능
```

---

## 🔐 보안

### 1️⃣ 방화벽 설정

```bash
# 로컬만 접근 허용
iptables -A INPUT -p tcp --dport 8000 -s 127.0.0.1 -j ACCEPT
iptables -A INPUT -p tcp --dport 8000 -j DROP
```

### 2️⃣ HTTPS 설정

```bash
# dclub deploy로 자동 설정됨
# 또는 Let's Encrypt로 수동 설정

certbot certonly --standalone -d knowledge-vault.dclub.kr
```

### 3️⃣ 인증 (추가 기능)

```python
# 향후 JWT 인증 추가
# BasicAuth 또는 API 키 기반 인증
```

---

## 📚 관련 명령어

### dclub CLI

```bash
# 서비스 배포
dclub deploy knowledge-vault 50500

# PM2 관리
dclub pm2 list
dclub pm2 logs knowledge-vault
dclub pm2 restart knowledge-vault

# DNS 관리
dclub dns list
dclub dns create knowledge-vault 192.168.45.73

# 상태 확인
dclub status
dclub health

# 서비스 제거
dclub undeploy knowledge-vault
```

### PM2 명령어

```bash
pm2 start ecosystem.config.js
pm2 list
pm2 logs
pm2 restart all
pm2 stop all
pm2 delete all
pm2 save
pm2 startup
```

### Docker 명령어

```bash
docker-compose up -d
docker-compose down
docker-compose logs -f
docker-compose ps
docker-compose restart knowledge-vault
```

---

## ✅ 배포 체크리스트

- [ ] 코드 수정 완료
- [ ] 로컬 테스트 완료
- [ ] GitHub에 푸시
- [ ] 배포 스크립트 실행 (`bash deploy.sh 73`)
- [ ] 웹 접속 확인 (`http://localhost:8000`)
- [ ] API 동작 확인 (`curl http://localhost:8000/api/stats`)
- [ ] 로그 확인 (`pm2 logs knowledge-vault`)
- [ ] 외부 접근 확인 (필요시)
- [ ] 자동 재시작 설정 확인

---

## 🎉 배포 완료!

```
✅ Knowledge Vault 배포 완료

🌐 웹: http://localhost:8000
📊 API: http://localhost:8000/api/stats
📍 GitHub: https://github.com/kimjindol2025/knowledge-vault

🎯 다음 단계:
1. 메모 추가
2. 그래프 확인
3. 자동화 설정
```

---

**Questions?** 로그를 확인하세요:
```bash
pm2 logs knowledge-vault
sudo journalctl -u knowledge-vault -f
docker-compose logs -f
```
