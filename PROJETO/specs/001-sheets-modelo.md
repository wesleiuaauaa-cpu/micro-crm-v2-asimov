# 001 — Modelo Sheets (5 abas no M0) — MVP Micro-CRM v2

**Objetivo:** Template replicável em 2h. 1 planilha por cliente, na conta Google do lojista.
**Padrão BR:** `America/Sao_Paulo`, `DD/MM/YYYY HH:mm`, `R$`, `telefone_norm` = só dígitos.

## O que entregar
- 5 CSVs em `specs/csvs/` (M0) com headers + 5 linhas fake (clínica)
- 2 CSVs em `specs/_backlog/` (`LOGS.csv`, `FATURAMENTO.csv`) — só em M4, sob demanda
- Fórmulas prontas para colar (pipeline + atraso)
- Validações de lista (documentadas, não no CSV)

## Como usar (humano, 30 min)
1. Crie pasta Drive `MC-<slug>` na conta do lojista
2. Crie planilha `MC-<slug>-DB`
3. Para cada CSV: `Arquivo → Importar → Anexar → Substituir` (cria aba com mesmo nome)
4. Validações: formate coluna como lista (ver seção Validações)
5. Cole fórmulas da seção Fórmulas
6. Ajuste `CONFIG` com dados reais

## Validações (fazer no Sheets)
- `CLIENTES.origem`: `whatsapp,indicacao,presencial,outro`
- `CLIENTES.status_relacionamento`: `lead,ativo,inativo`
- `OPORTUNIDADES.estagio`: `novo,em_analise,proposta_enviada,aguardando,fechado,perdido`
- `OPORTUNIDADES.origem`: idem
- `OPORTUNIDADES.perdida_motivo`: `preco,prazo,sem retorno,outro` (obrigatório se `perdido`)
- `AGENDAMENTOS.status`: `agendado,confirmado,realizado,cancelado,no_show,pendente_sync`

## Fórmulas (colar como está)
```text
# OPORTUNIDADES — célula J1 (ou solta):
Pipeline aberto:
=SUMIFS(D:D; E:E; "<>fechado"; E:E; "<>perdido")

# OPORTUNIDADES — coluna H (aux_atraso), linha 2 e arrastar:
=SE(E2="";""; SE(OU(E2="fechado";E2="perdido");""; HOJE()-G2))

# FATURAMENTO — coluna G (margem), linha 2:
=D2-E2
```

## Abas
- `CLIENTES.csv` — 10 colunas, `telefone_norm` via `=REGEXREPLACE(C2;"\D";"")` no Sheets (sem módulo Make), criado_em = `=AGORA()`
- `OPORTUNIDADES.csv` — 13 colunas, `proximo_contato` = `=HOJE()+2` (dias_followup)
- `INTERACOES.csv` — 8 colunas
- `AGENDAMENTOS.csv` — 7 colunas, `calendar_event_id` vazio até SC3
- `CONFIG.csv` — chave|valor (12 linhas, ver V2 seção 5)
- `LOGS.csv` — 5 colunas → `_backlog/` (só M4)
- `FATURAMENTO.csv` — 8 colunas → `_backlog/` (só M4)

## Fake data (clínica)
5 clientes: Maria Silva (31) 98765-4321, João Oliveira, Ana Costa, Pedro Santos, Carla Mendes. 5 oportunidades: limpeza, clareamento, implante, ortodontia, avaliação. Valores R$ 150-3200. Estágios variados para testar digest.

## Checklist
- [ ] Abas criadas com nomes exatos
- [ ] Validações aplicadas
- [ ] Fórmulas coladas e testadas (mudar E2 para testar)
- [ ] CONFIG preenchido (nome_negocio, telegram_chat_id, etc)

→ Skipped: script de criação via API ( Sheets API exigiria OAuth extra), add quando replicação >5 clientes/mês.
