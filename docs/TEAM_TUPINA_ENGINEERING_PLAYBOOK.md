# Team Tupina - Engineering Playbook

Atualizado em 2026-06-26.

Este playbook aplica ao projeto Team Tupina os principios do compendio anexado:
complexidade controlada, requisitos rastreaveis, arquitetura com fronteiras,
testes de legado, seguranca em refatoracao e operacao DevOps saudavel.

## 1. Principios operacionais

1. Mudancas pequenas, verificaveis e reversiveis.
2. Personalizacao Team Tupina fora do core upstream sempre que possivel.
3. Seguranca e dados de alunos/professores tratados como requisito de produto.
4. Todo deploy precisa de evidencias: checks, auditoria, rotas e rollback.
5. Decisoes arquiteturais importantes entram em ADR.

## 2. Mapa de fronteiras

| Area | Responsabilidade | Regra de mudanca |
| --- | --- | --- |
| Site estatico raiz | Marketing, Premium, RESET 7, SEO e assets publicos | Pode evoluir rapido, mas sempre passar HTML/JS validation |
| `wger/settings` | Configuracao, seguranca, ambiente e deploy | Mudancas com `manage.py check` e registro em docs |
| `wger/wger/core/templates` | Shell do sistema, navegacao, dashboard e login | Customizacao permitida, preservar compatibilidade wger |
| `wger/wger/core/static/css/team-tupina-system.css` | Tema visual global Team Tupina no app | Ponto preferido para UX global |
| `wger/wger/software` | Landing institucional dentro do wger | Pode ter CSS proprio, validado em desktop/mobile |
| `mobile/team-tupina-app` | App Android/iOS baseado no wger | Alteracoes exigem SDK Flutter/Dart/Java instalados para build |
| `deploy/production` | Stack de producao | Qualquer mudanca precisa de checklist pre-deploy |

## 3. Politica de complexidade

Antes de criar abstracao nova, responder:

- Isso reduz duplicacao real ou apenas antecipa um futuro incerto?
- O padrao ja existe no wger ou no site?
- O teste/validacao ficara mais simples depois da mudanca?
- A mudanca pode ser revertida sem afetar dados de alunos?

Sinais de alerta:

- CSS ou templates com regra muito especifica para uma unica tela sem motivo.
- Configuracao de producao hardcoded fora do `.env`.
- Scripts que exigem passos manuais nao documentados.
- Customizacao que apaga creditos/licenca do wger base.

## 4. Engenharia de requisitos

Todo requisito de produto deve ter:

- Perfil afetado: admin, professor, aluno ou visitante.
- Fluxo principal.
- Evidencia de validacao.
- Risco de seguranca/dados.
- Arquivos principais tocados.

A matriz viva fica em `docs/TEAM_TUPINA_REQUIREMENTS_TRACEABILITY.md`.

## 5. Arquitetura de personalizacao

O projeto segue uma fronteira pratica inspirada em ports/adapters:

- Nucleo herdado: regras e modelos do wger.
- Adaptadores Team Tupina: templates, CSS, fixtures, settings e links de ecossistema.
- Canais externos: site estatico, app mobile, WhatsApp, Instagram, SMTP e deploy.

Regra: o nucleo wger so deve ser alterado quando a personalizacao nao puder ser
feita por settings, template, CSS, fixtures ou adapter documentado.

## 6. Testes e quality gate

Rodar antes de entregar mudancas relevantes:

```powershell
.\scripts\quality\team-tupina-quality-gate.ps1
```

Para ambiente sem internet:

```powershell
.\scripts\quality\team-tupina-quality-gate.ps1 -SkipNetworkAudits
```

Para validacao sem servidores locais ativos:

```powershell
.\scripts\quality\team-tupina-quality-gate.ps1 -SkipHttpProbes
```

O gate cobre:

- Django system check.
- Testes de login.
- Ruff na superficie customizada.
- Sintaxe JS do site.
- HTML validate do site estatico.
- Auditoria npm e Python.
- Checagem mobile/backend.
- Probes HTTP locais.
- `git diff --check`.

## 7. Seguranca em legado

Ao alterar legado wger:

1. Rodar check/teste antes, quando possivel.
2. Alterar menor superficie necessaria.
3. Evitar refatoracao estrutural junto com mudanca visual.
4. Rodar quality gate.
5. Documentar risco residual no manual ou ADR.

Regras de producao:

- `DJANGO_DEBUG=False`.
- `SECRET_KEY` e `SIGNING_KEY` reais.
- `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` e `CORS_ALLOWED_ORIGINS` restritos.
- HTTPS obrigatorio.
- Backups testados.
- Usuarios de teste nunca usados em producao.

## 8. DevOps e cultura

Metrica minima por release:

| Metrica | Como medir no projeto |
| --- | --- |
| Frequencia de deploy | Tags/releases publicadas |
| Lead time | Tempo entre tarefa aprovada e deploy |
| Falha de mudanca | Incidentes/rollback por release |
| Tempo de recuperacao | Tempo para restaurar servico apos incidente |

Postura operacional:

- Falha vira aprendizado, nao culpa.
- Incidente gera checklist ou automacao.
- Toda decisao relevante deixa rastro em ADR.
- O time de produto deve conseguir rodar o ambiente local com scripts.

## 9. Definition of Done

Uma mudanca so esta pronta quando:

- O fluxo pedido funciona localmente.
- O quality gate relevante passou ou a excecao foi documentada.
- Responsividade foi verificada quando houver UI.
- Riscos de seguranca/dados foram revisados.
- Documentacao foi atualizada quando alterou deploy, operacao ou comportamento.

