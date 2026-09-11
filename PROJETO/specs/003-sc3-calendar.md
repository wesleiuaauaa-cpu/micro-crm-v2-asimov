# 003 — SC3 Agendamento → Calendar (Make)

**Trigger:** `Google Sheets > Watch New Rows` em `AGENDAMENTOS`, intervalo 15 min (Free) — só dispara quando há linha nova.

## Módulos (3 ops/evento)

| # | Módulo | Config | Ops |
|---|---|---|---|
| 1 | **Watch New Rows** | Sheet `AGENDAMENTOS`, `Choose a method: By created time`, 15 min | 1 |
| 2 | **Filter** | `status == agendado AND calendar_event_id == ""` | 0 |
| 3 | **Google Calendar > Create an Event** | Calendar do lojista, `Summary: {{titulo}} - {{nome}}`, `Start: {{data_hora}}`, `End: {{data_hora+1h}}` | 1 |
| 4 | **Google Sheets > Update a Row** | `calendar_event_id = {{id do evento}}`, `status = confirmado` | 1 |

**Erro:** Handler → `Update Row` com `status=pendente_sync` + `LOGS` Add Row + `Telegram` ao prestador. SC2 reprocessa `pendente_sync` no dia seguinte.

## Blueprint rascunho

```json
{
  "name": "SC3 - Calendar",
  "trigger": {"type": "google-sheets:watchNewRows", "sheet": "AGENDAMENTOS", "interval": 15},
  "modules": [
    {"id": 1, "type": "google-sheets:watchNewRows"},
    {"id": 2, "type": "filter", "condition": "status == 'agendado' && calendar_event_id == ''"},
    {"id": 3, "type": "google-calendar:createEvent", "params": {"calendar": "{{CONFIG.calendar_id}}", "summary": "{{titulo}}", "start": "{{data_hora}}"}},
    {"id": 4, "type": "google-sheets:updateRow", "params": {"calendar_event_id": "{{event.id}}", "status": "confirmado"}}
  ]
}
```

## Checklist RN-08
- `calendar_event_id` vazio antes de criar
- `data_hora` em `America/Sao_Paulo`, formato `DD/MM/YYYY HH:mm` → Make converte para ISO
- SLA 15 min (Free) — avisar lojista

→ Skipped: `Update` via Calendar API direta (módulo nativo já faz), add quando precisar de `attendees`.

## Teste T6
Adicionar linha `AGENDAMENTOS` com `agendado` → em ≤15 min evento aparece no Calendar e `calendar_event_id` preenchido.
