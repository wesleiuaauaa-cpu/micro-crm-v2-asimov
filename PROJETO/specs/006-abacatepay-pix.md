# 006 — Cobrança Pix via AbacatePay (Checkout Transparente)

**Origem:** `meio de pagamento que iremos implantar..txt` → https://docs.abacatepay.com → `POST /transparents/create` (PIX) + Webhooks `transparent.completed`
**Decisão:** Substitui Asaas/Mercado Pago. Ainda é Pix, mas pela API AbacatePay. PIX é instantâneo, sem boleto no MVP.

## 1. Onde entra no Micro-CRM

```
[OPORTUNIDADES.estagio = proposta_enviada] ──► [Make SC4: Cobrança Pix]
                                                    │
                                                    ├─► AbacatePay API → brCode + brCodeBase64
                                                    ├─► Sheets Update (pix_id, pix_status=PENDING, pix_brCode)
                                                    └─► WhatsApp (WAHA) → cliente recebe QR + copia-e-cola
                                                          │
[AbacatePay Webhook transparent.completed] ──► [Make SC4b: Confirmação]
                                                    └─► Sheets Update (pix_status=PAID, fechado_em, estagio=fechado) → Telegram lojista
```

**Gating:** SC4 só no plano Mensageiro/Oficial. Base continua sem cobrança (só digest).

## 2. Modelo de dados — ajuste mínimo (ponytail)

Não criar aba nova. Reuso `OPORTUNIDADES` + 4 colunas (já existem `valor`, `estagio`):

| Coluna nova em OPORTUNIDADES | Tipo | Regra |
|---|---|---|
| `pix_id` | texto | `pix_char_...` ou `bole_...` retornado pela AbacatePay |
| `pix_brCode` | texto | copia-e-cola (`000201...`) |
| `pix_status` | lista | `PENDING` → `PAID`/`EXPIRED`/`REFUNDED` |
| `pix_expiresAt` | data-hora | `expiresAt` da API |

*Ponytail: sem aba COBRANCAS separada. Uma aba a menos = menos ops, menos confusão. Crie COBRANCAS só quando precisar de 2 Pix por oportunidade.*

**CONFIG novas chaves:**

| chave | default | uso |
|---|---|---|
| `abacatepay_api_key` | — | **Nunca na planilha** — só em conexão HTTP Make (Bearer) — RN-17 |
| `abacatepay_webhook_secret` | — | Validação HMAC do webhook |
| `pix_expiresIn` | `3600` | 1h em segundos (abacatepay: `expiresIn`) |
| `pix_mensagem_template` | ver seção 4 | Texto enviado no WhatsApp com QR |

## 3. Cenários Make (2 cenários, 4-6 ops cada)

### SC4a — Gera Pix (trigger: Sheets Watch)
| # | Módulo | Config | Ops |
|---|---|---|---|
| 1 | **Sheets > Watch New/Updated Rows** `OPORTUNIDADES` | Filtro `estagio == proposta_enviada && pix_status == ""` | 1 |
| 2 | **HTTP > Make a request** `POST https://api.abacatepay.com/v2/transparents/create` | Headers `Authorization: Bearer {{abacatepay_api_key}}`, Body `{"method":"PIX","data":{"amount":{{valor*100}},"description":"{{descricao}} - {{cliente_nome}}","externalId":"{{id}}","metadata":{"oportunidadeId":"{{id}}","clienteId":"{{cliente_id}}"},"expiresIn":{{pix_expiresIn}}}}` | 1 |
| 3 | **Sheets > Update Row** | `pix_id={{data.id}}`, `pix_brCode={{data.brCode}}`, `pix_status={{data.status}}`, `pix_expiresAt={{data.expiresAt}}` | 1 |
| 4 | **HTTP > Make a request** (WAHA) | `POST {{waha_url}}/api/sendText` `{"chatId":"{{telefone_norm}}@c.us","text":"{{pix_mensagem_template}} + brCode","session":"wa-{{slug}}"}` | 1 |
| 5 | **Telegram** | Lojista: `Pix gerado para {{cliente}} R$ {{valor}} — expira {{pix_expiresAt}}` | 1 |

**Total 5 ops/Pix.** Sem `customer` no MVP (ponytail: sem CPF, sem `ensureSameTaxId`).

### SC4b — Confirma pagamento (trigger: Webhook AbacatePay)
| # | Módulo | Config | Ops |
|---|---|---|---|
| 1 | **Webhooks > Custom webhook** | `POST /abacate-webhook` (HTTPS, secret na URL) | 1 |
| 2 | **Filter** | `event == transparent.completed && data.metadata.oportunidadeId != ""` | 0 |
| 3 | **Sheets > Search Rows** `OPORTUNIDADES` | `id == {{data.metadata.oportunidadeId}}` | 1 |
| 4 | **Sheets > Update Row** | `pix_status=PAID`, `estagio=fechado`, `fechado_em={{now}}` | 1 |
| 5 | **Telegram** | `✅ Pix pago: {{cliente}} R$ {{valor}} — {{pix_id}}` | 1 |

**HMAC:** Make `Webhook` com `Validate HMAC` usando `abacatepay_webhook_secret`. Se falhar, descarta (RN-09).

## 4. Mensagem modelo (WhatsApp)

```text
Olá {{cliente_nome}}! Segue o Pix da {{nome_negocio}} para "{{descricao}}" — R$ {{valor}}.

Copia e cola:
{{pix_brCode}}

Ou escaneie o QR Code na imagem.

Expira em 1h ({{pix_expiresAt DD/MM HH:mm}} America/Sao_Paulo). Após pagar, me avise por aqui ✅

Dúvidas? Fale com {{responsavel}}.
```

*Imagem QR:* `brCodeBase64` é `data:image/png;base64,...` — no Make, use `HTTP > Get a file` se quiser enviar como imagem via WAHA `sendImage` (fase 2, não no MVP).

## 5. Configuração (humano, 15 min)

1. **AbacatePay:** Dashboard → Chaves de API → `Criar` → copie `Bearer` → crie conexão `HTTP` no Make chamada `abacate-{{slug}}` com header `Authorization: Bearer ...`
2. **Webhook:** Dashboard AbacatePay → Webhooks → `Criar` → URL `https://hook.make.com/abacate-{{slug}}` + `secret` (gere `openssl rand -hex 16`) + eventos `transparent.completed`, `transparent.refunded` → copie secret para `CONFIG.abacatepay_webhook_secret` (não na planilha, só no Make)
3. **Teste devMode:** no Make, use `devMode: true` no body ou crie cobrança de R$1,00 e simule com `POST /transparents/simulate-payment` (docs).

## 6. Custos e taxas (verificado 11/09/2026)

- Valores em **centavos** (`10000` = R$100,00)
- `platformFee` em exemplo: `5000` → `250` (5%) — confirmar no dashboard (varia por conta)
- Webhook: 1 op por pagamento confirmado (dentro do Free)

## 7. Checklist RN (adicionais)

- [ ] RN-17: `abacatepay_api_key` nunca na planilha, só na conexão HTTP
- [ ] RN-13: `pix_expiresAt` em `America/Sao_Paulo`, formato ISO da API já vem em UTC — converter com `formatDate(...; "DD/MM HH:mm"; "America/Sao_Paulo")`
- [ ] RN-09: log `LOGS` só em `transparent.refunded`/`failed` + Telegram prestador

→ Skipped: `ensureSameTaxId`, `customer.taxId`, `boleto`, `subscriptions`, `payouts` — add quando precisar de CPF travado ou recorrência. Checkout Transparente já cobre 80% dos Pix avulsos.

## 8. Testes

**T-Pix1:** OPORTUNIDADES com `proposta_enviada` e `valor=5000` → SC4a gera `pix_id` + envia WhatsApp com `brCode` (ver no Sheets).
**T-Pix2:** Simule pagamento `POST /transparents/simulate-payment {id: pix_id}` → SC4b atualiza `pix_status=PAID` e `estagio=fechado`.

→ Próximo: auditar blueprint exportado contra este spec antes de ir para produção.
