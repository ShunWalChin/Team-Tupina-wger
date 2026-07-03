# Team Tupina production deploy

Arquivos desta pasta:

- `docker-compose.team-tupina.yml`: stack de producao.
- `team-tupina.env.example`: modelo para `.env`.
- `nginx.team-tupina.conf`: reverse proxy para site e app.

Fluxo rapido:

```bash
cp deploy/production/team-tupina.env.example .env
nano .env
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env config
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env build
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env up -d
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env exec web python3 manage.py migrate
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env exec web python3 manage.py collectstatic --no-input
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env exec web python3 manage.py createsuperuser
```

Manual completo:

```text
docs/TEAM_TUPINA_MANUAL_COMPLETO.md
```

Relatorio de validacao:

```text
docs/TEAM_TUPINA_VALIDACAO_PRE_DEPLOY.md
```
