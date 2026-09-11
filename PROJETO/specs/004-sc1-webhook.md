# 004 — SC1 Entrada de Lead por WhatsApp (WAHA → Sheets)

**Trigger:** `Webhooks > Custom webhook` (instantâneo, 1 op). Capturar payload real WAHA antes de mapear.

## Contrato normalizado (o que SC1 espera)
```json
{"telefone":"5531999990000","texto":"quanto custa limpeza?","fromMe":false,"eh_grupo":false,"msg_id":"ABC123"}
```
**Regra:** só mapear após `curl` de teste com payload real WAHA (seção Payloads).

## Módulos (4-5 ops/msg) — ponytail

| # | Módulo | Config | Ops |
|---|---|---|---|
| 1 | **Custom Webhook** | `POST /wa-mc-<slug>` | 1 |
| 2 | **Google Sheets > Search Rows** `CLIENTES` | `telefone_norm = {{telefone}}` (coluna `telefone_norm` já é `=REGEXREPLACE(C2;"\D";"")` no Sheets) | 1 |
| 3 | **Router** (3 paths) | — | 0 |

**Router:**
- **Path A — cliente novo** (`length(Search)==0 && fromMe==false && eh_grupo==false`):
  A1 Add CLIENTES (`CLI-...`, `Sem nome XXXX`, `telefone_norm`, `ultima_interacao=now`, `ultima_auto_resposta=now` se janela ok) · A2 Add OPORTUNIDADES (`OPP-...`, `novo`, `proximo_contato=TODAY()+2`) · A3 Add INTERACOES (`recebida`) · A4 HTTP send (WAHA/Z-API) filtrado por `auto_resposta_ativa==SIM && now-ultima_auto_resposta > janela` · A5 Telegram lojista. **6 ops.**
- **Path B — cliente existente**: B1 Update CLIENTES (`ultima_interacao=now`, `ultima_auto_resposta` condicional) · B2 Add INTERACOES · B3 HTTP · B4 Telegram. **5 ops.**
- **Path C — `fromMe==true` ou `eh_grupo==true`**: nenhum módulo. **1 op** total.

**Debounce (ponytail: 0 ops até provar necessidade)**
```text
# ponytail: debounce via Data Store/Sleep (2 ops/msg) adiado até >20 msgs/dia. MVP usa só If msg_id (0 ops) — se duplicidade virar problema, add Data Store + Sleep 10s.
```
*Atual:* sem debounce. Se cliente mandar “oi” + “quanto custa?” em 10s, cria 1 lead + 1 interação extra (aceitável no piloto clínica, <20 msgs/dia).

**Adapter (WAHA — congelado):**
- **WAHA:** `POST http://waha:3000/api/sendText` `{"chatId":"{{telefone}}@c.us","text":"{{auto_resposta}}","session":"wa-{{slug}}"}` header `X-Api-Key`
- *Nota Z-API fallback (não montar agora):* `POST https://api.z-api.io/instances/{{id}}/token/{{tk}}/send-text` `{"phone":"{{telefone}}","message":"{{auto_resposta}}"}` — 2 linhas, trocar URL/header se migrar.

## Blueprint rascunho
```json
{
  "name": "SC1 - Lead WA (WAHA)",
  "trigger": {"type": "custom-webhook", "path": "wa-mc-clinica"},
  "modules": [
    {"id":1,"type":"webhook"},
    {"id":2,"type":"google-sheets:searchRows","sheet":"CLIENTES","filter":"telefone_norm = {{telefone}}"},
    {"id":3,"type":"router","routes":["novo","existente","ignorar"]}
  ],
  "notes": "telefone_norm via REGEXREPLACE no Sheets. Sem Data Store no MVP. Z-API é troca de URL/header."
}
```

## Error handler
Todos os paths: `Incomplete execution` + `Sheets Add LOGS` + `Telegram` ao prestador. HTTP com retry 3x.

## Checklist RN-01..05,09
- RN-01: `telefone_norm` só dígitos, fallback sufixo 8 dígitos
- RN-02: `fromMe` e grupo não criam lead
- RN-05: `janela_auto_resposta_h` (24h) — usar `if(now - ultima_auto_resposta > janela)`
- RN-09: log só em erro + auto-resposta enviada

→ Skipped: dedupe `msg_id` (1 op/msg economizado), add quando duplicidade virar problema real.
