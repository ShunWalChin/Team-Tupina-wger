# Team Tupina wger - Manual completo

Data: 2026-06-11

Este manual cobre instalacao local, deploy em producao, uso operacional e rotina
de manutencao do wger personalizado para o Team Tupina.

## 1. Visao geral

O sistema combina:

- Site institucional Team Tupina.
- Plataforma wger personalizada para treino, nutricao e acompanhamento.
- Perfis de admin, professor e aluno.
- API REST documentada por OpenAPI.
- Integracoes de ecossistema: site, Premium, RESET 7, Instagram, WhatsApp e email.

URLs locais usadas na homologacao:

| Area | URL |
| --- | --- |
| Site base | `http://127.0.0.1:8000/` |
| Premium | `http://127.0.0.1:8000/premium.html` |
| RESET 7 | `http://127.0.0.1:8000/reset-7.html` |
| App wger | `http://127.0.0.1:8002/pt-br/dashboard` |
| Login wger | `http://127.0.0.1:8002/pt-br/user/login` |
| API | `http://127.0.0.1:8002/pt-br/software/api` |

## 2. Usuarios locais de teste

| Perfil | Usuario | Uso |
| --- | --- | --- |
| Admin | `teamadmin` | Gestao geral e configuracao |
| Professor | `professor.teste` | Prescricao e acompanhamento |
| Aluno | `aluno.teste` | Uso final do aluno |

As senhas nao devem ser gravadas em documentacao versionada. Defina credenciais
em ambiente seguro e compartilhe apenas por gerenciador de senhas.

## 3. Fluxo de uso

### Admin

1. Acessar `/pt-br/user/login`.
2. Entrar com o usuario admin.
3. Revisar unidades Team Tupina, alunos e usuarios.
4. Criar professores e alunos reais.
5. Configurar permissoes.
6. Validar links do ecossistema no menu superior.
7. Acompanhar uso pela area administrativa e pela API quando necessario.

### Professor

1. Entrar no app.
2. Acessar Treinos.
3. Criar rotinas e templates.
4. Acessar Nutricao.
5. Criar planos nutricionais, quando fizer parte da entrega.
6. Acompanhar medidas, peso corporal e progresso dos alunos.
7. Reutilizar templates para acelerar a operacao.

### Aluno

1. Entrar no app.
2. Ver rotina de treino do dia.
3. Registrar progresso, medidas e peso quando orientado.
4. Consultar plano nutricional.
5. Usar o app como central de acompanhamento.

## 4. Instalacao local

No Windows usado na homologacao:

```powershell
cd "<CAMINHO_DO_PROJETO>\wger"
$env:DJANGO_SETTINGS_MODULE="settings.local_dev"
uv run python manage.py migrate
uv run python manage.py runserver 127.0.0.1:8002
```

Site institucional local:

```powershell
cd "<CAMINHO_DO_PROJETO>"
python -m http.server 8000 --bind 127.0.0.1
```

Checks locais:

```powershell
$env:DJANGO_SETTINGS_MODULE="settings.local_dev"
uv run python manage.py check
```

Quality gate completo do ecossistema:

```powershell
cd "<CAMINHO_DO_PROJETO>"
.\scripts\quality\team-tupina-quality-gate.ps1
```

## 5. Arquivos de deploy

Arquivos principais:

| Arquivo | Funcao |
| --- | --- |
| `deploy/production/docker-compose.team-tupina.yml` | Stack Docker de producao |
| `deploy/production/team-tupina.env.example` | Modelo de `.env` |
| `deploy/production/nginx.team-tupina.conf` | Nginx/reverse proxy |
| `docs/TEAM_TUPINA_VALIDACAO_PRE_DEPLOY.md` | Evidencia de validacao |
| `docs/TEAM_TUPINA_WGER_PRODUCAO.md` | Guia de producao inicial |
| `docs/TEAM_TUPINA_ENGINEERING_PLAYBOOK.md` | Playbook de engenharia e qualidade |
| `docs/TEAM_TUPINA_REQUIREMENTS_TRACEABILITY.md` | Matriz de requisitos e validacoes |
| `docs/adr/0001-team-tupina-customization-boundaries.md` | Fronteiras da customizacao wger |
| `../scripts/quality/team-tupina-quality-gate.ps1` | Quality gate local do ecossistema |

## 6. Variaveis de ambiente

Crie `.env` a partir do exemplo:

```bash
cp deploy/production/team-tupina.env.example .env
```

Campos obrigatorios:

| Variavel | O que configurar |
| --- | --- |
| `SECRET_KEY` | Chave longa e aleatoria do Django |
| `SIGNING_KEY` | Chave longa e aleatoria para tokens JWT |
| `SITE_URL` | `https://app.teamtupina.com.br` |
| `ALLOWED_HOSTS` | Dominios aceitos pelo Django |
| `CSRF_TRUSTED_ORIGINS` | Origens HTTPS aceitas para CSRF |
| `CORS_ALLOWED_ORIGINS` | Origens HTTPS autorizadas para acessar a API |
| `FROM_EMAIL` | Remetente do sistema |
| `EMAIL_*` | SMTP real |
| `DJANGO_DB_*` | PostgreSQL |
| `DJANGO_CACHE_*` | Redis cache |
| `CELERY_BROKER` | Redis fila |
| `CELERY_BACKEND` | Redis resultado |
| `TEAM_TUPINA_*` | Links do ecossistema |

Gerar secrets no servidor:

```bash
python3 - <<'PY'
import secrets
print("SECRET_KEY=" + secrets.token_urlsafe(64))
print("SIGNING_KEY=" + secrets.token_urlsafe(64))
PY
```

## 7. Deploy em servidor Linux

Base recomendada:

- Ubuntu LTS.
- Docker Engine.
- Docker Compose plugin.
- Nginx.
- Certbot.
- Firewall UFW.
- Backup externo.

Instalacao base:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y git ufw nginx certbot python3-certbot-nginx
```

Instale Docker Engine pela documentacao oficial da Docker.

Clone:

```bash
sudo mkdir -p /opt/team-tupina
sudo chown "$USER":"$USER" /opt/team-tupina
cd /opt/team-tupina
git clone <URL_DO_REPOSITORIO> wger
cd wger
```

Ambiente:

```bash
cp deploy/production/team-tupina.env.example .env
nano .env
```

Validar compose:

```bash
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env config
```

Subir:

```bash
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env build
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env up -d
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env ps
```

Migrations e static:

```bash
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env exec web python3 manage.py migrate
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env exec web python3 manage.py collectstatic --no-input
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env exec web python3 manage.py createsuperuser
```

## 8. Nginx e SSL

Copie a configuracao:

```bash
sudo cp deploy/production/nginx.team-tupina.conf /etc/nginx/sites-available/team-tupina.conf
sudo ln -s /etc/nginx/sites-available/team-tupina.conf /etc/nginx/sites-enabled/team-tupina.conf
sudo nginx -t
sudo systemctl reload nginx
```

Gerar SSL:

```bash
sudo certbot --nginx -d teamtupina.com.br -d www.teamtupina.com.br -d app.teamtupina.com.br
```

Depois do SSL:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## 9. Backup

Criar pasta:

```bash
sudo mkdir -p /opt/team-tupina/backups
sudo chown "$USER":"$USER" /opt/team-tupina/backups
```

Backup PostgreSQL:

```bash
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env exec -T postgres \
  pg_dump -U "$DJANGO_DB_USER" "$DJANGO_DB_DATABASE" \
  > /opt/team-tupina/backups/wger-$(date +%F).sql
```

Backup de midias:

```bash
docker run --rm \
  -v team_tupina_media:/data \
  -v /opt/team-tupina/backups:/backup \
  alpine tar -czf /backup/media-$(date +%F).tar.gz -C /data .
```

Rotina minima:

- Diario: banco e media.
- Semanal: copia externa.
- Mensal: teste de restauracao.
- Antes de atualizacoes: backup manual.

## 10. Atualizacao

```bash
cd /opt/team-tupina/wger
git pull
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env build
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env up -d
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env exec web python3 manage.py migrate
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env exec web python3 manage.py collectstatic --no-input
```

## 11. Rollback simples

1. Identificar ultimo commit estavel.
2. Fazer backup antes do rollback.
3. Voltar codigo:

```bash
git checkout <COMMIT_ESTAVEL>
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env build
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env up -d
```

Se houve migration destrutiva, restaurar backup do banco.

## 12. Monitoramento

Comandos uteis:

```bash
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env ps
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env logs -f web
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env logs -f celery-worker
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env logs -f postgres
```

Sinais de alerta:

- Login falhando para usuarios validos.
- Emails nao enviados.
- Uploads de imagem/video sem aparecer.
- Erros 500 no Nginx.
- Disco acima de 80%.
- Backups ausentes.

## 13. Seguranca

Obrigatorio em producao:

- `DJANGO_DEBUG=False`.
- `ALLOWED_HOSTS` restrito.
- `CSRF_TRUSTED_ORIGINS` com HTTPS real.
- `CORS_ALLOWED_ORIGINS` restrito aos dominios reais do app/site.
- HTTPS ativo.
- `SECRET_KEY` e `SIGNING_KEY` reais.
- Admin com senha forte.
- SSH com chave.
- Firewall liberando somente 22, 80 e 443.
- Backups externos.
- Registro de incidentes.

`SECURE_HSTS_PRELOAD` fica `False` no primeiro deploy. Ativar apenas depois de confirmar todos os subdominios HTTPS, pois preload e uma escolha persistente para navegadores.

## 14. Checklist de aceite

- Site institucional abre em HTTPS.
- App abre em HTTPS.
- Login admin funciona.
- Login professor funciona.
- Login aluno funciona.
- Dashboard sem overflow em mobile, tablet e desktop.
- Treinos, nutricao e medidas acessiveis.
- API/documentacao abre.
- Emails transacionais enviados.
- Upload de midia testado.
- Backup manual realizado.
- Primeiro restore testado em ambiente de homologacao.
