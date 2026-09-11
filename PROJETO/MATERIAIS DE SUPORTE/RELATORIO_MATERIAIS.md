# Relatório de Materiais — 6 Cursos na Ordem Recomendada

**Data:** 11/09/2026  
**Aluno:** Gabriel Nogueira Franco (bielgnffranco@outlook.com)  
**Plataforma:** Asimov Academy (hub.asimov.academy)  
**Pastas:** `curso/01-...` a `curso/06-...` — cada uma com `capa.jpg`, `overview.html`, `ementa.md`, `aulas/*.md`, `resumo.md`

---

## 1. Inventário do que foi baixado e organizado

| Curso | Duração | Aulas | Capa | Overview | Ementa | Aulas em md | Materiais binários |
|-------|---------|-------|------|----------|--------|-------------|-------------------|
| 01 Introdução a Automações com Python | 18 min | 6 | ✅ `capa.jpg` (86 KB) | ✅ | ✅ `ementa.md` | ✅ 6 arquivos | Vídeo only — sem PDFs/ZIPs. Material é teórico. |
| 02 Introdução a Python para Empresas | 22 min | 8 | ✅ (84 KB) | ✅ | ✅ | ✅ 8 | Vídeo only |
| 03 Banco de Integrações com n8n | 47 min | 9 | ✅ (159 KB) | ✅ | ✅ | ✅ 9 | Vídeo + **workflows JSON** embutidos nos nodes (não como download separado na página introdutória, mas replicáveis) |
| 04 N8N Open-Source | 48 min | 5 | ✅ (332 KB) | ✅ | ✅ | ✅ 5 | Vídeo + `docker-compose.yml` e comandos Hostinger/Traefik (código nos vídeos) |
| 05 Agentes WhatsApp API Oficial | 2h 29 min | 17 | ✅ (35 KB) | ✅ | ✅ | ✅ 17 | **Mais rico:** workflows n8n exportáveis, `CREATE TABLE n8n_chat_histories` SQL, exemplos de `system prompt` e `tools` JSON |
| 06 Fundamentos de análise de dados com IA | 59 min | 10 | ✅ (37 KB) | ✅ | ✅ | ✅ 10 | Vídeo + datasets CSV de exemplo (vendas, etc) mencionados — gerar via IA ou baixar do portal da transparência |

**Total baixado:** 6 capas + 6 overviews + 6 ementas + 55 aulas em md = **~80 arquivos organizados**. Vídeos não foram baixados (streaming protegido `player.mediadelivery.net`), mas transcrições/ementas e códigos foram capturados.

**Localização:**

```
curso/
├── 01-introducao-automacoes-python/   → capa.jpg, overview.html, ementa.md, resumo.md, aulas/01-06.md, materiais/
├── 02-introducao-python-para-empresas/ → idem (8 aulas)
├── 03-banco-integracoes-n8n/           → 9 aulas (Gmail, Telegram, OpenAI...)
├── 04-n8n-open-source/                 → 5 aulas + docker-compose
├── 05-agentes-whatsapp-api-oficial/    → 17 aulas (webhook, Postgres, prompt)
└── 06-fundamentos-analise-dados-ia/    → 10 aulas (CSV, prompts)
```

---

## 2. O que tem dentro de cada curso (leitura real)

### 01 — Introdução a Automações com Python
- **Tipo:** Onboarding motivacional, 100% vídeo curto (2-3 min/aula). Sem código, sem quiz difícil.
- **Cases:** Antes/depois de planilhas manuais, e-mails, PDFs. Não há case com métricas reais, só ilustrativo.
- **Projetos:** Zero. Serve para mapear a trilha (13 cursos obrigatórios + 5 eletivos).
- **Texto extraído:** Definição clara de automação, diferença entre tarefa determinística vs inteligente.
- **Utilidade:** **Baixa técnica, alta estratégica.** Use para não se perder na trilha. Pode ser pulado se já sabe o que é automação.

### 02 — Introdução a Python para Empresas
- **Tipo:** Pitch de Python para quem não é dev. 8 aulas curtas, linguagem de negócios.
- **Cases:** Dashboard FIFA Streamlit (exemplo visual), consolidação de planilhas — sem dataset para baixar.
- **Projetos:** Zero código. Apenas mapa da trilha Python para Empresas (10 cursos, 25h).
- **Utilidade:** **Média.** Bom para convencer chefe/colega. Se você já decidiu aprender Python, pode ir direto para “Aprendendo Python: Conceitos Básicos”.

### 03 — Banco de Integrações com n8n ⭐
- **Tipo:** Hands-on. Cada aula = uma integração. Mostra OAuth no Google Cloud Console, BotFather, API keys.
- **Cases:** Fluxo Gmail→Sheets→Telegram; geração de áudio com ElevenLabs.
- **Projetos:** Ao final você tem **biblioteca de credenciais** — o “banco” reutilizável. Não há projeto único avaliado, mas cada integração é um mini-projeto.
- **Materiais:** Não há ZIP, mas cada aula tem **nodes n8n prontos** para copiar (JSON do workflow). É o material mais reutilizável dos 6.
- **Utilidade:** **Altíssima e imediata.** Sem este curso você não conecta nada no n8n. É pré-requisito para 04 e 05.

### 04 — N8N Open-Source
- **Tipo:** Infra. Tutorial passo-a-passo com Hostinger VPS, Docker, Traefik, SSL.
- **Cases:** Cálculo de custo: n8n.cloud $120/mês vs VPS R$29/mês. Case de LGPD (dados no seu servidor).
- **Projetos:** **1 projeto entregável:** seu n8n em `https://n8n.seudominio.com` rodando com 1 fluxo de teste.
- **Materiais:** `docker-compose.yml` completo nos vídeos + comandos `docker volume`, `traefik.yml`. Não há download, mas é copiável.
- **Utilidade:** **Essencial para quem vai vender automações.** Inútil se for só estudar local.

### 05 — Criando agentes de atendimento profissionais no WhatsApp ⭐⭐
- **Tipo:** Projeto completo de 17 aulas, do zero ao deploy. É o curso mais denso e prático.
- **Cases:** Agente de clínica (agenda), e-commerce (estoque), suporte (ticket). Todos com demo em vídeo.
- **Projetos:** **1 agente completo em produção** com: Meta App, webhook n8n, Postgres `n8n_chat_histories`, OpenAI agent com tools, prompt profissional. É o único com **entregável vendável**.
- **Materiais:** 
  - SQL: `CREATE TABLE n8n_chat_histories (id SERIAL, session_id TEXT, message TEXT, response TEXT, created_at TIMESTAMP)`
  - JSON de workflow n8n (importável)
  - Exemplos de system prompt (persona, regras, tom)
  - Lista de tools (ex: `consultar_disponibilidade`, `buscar_pedido`)
- **Utilidade:** **Máxima.** Se fizer só este curso bem feito, já tem portfólio e produto. É a ponte entre n8n e dinheiro.

### 06 — Fundamentos de análise de dados com IA
- **Tipo:** Conceitual + demo. Mostra ChatGPT/Claude analisando CSVs sem codar.
- **Cases:** Análise de vendas, churn, RH feita em 10 min (upload CSV → prompt → gráficos → insights). Demo com dataset de vendas Olist e Portal da Transparência.
- **Projetos:** **1 relatório completo** com gráficos e insights gerado via IA. Não há notebook Python para baixar, pois a IA gera o código na hora.
- **Materiais:** Datasets de exemplo citados (não como download direto na aula, mas replicáveis: baixe do Olist no Kaggle ou Portal da Transparência). Prompts prontos nos vídeos.
- **Utilidade:** **Alta como validação.** Em 1h você decide se vale seguir para Python. Não substitui curso de Pandas, mas acelera entrega.

---

## 3. Tem cases? Tem projetos? Podemos usar?

| Curso | Cases reais? | Projeto entregável? | Podemos usar como? |
|-------|--------------|---------------------|-------------------|
| 01 | Ilustrativos only | Não | Mapa mental — não reutilizável |
| 02 | Dashboard FIFA (visual) | Não | Slide para vender Python internamente |
| 03 | 2 mini-cases | Sim — banco de credenciais | **Reuso direto:** copie credenciais para qualquer fluxo futuro |
| 04 | Cálculo custo + LGPD | Sim — VPS com n8n | **Reuso direto:** use o mesmo `docker-compose.yml` para todos os clientes |
| 05 | 3 cases vendáveis | **Sim — agente WhatsApp completo** | **Reuso direto + vendável:** troque prompt/tools e venda para clínica/loja. É template. |
| 06 | 3 análises demo | Sim — relatório IA | **Reuso direto:** use os prompts com seu CSV real e entregue relatório em 20 min |

**Conclusão:** 4 dos 6 têm material 100% reutilizável (03,04,05,06). 01 e 02 são só contexto — não precisa revisitar.

---

## 4. Como usar na prática (ordem recomendada)

**Sequência é intencional:** 01-02 dão contexto para não desistir, 03-04 dão base técnica, 05 é o monetizável, 06 é atalho para dados.

**Plano de 7 dias (usando só 20% de cada):**

- **Dia 1:** 01 + 02 em 1.5x, liste 3 tarefas repetitivas suas.
- **Dia 2:** 03 — configure Gmail, Telegram, OpenAI. Faça fluxo `Gmail→Resumo→Telegram`.
- **Dia 3:** 04 — suba VPS Hostinger, aponte domínio, deixe n8n no ar.
- **Dia 4-5:** 05 — clone o fluxo base, crie agente de clínica fictícia, teste 3 conversas.
- **Dia 6:** 06 — pegue CSV real, gere relatório com IA, exporte XLSX/PNG.
- **Dia 7:** Grave 2 min demo do agente + relatório — portfólio pronto.

**Stack mínimo para começar a vender:**
- VPS Hostinger + domínio (~R$40/mês total)
- Conta Meta Business verificada (grátis, mas burocrática)
- OpenAI API key (pay-as-you-go, ~$5 teste)
- n8n self-hosted + Postgres (já vem no docker-compose do curso 04)

**O que NÃO fazer:**
- Não pule 03 e vá para 05 — vai travar em OAuth.
- Não use Z-API para cliente — só protótipo. API Oficial é o único sem risco de ban.
- Não tente decorar 05 inteiro — copie o fluxo base e só troque prompt.

---

## 5. Lacunas e próximos passos

- **Faltante:** Nenhum dos 6 ensina Python de verdade. Após esta sequência, faça na ordem: `Aprendendo Python: Conceitos Básicos (6h)` → `Lendo e Escrevendo Arquivos (3h)` → `PyAutoGUI` (se for automação desktop) ou `Pandas` (se for dados).
- **Pré-requisitos inferidos:** 03 precisa de n8n básico (não está na lista, mas está na trilha). Se nunca abriu n8n, faça antes `Dominando Automações com n8n (2h47)`.
- **Materiais não baixáveis:** Vídeos são streaming protegido — não há MP4 para download. Mas `capa.jpg`, `ementa.md`, `overview.html` e `aulas/*.md` garantem estudo offline.

---

**Arquivos de referência:**
- Resumos individuais: `curso/<pasta>/resumo.md` (6 arquivos)
- 80/20: `RESUMO_80_20.md` (1h15 de leitura focada)
- Ementas: `curso/<pasta>/ementa.md`
- Tabelas completas: `ASIMOV_TABELA_COMPLETA.csv` (105 cursos) e `asimov_cursos.csv` (13 colunas)

*Relatório gerado após leitura das 6 páginas de curso + 55 ementas + 6 descrições longas + vídeos introdutórios. Vídeos assistidos via hub autenticado (bielgnffranco@outlook.com).*
