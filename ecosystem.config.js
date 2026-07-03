/**
 * PM2 Ecosystem Config
 * Knowledge Vault을 PM2로 관리
 */

module.exports = {
  apps: [
    {
      name: 'knowledge-vault',
      script: 'vault_server.py',
      interpreter: 'python3',
      cwd: '/home/kim/OurKnowledgeVault',
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'production',
        VAULT_PATH: '/home/kim/OurKnowledgeVault'
      },
      instances: 1,
      exec_mode: 'fork',
      error_file: '/home/kim/.pm2/logs/knowledge-vault-error.log',
      out_file: '/home/kim/.pm2/logs/knowledge-vault-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    }
  ]
};
