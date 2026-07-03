# ADR 0001 - Fronteiras de customizacao Team Tupina sobre wger

Data: 2026-06-26

## Status

Aceita.

## Contexto

O projeto usa o wger como base de treino, nutricao, medidas, usuarios e API.
Ao mesmo tempo, precisa parecer e operar como ecossistema Team Tupina: site,
landing, Premium, RESET 7, app mobile, identidade visual e fluxos de alunos e
professores.

Sem fronteiras explicitas, a personalizacao tende a se espalhar pelo core wger,
aumentando custo de atualizacao, risco de regressao e dificuldade de auditoria.

## Decisao

Separar customizacao em camadas:

1. **Configuracao**: `settings/main.py`, `settings/local_dev.py`,
   `deploy/production/team-tupina.env.example`.
2. **Tema e UX global**: `wger/core/static/css/team-tupina-system.css`.
3. **Templates de shell**: `navigation.html`, `template.html`,
   `template_features.html`, `login.html` e emails.
4. **Landing wger**: `wger/software/templates` e
   `wger/software/static/css/landing_page.css`.
5. **Assets de marca**: imagens em `wger/core/static/images`,
   `wger/software/static/images` e `assets/`.
6. **Mobile**: customizacoes isoladas em `mobile/team-tupina-app`.
7. **Documentacao e operacao**: `wger/docs`, `deploy/production` e
   `scripts`.

O core funcional do wger deve ser alterado somente quando settings, templates,
fixtures, CSS ou adapter documentado nao resolverem o requisito.

## Consequencias

Beneficios:

- Upgrade futuro do wger fica menos arriscado.
- Auditoria de seguranca encontra melhor a superficie customizada.
- UX pode evoluir sem tocar regras centrais de treino/nutricao.
- O ecossistema Team Tupina fica rastreavel.

Custos:

- Algumas telas herdadas ainda podem exigir overrides CSS mais especificos.
- Decisoes de produto precisam virar settings/env quando forem variaveis por
  ambiente.
- Novos desenvolvedores precisam consultar este ADR antes de refatorar.

## Regras de validacao

- Rodar `scripts/quality/team-tupina-quality-gate.ps1`.
- Se tocar UI, validar desktop e mobile.
- Se tocar settings/deploy, atualizar `.env.example` e manuais.
- Se tocar dados, login ou permissoes, rodar testes Django relevantes.

