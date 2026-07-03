# Team Tupina wger - Validacao pre-deploy

Data: 2026-06-11
Ambiente: local Windows, wger em `http://127.0.0.1:8002/`

## Rodada de hardening e UX - 2026-06-19

Status: aprovado para continuidade de testes locais e preparacao de deploy.

Pontos corrigidos nesta rodada:

- `django-axes` voltou a usar handler de banco por padrao em producao, evitando
  falha de rastreamento de tentativas de login quando cache nao esta preparado.
- CORS de producao deixou de aceitar qualquer origem automaticamente; usar
  `CORS_ALLOWED_ORIGINS` no `.env` com os dominios reais.
- Dependencias vulneraveis atualizadas: `django==6.0.6`,
  `cryptography==48.0.1`, `pyjwt==2.13.0` e `tornado==6.5.7`.
- Navegacao interna recebeu wordmark oficial Team Tupina.
- Dashboard recebeu hero refinado, titulo correto, botoes de acao e grid
  responsivo estavel para os cards React/MUI.
- Landing wger recebeu ajustes de legibilidade, raio visual e alvos de toque.
- Site estatico teve problemas de validacao HTML corrigidos em `index.html`,
  `premium.html` e `reset-7.html`.

Checks executados:

```text
python manage.py check                         OK
python manage.py test wger.core.tests.test_user_login --keepdb  OK, 12 testes
uvx pip-audit --path .venv\Lib\site-packages  OK, sem vulnerabilidades conhecidas
npm audit --omit=dev --audit-level=moderate   OK, 0 vulnerabilidades
npx html-validate index.html premium.html reset-7.html privacy.html terms.html  OK
node --check script.js                         OK
git diff --check                               OK
```

Rotas HTTP validadas localmente:

| URL | Resultado |
| --- | --- |
| `http://127.0.0.1:8000/` | 200 |
| `http://127.0.0.1:8000/premium.html` | 200 |
| `http://127.0.0.1:8000/reset-7.html` | 200 |
| `http://127.0.0.1:8002/pt-br/software/features` | 200 |
| `http://127.0.0.1:8002/pt-br/dashboard` | 200 |
| `http://127.0.0.1:8002/api/v2/version/` | 200 |

Responsividade medida no browser local:

| Tela | Viewport | Resultado |
| --- | --- | --- |
| Dashboard | 1280 x 720 | Sem overflow horizontal; cards em grid de 3 colunas |
| Dashboard | 390 x 844 | Sem overflow horizontal; cards em 1 coluna |
| Landing wger | 1280 x 720 | Sem overflow horizontal; marca e hero OK |
| Landing wger | 390 x 844 | Sem overflow horizontal; botoes com alvo de toque de 44px |

Pendencia local para mobile nativo:

- Backend responde para o app (`/api/v2/`, `/version/`, `/min-app-version/`).
- Flutter, Dart e Java ainda nao estao no PATH desta maquina; instalar SDKs
  antes de compilar Android/iOS.

## Rodada de governanca de engenharia - 2026-06-26

Objetivo: aplicar o compendio de engenharia anexado ao projeto, transformando
principios de complexidade, arquitetura, requisitos, testes, seguranca e DevOps
em artefatos executaveis.

Artefatos adicionados:

- `docs/TEAM_TUPINA_ENGINEERING_PLAYBOOK.md`
- `docs/TEAM_TUPINA_REQUIREMENTS_TRACEABILITY.md`
- `docs/adr/0001-team-tupina-customization-boundaries.md`
- `../scripts/quality/team-tupina-quality-gate.ps1`

Checks executados pelo quality gate:

```text
Django system check              OK
Django login regression tests    OK, 12 testes
Ruff custom surface              OK
Static JS syntax                 OK
Static HTML validation           OK
npm dependency audit             OK, 0 vulnerabilidades
Python dependency audit          OK, sem vulnerabilidades conhecidas
Whitespace diff check            OK
```

Avisos esperados no ambiente atual:

- Servidores locais `127.0.0.1:8000` e `127.0.0.1:8002` nao estavam ativos no
  momento da segunda execucao, por isso os HTTP probes retornaram WARN.
- Flutter, Dart e Java continuam ausentes no PATH, entao o check mobile em modo
  estrito retorna WARN ate os SDKs serem instalados.

Comando recomendado para validacao recorrente:

```powershell
.\scripts\quality\team-tupina-quality-gate.ps1
```

Para validacao offline ou sem servidores locais:

```powershell
.\scripts\quality\team-tupina-quality-gate.ps1 -SkipNetworkAudits -SkipHttpProbes
```

## Resultado geral

Status: aprovado para etapa de deploy controlado.

Pontos corrigidos durante a validacao:

- Navegacao principal passou a expandir apenas em telas grandes.
- Dashboard React/MUI passou a usar layout de coluna unica tambem em tablets.
- Rodape foi ajustado para impedir overflow lateral do seletor de idioma em 768px.
- Configuracao de producao passou a respeitar `ALLOWED_HOSTS` do `.env`.
- `SecurityMiddleware` foi ativado no settings de producao.
- Variaveis de Celery do exemplo de ambiente foram alinhadas com `settings/main.py`.
- Docker Compose recebeu healthchecks para PostgreSQL e Redis.

## Checks tecnicos locais

Comando:

```bash
DJANGO_SETTINGS_MODULE=settings.local_dev uv run python manage.py check
```

Resultado:

```text
System check identified no issues (0 silenced).
```

## Perfis de teste

Usuarios validados no ambiente local:

| Perfil | Usuario | Resultado |
| --- | --- | --- |
| Admin | `teamadmin` | Login OK |
| Professor | `professor.teste` | Login OK |
| Aluno | `aluno.teste` | Login OK |

Rotas autenticadas testadas com os tres perfis:

| Tela | URL resolvida | Admin | Professor | Aluno |
| --- | --- | --- | --- | --- |
| Dashboard | `/en/dashboard` | 200 | 200 | 200 |
| Login autenticado | `/en/user/login` | 302 dashboard | 302 dashboard | 302 dashboard |
| Treinos | `/en/routine/overview` | 200 | 200 | 200 |
| Nutricao | `/en/nutrition/overview/` | 200 | 200 | 200 |
| Medidas | `/en/measurement/` | 200 | 200 | 200 |

## Responsividade visual

Viewports testados:

- Mobile: 390 x 844
- Tablet: 768 x 1024
- Desktop: 1366 x 900

Telas testadas:

- Dashboard: `/pt-br/dashboard`
- Treinos: `/pt-br/routine/overview`
- Nutricao: `/pt-br/nutrition/overview/`
- Medidas: `/pt-br/measurement/`
- Landing de recursos: `/pt-br/software/features`
- API: `/pt-br/software/api`

Resultado por criterio:

| Criterio | Resultado |
| --- | --- |
| Branding Team Tupina visivel | OK |
| CSS global Team Tupina nas telas internas | OK |
| Hero do dashboard | OK |
| Cards React/MUI do dashboard | OK |
| Overflow horizontal mobile | OK |
| Overflow horizontal tablet | Corrigido e OK |
| Overflow horizontal desktop | OK |
| Imagens quebradas | Nenhuma encontrada |
| Erros de console | Nenhum encontrado nas telas testadas |

Observacao: a landing `/software/features` usa template proprio de marketing e nao carrega `team-tupina-system.css`, por desenho. Ela foi validada separadamente sem overflow e sem imagens quebradas.

## Producao/Django deploy check

Comando usado com `deploy/production/team-tupina.env.example`:

```bash
DJANGO_SETTINGS_MODULE=settings.main uv run python manage.py check --deploy
```

Resultado: sem erros bloqueantes. Avisos remanescentes:

- Avisos `drf_spectacular` herdados da geracao de schema OpenAPI do wger.
- `security.W021`: `SECURE_HSTS_PRELOAD=False`.

Decisao: manter `SECURE_HSTS_PRELOAD=False` no primeiro deploy. Ativar somente depois de validar HTTPS em todos os subdominios, porque preload HSTS e uma decisao de longo prazo.

## Docker

Docker nao esta instalado no ambiente Windows local usado nesta validacao.

Foi validado localmente:

- Sintaxe YAML do compose.
- Existencia dos servicos `web`, `celery-worker`, `celery-beat`, `postgres`, `redis`.
- Existencia dos arquivos de Dockerfile e comandos Celery usados pelo compose.

Validacao obrigatoria no servidor Linux:

```bash
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env config
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env build
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env up -d
docker compose -f deploy/production/docker-compose.team-tupina.yml --env-file .env ps
```

## Checklist antes de publicar

- Trocar todas as senhas de teste.
- Gerar `SECRET_KEY` e `SIGNING_KEY` reais.
- Configurar dominio real em `SITE_URL`, `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`.
- Configurar SMTP real.
- Revisar `TEAM_TUPINA_WHATSAPP_URL`.
- Rodar `docker compose config` no servidor.
- Rodar migrations e collectstatic.
- Criar superuser real.
- Configurar SSL com Certbot.
- Testar login admin em `https://app.teamtupina.com.br`.
- Fazer primeiro backup manual antes de liberar usuarios.
