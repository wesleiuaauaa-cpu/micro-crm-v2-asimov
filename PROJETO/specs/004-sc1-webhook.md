# 004 — SC1 Entrada de Lead por WhatsApp (WAHA/Z-API → Sheets)

**Trigger:** `Webhooks > Custom webhook` (instantâneo, 1 op). Capturar payload real antes de mapear.

## Contrato normalizado (o que SC1 espera)
```json
{"telefone":"5531999990000","texto":"quanto custa limpeza?","fromMe":false,"eh_grupo":false,"msg_id":"ABC123"}
```
**Regra:** só mapear após `curl` de teste com payload real da WAHA/Z-API (seção Payloads).

## Módulos (5-6 ops/msg)

| # | Módulo | Config | Ops |
|---|---|---|---|
| 1 | **Custom Webhook** | `POST /wa-mc-<slug>` | 1 |
| 2 | **Set Variable: telefone_norm** | `=replace({{telefone}}; "/\D/g"; "")` → se len 10-11 sem 55, prefixar `55` | 0 |
| 3 | **Google Sheets > Search Rows** `CLIENTES` | `telefone_norm = {{telefone_norm}}` | 1 |
| 4 | **Router** (3 paths) | — | 0 |

**Router:**
- **Path A — cliente novo** (`length(Search)==0 && fromMe==false && eh_grupo==false`):
  A1 Add CLIENTES (`CLI-...`, `Sem nome XXXX`, `telefone_norm`, `ultima_interacao=now`, `ultima_auto_resposta=now` se janela ok) · A2 Add OPORTUNIDADES (`OPP-...`, `novo`, `proximo_contato=TODAY()+2`) · A3 Add INTERACOES (`recebida`) · A4 HTTP send (WAHA/Z-API) filtrado por `auto_resposta_ativa==SIM && now-ultima_auto_resposta > janela` · A5 Telegram lojista. **6 ops.**
- **Path B — cliente existente**: B1 Update CLIENTES (`ultima_interacao=now`, `ultima_auto_resposta` condicional) · B2 Add INTERACOES · B3 HTTP · B4 Telegram. **5 ops.**
- **Path C — `fromMe==true` ou `eh_grupo==true`**: nenhum módulo. **1 op** total.

**Debounce (ponytail: Data Store, não Redis)**
```text
# ponytail: Data Store (Make nativo) em vez de Redis externo, evita VPS. Troque por Upstash Redis via HTTP se volume >100 msgs/dia.
```
Após `Edit Fields` normalizado, antes do Router:
- `Data Store > Add` (`key=telefone_norm`, `value=texto`, `TTL=20s`) → `Sleep 10s` → `Data Store > Get` → `If` (texto == último) → só então entra no Router. Junta “oi” + “quanto custa?” em 1 lead.

**Adapters (confirmar doc antes do M3):**
- **WAHA:** `POST http://waha:3000/api/sendText` `{"chatId":"{{telefone}}@c.us","text":"{{auto_resposta}}","session":"wa-{{slug}}"}` header `X-Api-Key`
- **Z-API:** `POST https://api.z-api.io/instances/{{id}}/token/{{tk}}/send-text` `{"phone":"{{telefone}}","message":"{{auto_resposta}}"}` header `Client-Token`

## Blueprint rascunho
```json
{
  "name": "SC1 - Lead WA (WAHA/Z-API)",
  "trigger": {"type": "custom-webhook", "path": "wa-mc-clinica"},
  "modules": [
    {"id":1,"type":"webhook"},
    {"id":2,"type":"setVariable","telefone_norm":"replace(digits)"},
    {"id":3,"type":"google-sheets:searchRows","sheet":"CLIENTES"},
    {"id":4,"type":"router","routes":["novo","existente","ignorar"]},
    {"id":"4a","type":"data-store:add","ttl":20},
    {"id":"4b","type":"sleep","seconds":10}
  ]
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
