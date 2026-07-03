# Team Tupina wger - Guia de implementacao e producao

Atualizado em 2026-06-11.

Este documento descreve como sair do ambiente local do Team Tupina e publicar o
sistema completo em producao, com site institucional, wger personalizado,
PostgreSQL, Redis/Celery, Nginx, SSL, backup e monitoramento.

## Estado local confirmado

Ambiente local usado para homologacao:

- Site base: `http://127.0.0.1:8000/`
- Premium: `http://127.0.0.1:8000/premium.html`
- RESET 7: `http://127.0.0.1:8000/reset-7.html`
- wger Team Tupina: `http://127.0.0.1:8002/pt-br/software/features`
- Login wger: `http://127.0.0.1:8002/pt-br/user/login`

Usuarios locais de teste:

| Perfil | Usuario | Papel |
| --- | --- | --- |
| Admin | `teamadmin` | Superuser + gestao geral |
| Professor | `professor.teste` | `gym_trainer` |
| Aluno | `aluno.teste` | `gym_member` |

As senhas nao devem ser versionadas. Defina, troque e compartilhe credenciais
somente por gerenciador de senhas.

## Arquitetura recomendada

Para uma primeira versao publica, use um servidor dedicado ou VPS robusto com:

- Ubuntu LTS.
- Docker Engine + Docker Compose.
- Nginx como reverse proxy.
- Certbot/Let's Encrypt para SSL.
- PostgreSQL para banco principal.
- Redis para cache, fila e Celery.
- Volumes persistentes para banco, media e static files.
- Backup externo, preferencialmente em outro provedor ou storage S3 compativel.

Topologia sugerida:

```text
internet
  |
  | HTTPS
  v
Nginx
  |-- teamtupina.com.br          -> site institucional estatico
  |-- app.teamtupina.com.br      -> wger web
  |-- api.teamtupina.com.br      -> wger API, opcional
  |
Docker network
  |-- web: Django/Gunicorn
  |-- postgres
  |-- redis
  |-- celery-worker
  |-- celery-beat
```

## Provedores de hospedagem dedicada

Opcoes viaveis para comparar antes da contratacao:

- Hetzner Dedicated Root Server: dedicado com linhas AX/EX/RX/SX e server
  auction. Bom custo por CPU/RAM, datacenters fora do Brasil.
- OVHcloud Bare Metal: servidores dedicados com anti-DDoS incluso e rede
  global.
- DigitalOcean Droplets: VPS simples de operar; nao e bare metal dedicado, mas
  pode ser bom para MVP.
- AWS Lightsail/EC2: melhor quando o ecossistema AWS for necessario, com custo
  geralmente mais alto e mais componentes para configurar.

Dimensionamento inicial recomendado:

| Fase | Perfil minimo | Uso esperado |
| --- | --- | --- |
| MVP fechado | 2 vCPU, 4 GB RAM, 80 GB SSD | Validacao interna e poucos alunos |
| Beta pago | 4 vCPU, 8 GB RAM, 160 GB SSD | Professores + dezenas/centenas de alunos |
| Producao dedicada | 8 vCPU, 32 GB RAM, 2x NVMe em RAID1 | Operacao comercial com margem |
| Escala | App e DB separados | Mais trafego, videos, backups e BI |

Sempre confira preco, regiao, suporte, backup e politica de trafego antes de
contratar. Hospedagem e custo mudam com frequencia.

## DNS e dominios

Registros recomendados:

```text
A     teamtupina.com.br      -> IP do servidor
A     www.teamtupina.com.br  -> IP do servidor
A     app.teamtupina.com.br  -> IP do servidor
A     api.teamtupina.com.br  -> IP do servidor, opcional
CAA   teamtupina.com.br      -> letsencrypt.org, opcional
```

Se usar Cloudflare, deixe proxy ligado apenas depois de validar SSL direto no
servidor.

## Variaveis de ambiente

Use `deploy/production/team-tupina.env.example` como base. Os campos criticos:

- `SECRET_KEY` e `SIGNING_KEY`: gerar valores longos e unicos.
- `DJANGO_DEBUG=False`.
- `SITE_URL=https://app.teamtupina.com.br`.
- `ALLOWED_HOSTS`: restringir aos dominios reais.
- `CSRF_TRUSTED_ORIGINS`: listar as origens HTTPS reais.
- `CORS_ALLOWED_ORIGINS`: listar somente site/app autorizados a consumir a API.
- `FROM_EMAIL`, SMTP e DNS de email.
- `TEAM_TUPINA_*`: links do ecossistema exibidos dentro do wger.
- `DJANGO_DB_*`: PostgreSQL.
- `DJANGO_CACHE_*`, `CELERY_BROKER` e `CELERY_BACKEND`: Redis.
- `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE` e `CSRF_COOKIE_SECURE`: manter
  ativos em producao com HTTPS.

## Processo de deploy

1. Preparar servidor:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y git ufw nginx
```

2. Instalar Docker Engine seguindo a documentacao oficial da Docker para
   Ubuntu.

3. Clonar o repositorio personalizado:

```bash
sudo mkdir -p /opt/team-tupina
sudo chown "$USER":"$USER" /opt/team-tupina
cd /opt/team-tupina
git clone <URL_DO_REPOSITORIO> wger
cd wger
```

4. Criar `.env` de producao:

```bash
cp deploy/production/team-tupina.env.example .env
nano .env
```

5. Build e subida:

```bash
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env build
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env up -d
```

6. Migrations, static e usuario admin:

```bash
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env exec web python3 manage.py migrate
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env exec web python3 manage.py collectstatic --no-input
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env exec web python3 manage.py createsuperuser
```

7. Configurar Nginx com `deploy/production/nginx.team-tupina.conf`, ajustar
   dominios e executar:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

8. Gerar certificados SSL com Certbot para `teamtupina.com.br`,
   `www.teamtupina.com.br` e `app.teamtupina.com.br`.

## Rotina de atualizacao

```bash
cd /opt/team-tupina/wger
git pull
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env build web
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env up -d
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env exec web python3 manage.py migrate
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env exec web python3 manage.py collectstatic --no-input
```

## Backup

Backup diario minimo:

```bash
mkdir -p /opt/team-tupina/backups
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env exec -T postgres \
  pg_dump -U "$DJANGO_DB_USER" "$DJANGO_DB_DATABASE" \
  > /opt/team-tupina/backups/wger-$(date +%F).sql
docker run --rm \
  -v team_tupina_media:/data \
  -v /opt/team-tupina/backups:/backup \
  alpine tar -czf /backup/media-$(date +%F).tar.gz -C /data .
```

Politica recomendada:

- 7 backups diarios.
- 4 backups semanais.
- 12 backups mensais.
- Copia criptografada fora do servidor.
- Teste de restauracao mensal.

## Checklist de seguranca

- `DEBUG=False`.
- `SECRET_KEY` e `SIGNING_KEY` persistentes e secretos.
- `ALLOWED_HOSTS` restrito aos dominios reais.
- `CORS_ALLOWED_ORIGINS` restrito aos dominios reais.
- HTTPS obrigatorio.
- Admin com senha forte e, se possivel, MFA no provedor.
- Firewall liberando apenas 22, 80 e 443.
- SSH por chave, sem login root por senha.
- Backup externo testado.
- Logs e alertas de erro configurados.
- Atualizacoes de sistema e imagens Docker em rotina mensal.
- Revisao de licenca AGPL e manutencao dos creditos do wger base.

## Integracao do ecossistema

O wger personalizado le estes links via settings:

- `TEAM_TUPINA_SITE_URL`
- `TEAM_TUPINA_PREMIUM_URL`
- `TEAM_TUPINA_RESET7_URL`
- `TEAM_TUPINA_INSTAGRAM_URL`
- `TEAM_TUPINA_WHATSAPP_URL`
- `TEAM_TUPINA_SUPPORT_EMAIL`

Esses links alimentam a landing, a barra de ecossistema e telas internas. Para
trocar dominio, altere somente o `.env` e reinicie o stack.

## Fontes oficiais consultadas

- wger Docker: https://github.com/wger-project/docker
- wger prod env: https://github.com/wger-project/docker/blob/master/config/prod.env
- Docker Compose: https://docs.docker.com/compose/
- Docker Compose em producao: https://docs.docker.com/compose/how-tos/production/
- Docker Engine Ubuntu: https://docs.docker.com/engine/install/ubuntu/
- Django deployment: https://docs.djangoproject.com/en/6.0/howto/deployment/
- Nginx reverse proxy: https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/
- Certbot: https://certbot.eff.org/
- PostgreSQL backup/pg_dump: https://www.postgresql.org/docs/current/app-pgdump.html
- Hetzner dedicated servers: https://www.hetzner.com/dedicated-rootserver
- OVHcloud bare metal: https://us.ovhcloud.com/bare-metal/
- DigitalOcean Droplets: https://www.digitalocean.com/pricing/droplets
- AWS Lightsail pricing: https://aws.amazon.com/lightsail/pricing/
