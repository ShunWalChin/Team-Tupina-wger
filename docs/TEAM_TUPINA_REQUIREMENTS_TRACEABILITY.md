# Team Tupina - Matriz de requisitos e rastreabilidade

Atualizado em 2026-06-26.

Esta matriz conecta requisitos do ecossistema Team Tupina a artefatos,
validacoes e riscos. Ela deve ser atualizada quando uma funcionalidade mudar.

## Legenda

| Campo | Significado |
| --- | --- |
| Perfil | Visitante, aluno, professor, admin ou operador |
| Evidencia | Check, teste, rota, documento ou inspecao visual |
| Risco | Principal risco caso a area falhe |

## Requisitos funcionais

| ID | Requisito | Perfil | Artefatos principais | Evidencia atual | Risco |
| --- | --- | --- | --- | --- | --- |
| TT-REQ-001 | Site institucional abre localmente e comunica a proposta Team Tupina | Visitante | `index.html`, `styles.css`, `assets/` | `npx html-validate`, HTTP 200 em `:8000/` | Perda de conversao e marca inconsistente |
| TT-REQ-002 | Landing Premium e RESET 7 funcionam como funis separados | Visitante | `premium.html`, `reset-7.html` | HTML validate e HTTP 200 | Quebra de venda ou checkout |
| TT-REQ-003 | wger exibe identidade visual Team Tupina nas telas internas | Aluno/professor/admin | `team-tupina-system.css`, `template.html`, `navigation.html` | Inspecao responsiva e HTTP 200 dashboard | Experiencia fragmentada |
| TT-REQ-004 | Dashboard mostra atalhos de treino, nutricao e medidas | Aluno/professor | `template.html`, React dashboard wger | Mobile/desktop sem overflow | Usuario nao encontra o fluxo principal |
| TT-REQ-005 | Login local de admin, professor e aluno permanece funcional | Todos autenticados | `wger/core`, fixtures, settings | `wger.core.tests.test_user_login` | Bloqueio operacional |
| TT-REQ-006 | API do wger responde para web/mobile | Mobile/app externo | `wger/api`, settings, CORS | HTTP 200 em `/api/v2/version/` | App mobile sem comunicacao |
| TT-REQ-007 | App mobile tem identidade Team Tupina e aponta para backend local/producao | Aluno/professor | `mobile/team-tupina-app` | `scripts/mobile/check-mobile-env.ps1` | App inconsistente ou sem backend |
| TT-REQ-008 | Documentacao de producao permite deploy real | Operador | `deploy/production`, `wger/docs` | Revisao documental e quality gate | Deploy improvisado |

## Requisitos nao funcionais

| ID | Requisito | Artefatos principais | Evidencia atual | Risco |
| --- | --- | --- | --- | --- |
| TT-NFR-001 | Producao com secrets persistentes e seguros | `.env`, `settings/main.py` | Manuais e `team-tupina.env.example` | Sessao/token invalidos ou exposicao |
| TT-NFR-002 | CORS/CSRF/hosts restritos em producao | `settings/main.py`, `.env.example` | `manage.py check`, docs | API exposta para origens indevidas |
| TT-NFR-003 | Dependencias sem vulnerabilidades conhecidas | `pyproject.toml`, `package-lock.json` | `pip-audit`, `npm audit` | Risco de exploracao por pacote |
| TT-NFR-004 | UI responsiva sem overflow horizontal | CSS wger/site | Browser checks mobile/desktop | Uso ruim em smartphone |
| TT-NFR-005 | Mudancas futuras passam por gate repetivel | `scripts/quality/team-tupina-quality-gate.ps1` | Execucao do script | Regressao manual nao detectada |
| TT-NFR-006 | Customizacao preserva atualizabilidade do wger | ADR 0001, playbook | Revisao de diff | Fork impossivel de manter |

## Quality gates por tipo de mudanca

| Tipo de mudanca | Checks obrigatorios |
| --- | --- |
| Site estatico | `node --check script.js`, `npx html-validate ...`, HTTP probes |
| Tema/UX wger | `manage.py check`, browser mobile/desktop, HTTP dashboard |
| Login/permissoes | `manage.py test wger.core.tests.test_user_login --keepdb` |
| Settings/deploy | `manage.py check --deploy` com `.env` de homologacao, revisar docs |
| Dependencias | `pip-audit`, `npm audit`, testes de regressao |
| Mobile | `scripts/mobile/check-mobile-env.ps1`, Flutter build quando SDK existir |

## Pendencias conhecidas

- Flutter, Dart e Java precisam estar no PATH para compilar Android/iOS nesta
  maquina.
- PowerSync endpoint ainda nao existe no backend local; app mobile usa modo
  local/API-only enquanto a integracao final nao for implementada.
- Docker deve ser validado em servidor Linux real antes de producao.

