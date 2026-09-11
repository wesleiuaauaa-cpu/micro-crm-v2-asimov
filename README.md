# Micro-CRM v2 — MVP Make + Sheets + WhatsApp

**Clínica piloto · Mariana / Ouro Preto · Padrão Brasil (PT-BR, America/Sao_Paulo, R$)**

> Promessa (1 frase): *Todo orçamento que chega no seu WhatsApp fica registrado, com alerta de quem não foi respondido em 48h e relatório semanal do que está em aberto.*

Este repositório contém o **projeto completo** — spec congelada, modelo de dados, blueprints Make, payloads de teste, catálogo Asimov e todos os materiais de apoio lidos nesta sessão.

---

## 📁 Estrutura

```
Asimov/
└── PROJETO/
    ├── PROJETO V2..md              # Spec consolidada v1.0 (fonte única de build)
    ├── meio de pagamento que iremos implantar..txt
    ├── specs/                       # Specs ponytail (prontas para vibecoding)
    │   ├── 001-sheets-modelo.md     # 7 abas + 7 CSVs (5 linhas fake clínica)
    │   │   └── csvs/ CLIENTES.csv, OPORTUNIDADES.csv, INTERACOES.csv, AGENDAMENTOS.csv, CONFIG.csv, LOGS.csv, FATURAMENTO.csv
    │   ├── 002-sc2-digest.md        # SC2: Schedule 08:00 + Router domingo
    │   ├── 003-sc3-calendar.md      # SC3: Watch AGENDAMENTOS → Calendar
    │   ├── 004-sc1-webhook.md       # SC1: Webhook WAHA/Z-API → Sheets (com debounce Data Store)
    │   └── 005-payloads-checklist.md# curl T1-T3 + checklist RN-01..17
    └── MATERIAIS DE SUPORTE/        # Tudo que foi lido para criar o MVP
        ├── CATALOGO_FLUXOS_ATENDIMENTO_COMPLETO.md  # 8 fluxos do simples ao sofisticado, prompts, mindmaps
        ├── RESUMO_80_20.md          # 1h15 focado dos 5h02
        ├── RELATORIO_MATERIAIS.md   # Inventário de utilidade/cases
        ├── INVENTARIO_MATERIAIS.md  # Prova aula a aula de Baixar materiais
        ├── micro-crm-v2-briefing.md # Briefing original v2
        ├── tabelas/  ASIMOV_TABELA_COMPLETA.csv (105 cursos), asimov_cursos.csv
        ├── curso/    6 cursos na ordem recomendada (01-06, 55 aulas, 2 apostilas 14.3 MB)
        └── projetos/ 9 projetos de agentes/funil (workflows JSON 66 nodes, zips, Prompts)
```

---

## 🚀 Stack Congelada (não reabrir)

| Camada | Ferramenta | Custo piloto |
|---|---|---|
| Orquestração | **Make.com** Free (1.000 ops, 2 cenários) → Core US$12 | R$0 → rateio |
| Banco | **Google Sheets** (conta do lojista) | R$0 |
| WhatsApp padrão | **WAHA** (self-hosted) com fallback **Z-API** R$59,90 | Manual payload |
| WhatsApp premium | Cloud API Meta (fase 2) | Repasse |
| Agenda | Google Calendar | R$0 |
| Notificação | Telegram | R$0 |

Decisões: WAHA como piloto (você confirmou), pagamento manual no MVP, LLM opcional pago pelo cliente, testes nas suas contas, clínica como piloto.

---

## 🏗️ Como usar (vibecoding)

1. **M0 (2h):** Importe `specs/csvs/*.csv` em `MC-<slug>-DB` (Sheets do lojista) + cole fórmulas `=SUMIFS`/`=SE`.
2. **M1 (3h):** Monte SC2 no Make a partir de `002-sc2-digest.md` (1 cenário, Router domingo).
3. **M2 (1h):** Monte SC3 a partir de `003-sc3-calendar.md`.
4. **M3 (4h):** Monte SC1 a partir de `004-sc1-webhook.md` — capture payload real WAHA antes de mapear, use adapter Z-API se precisar.
5. **M4 (4h):** Replicação: duplique Sheets + importe blueprints em nova pasta `MC-<slug>` (runbook no `PROJETO V2..md:12`).

> **Honestidade técnica:** blueprint JSON é rascunho — monte visualmente na UI do Make (10-20 min/cenário) e audite contra `RN-01..17` em `005-payloads-checklist.md`.

### Testes (T1-T10)
```bash
# T1 cliente novo
curl -X POST "https://hook.make.com/wa-mc-clinica" \
  -d '{"telefone":"5531999990001","texto":"quanto custa limpeza?","fromMe":false,"eh_grupo":false,"msg_id":"TEST-001"}'
# T2 janela 24h, T3 fromMe=true → ver 005-payloads-checklist.md
```

---

## 📚 Materiais de Suporte — O que aprendemos

- **105 cursos** catalogados (tabela completa) + **9 projetos** de agentes/funil baixados e lidos (apostilas 14.3 MB, workflow 66 nodes, prompts).
- **Denominador comum:** `Webhook → Normaliza → Debounce (Redis/Data Store + Wait) → Memória Postgres → Agent (prompt+tools) → Persiste → Responde`.
- **Prompts catalogados:** FAQ, Agendamento Cal.com (5 tools), Agente Oficial (3 prompts), Funil clone voz, Otimizador LPs.
- **Bias prático aplicado:** debounce via `Data Store` (Make nativo) em vez de Redis externo (ponytail: 1 módulo HTTP economizado).

Ver `CATALOGO_FLUXOS_ATENDIMENTO_COMPLETO.md` para fichas do simples ao sofisticado + gaps.

---

## 💰 Planos

| Plano | Cenários | Mensalidade | Custo ferramentas |
|---|---|---|---|
| Base | SC2 | R$199-299 | R$0-25 |
| Mensageiro | SC1+SC2+SC3 | R$399-499 | ~R$60-110 (WAHA/Z-API + rateio) |
| Oficial | fase 2 | R$699-899 + repasse Meta | + consumo |

Manutenção embutida: monitoramento, religamento QR, 30 min/mês ajustes.

---

## 📄 Licença

Uso interno — replicável por cliente via runbook. Credenciais nunca no Sheets (RN-17).

---

*Gerado em 11/09/2026 com Playwright MCP + ponytail (lazy, minimal). Credenciais você cria quando precisar.*
