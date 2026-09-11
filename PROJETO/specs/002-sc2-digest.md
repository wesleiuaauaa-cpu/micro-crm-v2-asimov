# 002 — SC2 Digest Diário + Relatório Semanal (Make)

**Trigger:** `Schedule` diário `08:00` `America/Sao_Paulo` (seg–sáb digest, domingo relatório). 1 cenário só (RN-10).

## Módulos (4-10 ops/dia)

| # | Módulo Make | Config | Ops |
|---|---|---|---|
| 1 | **Schedule** | `Every day at 08:00`, Timezone `America/Sao_Paulo` (CONFIG.fuso) | 1 |
| 2 | **Google Sheets > Search Rows** `OPORTUNIDADES` | `estagio in (novo,em_analise,proposta_enviada) AND proximo_contato <= hoje` | 1 |
| 3 | **Router** | — | 0 |
| 4a | **Branch digest (default)** → `Text Aggregator` → `Telegram SendMessage` | Aggregator: `{{cliente}} — {{descricao}} · {{aux_atraso}}d · R${{valor}}` | 1+1 |
| 4b | **Branch domingo** (`formatDate(now; "dddd") == "Sunday"`) → +2 Searches + Telegram | `fechado` semana + `AGENDAMENTOS` próxima semana | 2+1 |

**Total:** digest 4-8 ops, domingo 8-10 ops. Dentro do Free.

## Templates (copiar para Telegram)

```text
Digest (seg–sáb):
📌 Follow-ups de hoje ({{hoje DD/MM}}) — {{n}} em atraso:
{{#each atrasadas}}
{{@index}}. {{nome}} — {{descricao}} · sem retorno há {{aux_atraso}}d · R$ {{valor}}
{{/each}}
→ responda pelo WhatsApp e atualize 'proximo_contato' na planilha.

Relatório domingo:
📊 Semana {{dd}}/{{mm}} — {{nome_negocio}}
Novos: {{n_novos}} · Em aberto: R$ {{pipeline}}
Ganhos: R$ {{ganho}} ({{qtd_fechado}}) · Perdidos: {{qtd_perdido}}
⚠️ Sem retorno >48h: {{atraso}} · Agenda próxima semana: {{agenda}}
💡 Valor recuperado: R$ {{recuperado}}
```

## Blueprint rascunho (JSON)

```json
{
  "name": "SC2 - Digest + Relatório",
  "schedule": {"type": "daily", "time": "08:00", "timezone": "America/Sao_Paulo"},
  "modules": [
    {"id": 1, "type": "schedule", "params": {"interval": "daily", "time": "08:00"}},
    {"id": 2, "type": "google-sheets:searchRows", "params": {"sheet": "OPORTUNIDADES", "filter": "estagio IN (novo,em_analise,proposta_enviada) AND proximo_contato <= TODAY()"}},
    {"id": 3, "type": "router", "routes": [
      {"name": "domingo", "filter": "formatDate(now; \"dddd\") == \"Sunday\""},
      {"name": "digest", "filter": "true"}
    ]}
  ],
  "notes": "Router não consome ops. Aggregator antes do Telegram. Ver RN-04, RN-06, RN-16."
}
```
> Honestidade: JSON é rascunho. Monte na UI em 15 min, valide `formatDate` gera `Sunday` em inglês.

## Checklist RN
- RN-04: `proximo_contato` é `date` (não datetime)
- RN-06: digest 08:00 seg–sáb, relatório domingo
- RN-16: `formatDate` com `dddd` em inglês — testar no Make

→ Skipped: agregação via Sheets fórmula (Sheets já tem `aux_atraso`), add quando volume >100 oportunidades.
