# Team Tupina - Conteudo PT-BR de treino e nutricao

Este documento registra a curadoria inicial da base Team Tupina em portugues
brasileiro para equipamentos, musculos, exercicios, alimentos e templates
publicos.

## Comando

Rode dentro do container ou ambiente Django:

```bash
python3 manage.py seed-team-tupina-ptbr --username teamadmin
```

O comando e idempotente: pode ser executado novamente para atualizar a base sem
apagar conteudo externo ao pacote Team Tupina.

Opcoes uteis:

```bash
python3 manage.py seed-team-tupina-ptbr --username teamadmin --skip-routines
python3 manage.py seed-team-tupina-ptbr --username teamadmin --skip-nutrition
```

## O que ele cria/atualiza

- Equipamentos de academia, peso livre, maquinas, cardio e acessorios.
- Grupos musculares em PT-BR.
- Categorias de exercicio em PT-BR.
- Exercicios com descricoes em portugues brasileiro.
- Ingredientes base com macros por 100g.
- Templates publicos Team Tupina:
  - `TT Reset 7 - Base`
  - `TT Forca Inicial 3x`
  - `TT Hipertrofia Upper Lower 4x`
  - `TT Gluteos e Pernas`
  - `TT Condicionamento 20min`

## Diretrizes usadas

- Priorizar consistencia e aderencia, nao complexidade desnecessaria.
- Cobrir grandes grupos musculares ao longo da semana.
- Manter alternativas com peso corporal, elasticos, maquinas e pesos livres.
- Usar RIR/descanso/volume como guia pratico para professor ajustar depois.
- Evitar promessas medicas ou garantias de resultado.

## Fontes de referencia

- ACSM, atualizacao de 2026 sobre treinamento resistido: consistencia,
  individualizacao e cobertura de objetivos como forca, hipertrofia e potencia.
  https://acsm.org/resistance-training-guidelines-update-2026/
- OMS, recomendacoes gerais de atividade fisica: adultos com 150 min semanais
  de atividade moderada ou equivalente e fortalecimento dos principais grupos
  musculares 2 ou mais dias por semana.
  https://www.who.int/initiatives/behealthy/physical-activity
- CDC, resumo adulto de atividade fisica: 150 min semanais e 2 dias de
  fortalecimento muscular.
  https://www.cdc.gov/physical-activity-basics/guidelines/adults.html
- Documentacao wger de rotinas: estrutura Routine > Day > Slot > SlotEntry e
  exposicao de templates publicos por `/api/v2/public-templates/`.
  https://wger.readthedocs.io/en/latest/api/routines.html

## Proximas evolucoes

- Importar imagens proprias de exercicios Team Tupina.
- Criar templates por perfil: iniciante, intermediario, mulher 35+, RESET 7,
  hipertrofia, recomposicao e condicionamento.
- Revisar alimentos com nutricionista antes de usar como prescricao formal.
- Conectar tags por objetivo para professores filtrarem templates com rapidez.
