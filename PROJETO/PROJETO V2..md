# MICRO-CRM v2 — ESPECIFICAÇÃO CONSOLIDADA DO MVP (documento de build)

**v1.0 · 11/09/2026 · destino: IA construtora (vibecoding) + humano executor**
Este documento substitui o briefing como fonte única. Tudo que estava decidido está congelado aqui; tudo que faltava detalhar está especificado abaixo.

---

## 0. Decisões congeladas (não reabrir)

1. **Orquestração:** Make.com (cloud). Sem VPS, sem Docker, sem servidor próprio.
2. **Banco:** Google Sheets, 1 planilha por cliente, **na conta Google do lojista**.
3. **WhatsApp padrão:** API não-oficial gerenciada (Z-API ou Green API) via módulos genéricos (Webhook + HTTP).
4. **WhatsApp premium:** Cloud API oficial da Meta — fase 2, por conta e risco do cliente (módulo nativo Make).
5. **Multi-tenant:** 1 conta Make do prestador, pastas/conexões isoladas por cliente.
6. **Manutenção embutida na mensalidade** (monitoramento, religamento QR, correções, 30 min/mês de ajustes).
7. ⚠️ Pendências externas (não bloqueiam o build): provedor não-oficial do piloto (Z-API vs Green API), gateway fase 2, LLM opcional, câmbio de cobrança.

---

## 1. Como usar este documento no vibecoding

**Divisão de trabalho:**

| A IA construtora gera | O humano executa |
|---|---|
| CSVs das abas com headers e validações | Criar a planilha e importar os CSVs |
| Fórmulas do Sheets | Colar as fórmulas |
| Rascunho de blueprint JSON de cada cenário | Montar/ajustar visualmente no Make (10–20 min/cenário) |
| Payloads de teste (curl) para simular webhook | Disparar os testes |
| Textos das mensagens-modelo | Aprovar e colar no CONFIG |
| Checklist de auditoria contra as RN-xx | Conferir módulo a módulo |

**Honestidade técnica:** blueprint JSON do Make gerado por IA é **rascunho** — o formato interno do Make muda entre versões e nenhum módulo nativo (Sheets, Calendar, Telegram) é 100% recriável fora da UI. O fluxo correto é: IA gera estrutura → humano monta na interface → IA audita contra as regras da seção 6.

**Ordem de construção (milestones):**

| Milestone | Entrega | Tempo alvo | Precisa de |
|---|---|---|---|
| M0 | Template do Sheets (abas, validações, fórmulas, 5 linhas fake) | 2h | — |
| M1 | SC2 rodando: digest diário + relatório de domingo chegando no Telegram | 3h | M0 |
| M2 | SC3 rodando: linha em AGENDAMENTOS → evento no Calendar | 1h | M0 |
| M3 | SC1 ponta a ponta: WhatsApp → registro → auto-resposta → alerta | 4h | M0 + conta no provedor WA |
| M4 | Replicação: runbook testado num 2º Sheets limpo, meio dia | 4h | M1–M3 |

---

## 2. Escopo do MVP

**Promessa (1 frase):** "Todo orçamento que chega no seu WhatsApp fica registrado, com alerta de quem não foi respondido em 48h e relatório semanal do que está em aberto."

**Gating por plano:**

| Plano | SC1 (lead WA) | SC2 (digest+relatório) | SC3 (agenda) | Cenários ativos Make |
|---|---|---|---|---|
| Base | ❌ | ✅ | opcional/manual | 1 (só SC2) |
| Mensageiro | ✅ | ✅ | ✅ | 2–3 (SC3 liga no Core) |
| Oficial | fase 2 | ✅ | ✅ | — |

**Nota de tier Free:** o free (1.000 ops, 2 cenários) cobre o piloto Base (só SC2) e **também** o 1º cliente Mensageiro (SC1+SC2 = 2 cenários) se volume ≤ ~70 msgs/mês. SC3 entra quando houver Core. Gatilho de webhook é instantâneo mesmo no Free; só polling (SC3) fica limitado a 15 min.

**Fora do escopo do MVP:** cobrança automática, estoque, fiscal, disparo em massa, agente autônomo/negociação por IA, comando `/mover` (a evolução de estágio é **por edição direta na planilha** — RN-15).

---

## 3. Arquitetura

```text
 [WhatsApp do cliente final]
        │ (mensagem recebida)
        ▼
 [Provedor WA não-oficial] ──webhook POST──▶ [Make SC1]
        ▲                                          │
        │ HTTP send (auto-resposta)                ▼
        └────────────────────────────  [Google Sheets — conta do lojista]
                                             ▲        │
                          [Make SC2 08:00] ──┘        ▼ (nova linha)
                          digest/relatório ──▶ Telegram do lojista
                                             ▲
                          [Make SC3] ────────┘ (watch)
                                │
                                ▼
                        [Google Calendar do lojista]
```

**Convenções multi-tenant** (nomear sempre assim):

- Pasta Sheets: `MC-<slug>` · Planilha: `MC-<slug>-DB`
- Pasta Make: `MC-<slug>` · Conexões: `google-<slug>`, `tg-<slug>` · Instância WA: `wa-<slug>`
- Nenhuma conexão ou planilha compartilhada entre clientes (RN-11).

---

## 4. Modelo de dados (Sheets)

**Convenções gerais:** datas = data real do Sheets (não texto), fuso `America/Sao_Paulo`; telefone_norm = só dígitos com código do país; IDs gerados pelo Make no padrão `PREFIXO-YYYYMMDDHHmmss` (ex.: `OPP-20260911083122`).

**CLIENTES**

| Coluna | Tipo | Regra |
|---|---|---|
| id | texto | `CLI-...` gerado no SC1 |
| nome | texto | default = "Sem nome " + 4 últimos dígitos até o lojista preencher |
| telefone | texto | como veio do provedor |
| telefone_norm | texto | dígitos, chave de busca (RN-01) |
| origem | lista | whatsapp · indicação · presencial · outro |
| status_relacionamento | lista | lead · ativo · inativo |
| observacoes | texto | livre |
| criado_em / ultima_interacao / ultima_auto_resposta | data-hora | escritos pelo Make |

**OPORTUNIDADES**

| Coluna | Tipo | Regra |
|---|---|---|
| id | texto | `OPP-...` |
| cliente_id | texto | FK → CLIENTES |
| descricao | texto | "piso laminado 60m²" etc. |
| valor | moeda | R$ |
| estagio | **lista (validação)** | novo · em_analise · proposta_enviada · aguardando · fechado · perdido |
| origem | lista | idem CLIENTES |
| proximo_contato | **data** | default = criado_em + `dias_followup` (RN-04) |
| responsavel | texto | nome do lojista |
| perdida_motivo | lista | preço · prazo · sem retorno · outro (exigido se perdido — ver T5) |
| criado_em / fechado_em | data | |

**INTERACOES**: `id (INT-...)` · `cliente_id` · `oportunidade_id` · `canal (whatsapp|telefone|presencial|email)` · `direcao (recebida|enviada)` · `resumo` · `msg_id` · `data`

**AGENDAMENTOS**: `id` · `cliente_id` · `titulo` · `data_hora` · `status (agendado|confirmado|realizado|cancelado|no_show|pendente_sync)` · `calendar_event_id` · `criado_em`

**CONFIG**: `chave | valor` (tabela completa na seção 5)

**LOGS**: `ts | cenario | severidade | resumo | payload_trunc` (payload truncado a 500 caracteres)

**FATURAMENTO**: `mes | cliente | plano | valor_cobrado | custo_ferramentas | margem | pago_em | obs` — fórmula da margem: `=D2-E2`

**Fórmulas de leitura humana** (não consomem ops; o Make lê as linhas, não estas células):

```text
Pipeline aberto (célula solta em OPORTUNIDADES):
=SUMIFS(D:D; E:E; "<>fechado"; E:E; "<>perdido")
Atraso em dias (coluna auxiliar aux_atraso em OPORTUNIDADES):
=SE(E2="";""; SE(OU(E2="fechado";E2="perdido");""; HOJE()-G2))
```

---

## 5. Parâmetros CONFIG (com defaults)

| chave | default | usado por |
|---|---|---|
| plano | base | gating de cenários |
| nome_negocio | (nome do lojista) | mensagens |
| horario_atendimento | "seg–sex 8h–18h" | auto-resposta |
| fuso | America/Sao_Paulo | todos os schedules |
| telegram_chat_id_lojista | — | SC2, SC1 |
| telegram_chat_id_prestador | — | erros e sessão caída |
| auto_resposta_ativa | SIM (Mensageiro) / NAO (Base) | SC1 |
| texto_auto_resposta | template seção 9 | SC1 |
| janela_auto_resposta_h | 24 | RN-05 |
| dias_followup | 2 | RN-04 |
| dia_relatorio | domingo | SC2 branch semanal |
| hora_digest | 08:00 | SC2 |

**RN-17 (segurança):** nenhum token/segredo vai na planilha. Credenciais de WA, Telegram e Google vivem apenas nas conexões dos módulos Make. Quem tem acesso ao Sheets não herda credenciais.

---

## 6. Regras de negócio (o coração do build)

- **RN-01 — Normalização e match de telefone:** `telefone_norm` = só dígitos. Se o payload vier com 10–11 dígitos sem "55", prefixar 55. Match: (a) exato em `CLIENTES.telefone_norm`; (b) fallback = sufixo de 8 dígitos; (c) sem match = cliente novo.
- **RN-02 — Só mensagem recebida é lead:** `fromMe=true` (mensagem do próprio lojista) e mensagens de **grupo** não criam nada (path C do SC1: zero módulos). Dedupe por `msg_id` re-enviado pelo provedor: não implementar no MVP; registrar no LOGS se ocorrer (trade-off consciente para economizar 1 op/msg).
- **RN-03 — Criação em cadeia:** cliente novo ⇒ 1 linha em CLIENTES + 1 em INTERACOES (direcao=recebida) + 1 em OPORTUNIDADES (`estagio=novo`, `proximo_contato = hoje + dias_followup`).
- **RN-04 — Follow-up 48h:** aparece no digest toda oportunidade com `estagio ∈ {novo, em_analise, proposta_enviada}` **e** `proximo_contato ≤ hoje`. Ao registrar interação ou mudar estágio, o lojista atualiza `proximo_contato` na planilha (a interação nova em INTERACOES com data de hoje também "esfria" o alerta via fórmula).
- **RN-05 — Auto-resposta controlada:** enviar só se `auto_resposta_ativa=SIM` **e** agora − `ultima_auto_resposta` do cliente > `janela_auto_resposta_h`. Objetivo: nunca parecer robô conversando com o lojista em tempo real.
- **RN-06 — Horários:** digest diário 08:00 (seg–sáb); relatório domingo (mesma execução, branch própria); fuso do CONFIG.
- **RN-07 — Estágios terminais:** `fechado` e `perdido` saem de todos os alertas; `perdido` sem `perdida_motivo` gera linha de aviso no digest.
- **RN-08 — Agendamento:** nova linha em AGENDAMENTOS com `status=agendado` e `calendar_event_id` vazio ⇒ SC3 cria evento e grava o id. Falha ⇒ `status=pendente_sync` (reprocesso no digest seguinte). SLA: ≤15 min (limite do polling free).
- **RN-09 — Logging econômico:** erro sempre grava LOGS + Telegram ao prestador; sucesso não grava (exceto auto-respostas enviadas, para auditoria). Router e filtro não consomem ops; cada módulo executado consome 1.
- **RN-10 — Cenário físico único SC2:** digest diário e relatório semanal são **um só cenário** com router por dia da semana (economiza cenário no tier free).
- **RN-11 — Isolamento:** ver seção 3; proibido reaproveitar conexão OAuth entre clientes.
- **RN-12 — LGPD:** dados na planilha do lojista (controlador); prestador = operador; Make processa em trânsito; retenção de logs Make ~30 dias; exclusão a pedido = encerrar integração + apagar abas + revogar conexões.
- **RN-13 — Datas:** todas em data real no fuso do CONFIG; `proximo_contato` é date (não datetime) para filtro simples.
- **RN-14 — Múltiplas oportunidades por cliente:** permitidas; o digest agrupa por cliente.
- **RN-15 — Mudança de estágio:** somente por edição na planilha no MVP (comando `/mover` é backlog).
- **RN-16 — Filtro de domingo no Make:** branch semanal com condição `formatDate(agora; "dddd") = "Sunday"` (Make gera nomes em inglês por padrão — validar na montagem).

---

## 7. Especificação dos cenários (módulo a módulo)

### SC1 — Entrada de lead por WhatsApp (plano Mensageiro)

**Trigger:** Webhooks → Custom webhook (instantâneo, não consome agenda de 15 min).

| # | Módulo | Config resumida | Ops |
|---|---|---|---|
| 1 | Webhook | capturar 1 payload real de amostra antes de mapear (seção 8) | 1 |
| 2 | Sheets: Search CLIENTES | filtro `telefone_norm = {{normalizado}}` | 1 |
| 3 | Router | — (não conta) | 0 |

**Router:**

- **Path A — cliente novo** (sem match, `fromMe=false`, não grupo):
  A1 Sheets Add CLIENTES (id, nome default, telefone_norm, criado_em, ultima_interacao, ultima_auto_resposta=agora se responder) · A2 Sheets Add OPORTUNIDADES (`novo`, proximo_contato=hoje+2) · A3 Sheets Add INTERACOES · A4 HTTP send-text (filtro: auto_resposta_ativa) · A5 Telegram → lojista. **Total 6 ops.**
- **Path B — cliente existente** (match, `fromMe=false`):
  B1 Sheets Update CLIENTES (ultima_interacao; ultima_auto_resposta com valor condicional `{{if(janela_ok; agora; valor_atual)}}`) · B2 Sheets Add INTERACOES · B3 HTTP auto-resposta (filtro janela) · B4 Telegram. **Total 5 ops.**
- **Path C — `fromMe=true` ou grupo:** nenhum módulo. **1 op** (só o webhook já consumido).

**Error handler (todos os paths):** incomplete execution + módulo Sheets Add LOGS + Telegram ao prestador. Retry nativo 3x no HTTP.

### SC2 — Digest diário + relatório semanal (todos os planos)

**Trigger:** Schedule diário 08:00 (fuso CONFIG).

| # | Módulo | Ops |
|---|---|---|
| 1 | Schedule | 1 |
| 2 | Sheets Search OPORTUNIDADES (`estagio ∈ {novo,em_analise,proposta_enviada}` **e** `proximo_contato ≤ hoje`) | 1 |
| 3 | Router: branch domingo (RN-16) / default | 0 |

- **Branch default (digest):** Text Aggregator (agrupa atrasadas em 1 mensagem: cliente, descrição, dias sem retorno, valor) → Telegram lojista. Custo: N atrasadas × ~1 + envio ≈ **4–8 ops/dia**.
- **Branch domingo (relatório):** + Search fechadas na semana (1) + Search agenda da próxima semana (1) + Gmail/Telegram com o template da seção 9. ≈ **8–10 ops/domingo**.

### SC3 — Agendamento → Calendar (Mensageiro; entra no Core)

**Trigger:** Sheets Watch New Rows em AGENDAMENTOS (polling 15 min).

1. Watch (1) → 2. Filtro `status=agendado` e `calendar_event_id` vazio → 3. Google Calendar Create Event (1) → 4. Sheets Update Row (`calendar_event_id`, `status=confirmado`) (1). **3 ops/evento.**
**Erro no Calendar:** handler grava `pendente_sync` + LOGS; SC2 do dia seguinte lista pendentes.

### Orçamento de ops por plano

| Plano | Cenários | Estimativa/mês | Folga no Free (1.000) |
|---|---|---|---|
| Base | SC2 | ~190 | ampla |
| Mensageiro (100 msgs, 20 eventos) | SC1+SC2+SC3 | ~850 | ok até ~70 msgs no free; Core no 2º cliente |

Regra operacional: **alerta quando o painel do Make bater 80% da cota** (monitoramento faz parte da manutenção embutida).

---

## 8. Contratos de integração

**Entrada (webhook do provedor) — contrato normalizado que o SC1 espera:**

```json
{ "telefone": "5531999990000", "texto": "vocês têm X? quanto custa?",
  "fromMe": false, "eh_grupo": false, "msg_id": "ABC123" }
```

⚠️ **Regra de build:** conectar o webhook real, mandar 1 mensagem de teste, **capturar o payload de amostra** e só então mapear os campos para este contrato. Não codificar antes da amostra (payload varia por versão do provedor).

**Saída (adapter por provedor) — confirmar doc oficial antes do M3 ⚠️:**

| Provedor | Endpoint envio texto | Auth |
|---|---|---|
| Z-API | POST `/instances/{id}/token/{tk}/send-text` body `{phone, message}` | header `Client-Token` |
| Green API | POST `/waInstance{id}/sendMessage/{tk}` body `{chatId: "<fone>@c.us", message}` | token na URL |

**Telegram:** POST `https://api.telegram.org/bot{token}/sendMessage` body `{chat_id, text}`. **Calendar:** módulo nativo Google Calendar "Create an Event". **Gmail:** módulo nativo.

---

## 9. Mensagens-modelo (variáveis entre chaves)

```text
AUTO_RESPOSTA:
"Olá! Recebemos sua mensagem e já registramos seu pedido. A {nome_negocio}
responde por aqui em até algumas horas ({horario_atendimento}). ✅"

DIGEST DIÁRIO (Telegram → lojista):
"📌 Follow-ups de hoje ({data}) — {N} em atraso:
{N}. {cliente} — {descricao} · sem retorno há {dias_atraso}d · {valor}
→ responda pelo seu WhatsApp e atualize a coluna 'proximo_contato'."

RELATÓRIO SEMANAL:
"📊 Semana {dd/aa} — {nome_negocio}
Novos orçamentos: {n} · Em aberto: R$ {pipeline_aberto}
Ganhos: R$ {ganho_semana} ({qtd}) · Perdidos: {qtd_perdidas}
⚠️ Sem retorno >48h: {n_atraso} · Agenda próxima semana: {n_agenda}
💡 Valor recuperado (novo→proposta nesta semana): R$ {x}"
```

A linha final do relatório é a **prova de valor** que sustenta a mensalidade: sempre numérica, sempre semanal.

---

## 10. Erros e contingências (resumo operacional)

| Falha | Ação automática | Ação humana |
|---|---|---|
| Sessão WA cai | provedor sinaliza / webhook silencioso → Telegram prestador | religar QR ≤15 min; celular do lojista nunca para de receber |
| Ban do número | — | plano de contingência contratual: novo número ≤24h ou upgrade ao Oficial com abatimento |
| Sheets indisponível | retry 3x → suspende + LOGS | reprocesso manual via LOGS |
| Calendar falha | `pendente_sync` | reprocesso no digest seguinte |
| Token Google expira | e-mail Make | reautorizar (~2 min) |
| Webhook perdido | — | lançamento manual na planilha |

---

## 11. Critérios de aceitação (executar na ordem)

| # | Teste | Resultado esperado |
|---|---|---|
| T1 | Msg de número novo via curl no webhook | 3 linhas criadas + auto-resposta + Telegram; ≤7 ops |
| T2 | 2ª msg do mesmo número em 10 min | registra interação, **sem** 2ª auto-resposta |
| T3 | Msg com fromMe=true | nenhuma linha criada |
| T4 | Oportunidade com proximo_contato ontem / amanhã | aparece / não aparece no digest |
| T5 | Estágio "perdido" sem motivo | aviso no digest |
| T6 | Nova linha em AGENDAMENTOS | evento ≤15 min com calendar_event_id gravado |
| T7 | HTTP de envio apontando para URL inválida | retry 3x → LOGS + Telegram prestador |
| T8 | Domingo 18h–08h | relatório com números conferidos manualmente contra a planilha |
| T9 | 2ª execução do digest no mesmo dia com nada novo | mensagem "0 em atraso" (nunca silêncio) |
| T10 | Replicação M4 num Sheets virgem | runbook funciona sem consultar memória, meio dia |

---

## 12. Runbook de replicação por cliente (meio dia)

1. Duplicar template-mestre do Sheets → renomear `MC-<slug>-DB` (30 min)
2. Importar blueprints SC1–SC3 na pasta `MC-<slug>` do Make (20 min)
3. Conectar OAuth Google do lojista nas conexões renomeadas (10 min)
4. Criar conexão Telegram do lojista e capturar `chat_id` (10 min)
5. Criar instância no provedor WA + conectar número dedicado via QR (20 min)
6. Apontar webhook do provedor ao URL do SC1; capturar payload de amostra e mapear (30 min)
7. Preencher CONFIG do cliente (15 min)
8. Rodar T1–T6 com dados fictícios (30 min)
9. Treinar o lojista (30 min): ler digest, atualizar planilha, religar QR básico
10. Assinar termo de ciência (não-oficial) + definir plano na aba FATURAMENTO (15 min)

---

## 13. Backlog pós-MVP (não construir agora)

1. Comando `/mover <id> <estagio>` por WhatsApp (parser no SC1)
2. Dedupe por `msg_id`
3. Plano Oficial (módulo nativo Make + Cloud API + termo de repasse 20%)
4. Gateway de cobrança (Asaas vs Mercado Pago ⚠️) e conciliação automática na FATURAMENTO
5. LLM de classificação/resumo de mensagens (nunca negociação autônoma)
6. Dash de health score: uso da planilha como proxy de engajamento (planilha parada 2 semanas = cliente em risco de churn → proativo)

---

## 14. Prompts prontos para a IA construtora (nesta ordem)

1. **P1 (M0):** "Gere o conteúdo CSV das 7 abas da seção 4, com validação de dados nas colunas marcadas como lista, e as fórmulas auxiliares prontas para colar."
2. **P2 (M1):** "Gere o blueprint JSON do cenário SC2 conforme seção 7, com schedule 08:00 America/Sao_Paulo, router com filtro de domingo e aggregator no digest. Aponte inconsistências contra RN-04, RN-06, RN-09, RN-10, RN-16."
3. **P3 (M2):** idem para SC3, auditando RN-08.
4. **P4 (M3):** "Gere os payloads curl para testar T1–T3 dado este contrato de webhook (colar amostra real aqui), e o esqueleto do blueprint SC1 com os 3 paths do router."
5. **P5 (auditoria):** "Audite este blueprint exportado do Make contra as RN-01 a RN-17 e liste desvios."
6. **P6 (M4):** "Gere o manual do lojista em 1 página a partir das seções 9 e 12: o que o sistema faz, o que é dele fazer, o que fazer se o WhatsApp cair."

---

**Próximo passo:** rodar P1 e P2 hoje; M0+M1 fecham o protótipo do Dia 4 do plano de 7 dias — ainda **sem WhatsApp**, que só entra (M3) depois de uma empresa dizer "eu pagaria por isso".