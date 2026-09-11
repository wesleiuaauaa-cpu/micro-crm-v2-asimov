# MICRO-CRM v2 — BRIEFING ÚNICO PARA IA CONSTRUTORA
### Reescrita completa: Make no lugar do Agno · sem VPS · WhatsApp não-oficial como padrão · oficial como opção premium · manutenção embutida na mensalidade
Data: 11/09/2026

---

## 0. MUDANÇAS v1 → v2

| Item | v1 (descartada) | v2 (esta spec) |
|---|---|---|
| Orquestrador | Agno (framework Python) | **Make.com** (cloud, sem servidor) |
| WhatsApp | WAHA self-hosted (Docker/VPS) | **API não-oficial gerenciada** (Z-API/Green API — sem VPS) + opção oficial Meta |
| Infra | PC do lojista ou VPS própria | **Nenhuma.** 100% cloud (Sheets + Calendar + Make) |
| Custo fixo de infra | VPS ~R$ 99+/mês | **R$ 0 no piloto; US$ 12/mês a partir do 2º cliente** |
| Manutenção | Não precificada | **Embutida na mensalidade** (monitoramento + correções + ajustes limitados) |
| Multi-tenant | Instalação local 1 a 1 | Conta Make única com pastas/conexões isoladas por cliente |

Motivo da troca do WAHA: WAHA exige servidor próprio (Docker — "run one command in the terminal **on your own server**", waha.devlike.pro), o que viola a restrição "sem VPS". O risco de ban de APIs não oficiais está documentado (github.com/devlikeapro/waha/issues/1362; asksuite.com/blog/unofficial-whatsapp-api-hotels-risks) — tratado na seção 7.

---

## 1. STACK (não negociável)

| Camada | Ferramenta | Custo verificado (set/2026) | Papel |
|---|---|---|---|
| Protótipo visual | Google Stitch | Free (~350 gerações/mês, uxpilot.ai) | Gerar telas/fluxo; não é runtime |
| Banco de dados | Google Sheets | R$ 0 (conta do lojista) | Abas modeladas (seção 3) |
| Orquestração | **Make.com** | **Free: 1.000 ops/mês, 2 cenários ativos, intervalo mínimo 15 min · Core: US$ 12/mês (anual), 10.000 ops, cenários ilimitados** (make.com/en/pricing) | Todos os fluxos |
| Mensageria padrão | **API não-oficial gerenciada** (Z-API ou Green API) | Mercado gerenciado: **R$ 29–99,90/instância/mês** (Wafly R$ 59,90 — wafly.com.br); Green API Business ~US$ 24/mês (green-api.com) ⚠️ plano exato a confirmar no site | Enviar/receber WA sem VPS |
| Mensageria premium | **WhatsApp Cloud API oficial (Meta)** | Conversas iniciadas pelo cliente: **grátis**; utility ~US$ 0,0068–0,0080/msg; marketing US$ 0,0625 (Brasil); revisões de preço 01/08 e 01/10/2026 (developers.facebook.com; blueticks.co; ominiflow.com) | Opção "por conta e risco do cliente" |
| Agenda | Google Calendar | R$ 0 | Agendamentos e lembretes |
| Notificação interna | Telegram / Gmail | R$ 0 | Alertas ao lojista e ao prestador |
| IA (opcional) | LLM via API (chave própria) | ⚠️ a confirmar modelo/provedor | Só classificação/resumo — nunca negociação autônoma |
| Pagamentos | Pix manual (v0) → gateway (Asaas/Mercado Pago) na fase 2 | ⚠️ taxas a confirmar | Conciliação na aba FATURAMENTO |

**Ponto técnico crítico:** o Make **não possui módulo nativo para APIs não oficiais** (WAHA/Evolution/Z-API). A integração é feita com módulos genéricos **Webhooks (Custom mail hook / webhook)** de entrada + **HTTP "Make a request"** de saída. Já o WhatsApp **oficial** tem módulo nativo no Make. Isso reduz o custo de ops (módulos genéricos contam igual) mas exige mapeamento manual de payload — ver seção 4.

**Verificação "existe alternativa melhor ao Make sem VPS?" — não, nesta faixa de tamanho o Make fica:**

| Orquestrador | Free | Pago de entrada | Veredicto |
|---|---|---|---|
| **Make** | 1.000 ops, 2 cenários | US$ 12 → 10.000 ops, cenários ilimitados | **Escolhido**: melhor razão ops/preço + módulo nativo WA oficial |
| Activepieces | 1.000 tarefas | desde US$ 16 | Empata no free; sem vantagem paga |
| n8n Cloud | não tem free | € 20–24/mês → 2.500 execuções | Mais caro por execução — descartado sem VPS |
| Zapier | 100 tarefas | US$ 19,99+ | Inviável no free para CRM |

---

## 2. PÚBLICO E USO (resumo operacional)

- **Cliente pagante:** empresas locais B2B que vivem de orçamento (manutenção, locação, transporte, fornecimento p/ obra e mineração) — Mariana, Ouro Preto e região; BH remoto.
- **Cliente final do lojista:** quem manda mensagem pedindo preço/prazo/agendamento.
- **Casos de uso do MVP:** (1) registro de lead/orçamento; (2) follow-up com alerta; (3) agendamento; (4) relatório semanal. Fora do MVP: cobrança automática, estoque, fiscal, disparo em massa, agente autônomo.

---

## 3. MODELAGEM DO SHEETS (banco)

```text
CLIENTES:      id | nome | telefone | origem | status_relacionamento | observacoes | criado_em | ultima_interacao
OPORTUNIDADES: id | cliente_id | descricao | valor | estagio(novo/em_analise/proposta_enviada/aguardando/fechado/perdido) |
               origem | proximo_contato | responsavel | perdida_motivo | criado_em | fechado_em
INTERACOES:    id | cliente_id | oportunidade_id | canal | direcao | resumo | data
AGENDAMENTOS:  id | cliente_id | titulo | data_hora | status(confirmado/realizado/cancelado/no_show) | calendar_event_id
CONFIG:        chave | valor   (nome do negócio, horário de atendimento, plano, telefone do bot, Flags)
LOGS:          ts | cenario | status | resumo_payload | erro
FATURAMENTO:   mes | cliente | plano | valor_cobrado | custo_ferramentas | pago_em
```

Índice prático: coluna auxiliar `telefone_norm` (só dígitos) em CLIENTES e INTERACOES para busca exata; `proximo_contato` formatado como data real (usado pelo alerta).

---

## 4. CENÁRIOS DO MAKE + ORÇAMENTO DE OPERAÇÕES

**Regra do Make: cada módulo executado consome 1 op; router e filtro não contam.** Com 1.000 ops free, o desenho precisa ser "event-driven, não polling".

| # | Cenário | Gatilho | Módulos (ops por rodada) | Uso |
|---|---|---|---|---|
| S1 | Entrada de lead | Webhook da API não-oficial (instantâneo) | Webhook(1) + Sheets-Search(1) + Sheets-Add/Update(1) + Router + HTTP-reply(1) + Telegram lojista(1) ≈ **5–6 ops/msg** | Só plano Mensageiro |
| S2 | Digest diário + alertas de follow-up | Schedule 1×/dia (8h útil) | Schedule(1) + Sheets-Search atrasados(1) + Iterator(1) + Gmail/Telegram(1) ≈ **4 ops/dia** | Todos os planos |
| S3 | Agendamento | Sheets "nova linha em AGENDAMENTOS" (watch) | Watch(1) + Calendar-Create(1) + confirmação(1) ≈ **3 ops/evento** | Todos |
| S4 | Relatório semanal | Schedule domingo | Schedule(1) + Sheets-Read agregações(2) + Gmail(1) ≈ **4 ops/semana** | Todos |

**Orçamento mensal por cliente (estimativa de projeto):** 100 msgs × 6 + 30 × 4 + 20 eventos × 3 + 4 × 4 ≈ **830 ops/mês**.

- **Free (1.000 ops, 2 cenários ativos):** cobre **1 cliente** no plano Base (S2+S4 combinados em 1 cenário, S3 desligado ou manual). É o piloto.
- **Core (US$ 12, 10.000 ops):** aciona no **2º cliente**; capacidade ≈ 10.000 ÷ 830 ≈ **até ~10–11 clientes** na mesma conta.
- **Ponto de virada:** acima de ~10 clientes, abrir 2ª conta Make ou reavaliar Activepieces/n8n self-host — só acontece depois de R$ 4.000+/mês de receita, portanto não é risco de hoje.

---

## 5. FLUXO-REFERÊNCIA (mensagem de orçamento)

1. Cliente final manda "vocês têm X? quanto custa?" →
2. Webhook da API não-oficial dispara S1 no Make →
3. Make normaliza telefone, busca em CLIENTES →
4. Não existe? cria cliente + INTERACAO + OPORTUNIDADE (estágio `novo`) →
5. Resposta automática padrão do CONFIG ("recebemos, retornamos em até Xh") →
6. Notifica lojista no Telegram →
7. S2 no dia seguinte lista tudo sem retorno > 48h →
8. Lojista responde pelo próprio WhatsApp/celular; sistema só registra →
9. Oportunidade avança por edição na planilha (ou comando `/mover 123 proposta`) →
10. S4 envia resumo semanal (novos, sem retorno, valor em aberto).

---

## 6. FALLBACKS E ERROS

| Falha | Detecção | Ação | Notificação |
|---|---|---|---|
| Sessão WA não-oficial cai | Webhook sem resposta / provedor sinaliza | Religar QR (< 15 min, procedimento do provedor); durante a queda o **celular do lojista continua funcionando normalmente** (a API espelha a sessão) | Telegram ao prestador + aviso ao cliente |
| **Ban do número (não-oficial)** | Número para de enviar/receber | Plano de contingência (seção 7); se irrecuperável: novo número dedicado ou migração ao plano Oficial com desconto proporcional do setup | Imediata |
| Sheets: cota de API/erro de escrita | Handler de erro do Make | Retry nativo; se persistir, suspende cenário e marca pendência na aba LOGS (reprocesso manual) | E-mail + Telegram |
| Calendar falha | Handler de erro | A linha fica em AGENDAMENTOS com `status=pendente_sync`; S2 do dia seguinte reprocessa | No digest |
| Token Google expira (OAuth) | Make notifica conexão quebrada | Reautorizar conexão (~2 min) | E-mail Make |
| Webhook perdido (msg não logada) | Divergência apontada pelo lojista | Lançamento manual na planilha (o celular nunca deixa de receber) | — |

---

## 7. TERMOS DE RISCO, DADOS E LGPD (embutidos no contrato)

**Termo de ciência — via não-oficial (assinatura obrigatória):**
> "O cliente declara ciência de que a integração utilizada não é a API oficial da Meta e que o número conectado pode ser bloqueado a critério do WhatsApp, sem prazo de aviso. Recomenda-se número dedicado ao robô, distinto do número principal do negócio. O prestador religará a sessão em até 24h úteis sem custo e, em caso de bloqueio definitivo, aplicará o plano de contingência ou migrará o cliente ao plano Oficial abatendo parte do setup."

**Termo — via oficial ("por conta e risco do cliente"):**
> "O cliente assume os custos de consumo da Meta por conversa/template (repasse integral + taxa administrativa de 20%), a responsabilidade pela aprovação dos templates e pelas políticas de negócio da Meta, e eventuais mudanças de preço (revisões programadas para 01/08/2026 e 01/10/2026)."

**Plano de contingência de número:** (1) número dedicado ao bot desde o dia 1; (2) contatos vivem no Sheets (backup nativo); (3) religamento QR documentado; (4) se ban: provisionar novo número em < 24h ou upgrade ao plano Oficial.

**Onde ficam os dados:** mensagens e cadastros → Sheets na **conta Google do lojista** (ele é o dono/controlador); Make processa em trânsito, com retenção de logs de execução limitada (config. ~30 dias); sessão WA hospedada no provedor não-oficial escolhido ⚠️ localização dos servidores a confirmar (Z-API é brasileira; Green API — verificar). LGPD: lojista = controlador, prestador = operador; base legal = execução de contrato; sem compartilhamento com terceiros além dos citados; exclusão a pedido = encerrar integração e apagar aba Logs.

---

## 8. DEPLOY REPLICÁVEL (sem VPS — decisão fechada)

**Cenário escolhido: 100% cloud, replicado por blueprint.**

1. Duplicar pasta no Sheets a partir do template-mestre (abas prontas).
2. Importar blueprint dos cenários no Make (exportáveis/importáveis) para a pasta do cliente.
3. Conectar OAuth do Google **do próprio lojista** (a planilha é dele).
4. Criar instância no provedor WA não-oficial e conectar o número dedicado (QR).
5. Preencher aba CONFIG, testar os 4 cenários com dados fictícios.
6. Treinar o lojista (30 min) + termo de risco assinado.

Tempo de replicação-alvo: **meio dia por cliente**. Custo de infra por cliente: R$ 0 (1º) a ~US$ 1,2 rateado (10 clientes no Core).

**Isolamento multi-tenant leve:** 1 conta Make do prestador, pastas por cliente, conexões OAuth nomeadas por cliente, 1 instância WA por cliente, 1 Sheets por cliente. Portabilidade: blueprint exportado guarda a configuração (credenciais ficam no provedor/Google, não no blueprint).

---

## 9. ROADMAP

| Fase | Escopo | Ferramentas | Custo fixo |
|---|---|---|---|
| 0 — Piloto (semana 1–2) | S2+S4, Base, 1 cliente, Pix manual | Make Free | R$ 0 |
| 1 — Venda Mensageiro | S1–S4, WA não-oficial | Make Free/Core + Z-API/Green | ~R$ 60–110/cliente |
| 2 — Escala | Plano Oficial (módulo nativo Make + Cloud API), gateway de cobrança (Asaas/Mercado Pago ⚠️ a confirmar), IA de classificação | + consumo Meta | repasse ao cliente |

---

## 10. PRECIFICAÇÃO (preços de teste — são hipóteses comerciais, não dados de mercado)

| Plano | Setup | Mensalidade | Custo de ferramentas/cliente/mês | Margem mensal bruta |
|---|---:|---:|---:|---:|
| **Base** (organização + follow-up, sem WA integrado) | R$ 600–900 | **R$ 199–299** | R$ 0–25 (rateio Make) | ~80–85% |
| **Mensageiro** (padrão — WA não-oficial) | R$ 900–1.400 | **R$ 399–499** | ~R$ 60–110 (instância não-oficial + rateio Make) | ~75% |
| **Oficial** (premium — conta e risco do cliente) | R$ 1.800–2.500 | **R$ 699–899** + repasse Meta | rateio Make + consumo Meta (service grátis; utility ~US$ 0,0068–0,0080; marketing US$ 0,0625) | ~70% + 20% s/ repasse |

**Manutenção embutida na mensalidade** (o que ela cobre): hospedagem das automações, instância WA, monitoramento de sessão, correções de fluxo, religamento/QR, até 30 min/mês de ajustes (excedente: R$ 80/h), relatório mensal de operação.

**Caminhos para R$ 5.000/mês (meta de 2–4 meses, não de semana 1):**
- 8 clientes Mensageiro (8 × R$ 450 = R$ 3.600) + 1 setup/mês (R$ 1.200) ≈ **R$ 4.800**
- 6 Mensageiro (R$ 2.700) + 2 Oficial (R$ 1.600 s/ repasse) + 1 setup ≈ **R$ 5.500**

**Ponto de virada de custo:** 2º cliente → Make Core (US$ 12); ~10 clientes → 2ª conta/reavaliar plataforma; gateway só quando a cobrança manual doer (>15 clientes).

---

## 11. PLANO DE 7 DIAS (atualizado ao Make)

1. **Dia 1** — listar 30 empresas (15 B2B orçamento / 10 turismo / 5 clínicas-contadores). Nada de construir.
2. **Dia 2** — 5 entrevistas (roteiro fixo: orçamentos/mês, onde chegam, como registram, quantos sem retorno, valor de resolver).
3. **Dia 3** — escolher 1 dor que apareceu em ≥3 empresas.
4. **Dia 4** — protótipo no **Make Free + Sheets**: S2 (digest+alertas) e S4 (relatório), **sem WhatsApp**.
5. **Dia 5** — demo para 5 empresas: "se funcionasse com seus dados, quanto valeria?"
6. **Dia 6** — 2 propostas-piloto (escopo, prazos, exclusões, responsabilidades, custos externos, métrica de sucesso) nas modalidades Base e Mensageiro.
7. **Dia 7** — decisão: seguir só se 3 reconhecerem a dor, 2 quiserem testar, 1 pagar. Se ninguém pagar: revisar dor/nicho/preço — não estudar mais IA.

---

## 12. DECISÕES PENDENTES (⚠️)

1. Provedor não-oficial do piloto: **Z-API** (brasileira) vs **Green API** (~US$ 24/mês) — confirmar plano exato e localização dos dados.
2. Gateway de cobrança da fase 2: Asaas vs Mercado Pago (taxas a confirmar).
3. LLM para classificação (opcional): modelo, provedor e quem paga a chave.
4. Conversão USD→BRL dos preços do Make/Meta: pelo câmbio do dia da cobrança.

## 13. FONTES DE CUSTO (verificadas em 11/09/2026)

- make.com/en/pricing — Free 1.000 credits/15 min interval; Core US$ 12/10k
- zapier.com/blog/make-com-pricing — corrobora tiers Make
- n8n.io/pricing — Starter € 20–24/mês, 2.5k execuções
- activepieces.com/pricing — free 1.000 tarefas; desde US$ 16
- zapier.com/pricing — free 100 tarefas; Pro US$ 19,99+
- wafly.com.br/comparativos/quanto-custa-api-whatsapp — APIs não-oficiais R$ 29–99,90/instância; Wafly R$ 59,90
- green-api.com — Business ~US$ 24/mês; Developer free limitado (3 chats)
- z-api.io — provedor brasileiro (plano exato a confirmar)
- developers.facebook.com/...whatsapp/pricing — revisões 01/08 e 01/10/2026
- blueticks.co / ominiflow.com — Brasil: marketing US$ 0,0625; utility US$ 0,0068–0,0080; auth US$ 0,0315
- sleekflow.io — conversas de serviço iniciadas pelo cliente: gratuitas
- github.com/devlikeapro/waha/issues/1362 + asksuite.com — risco de ban em API não-oficial
- waha.devlike.pro — WAHA exige servidor próprio (motivo da exclusão)
