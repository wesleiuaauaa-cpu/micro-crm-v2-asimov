# Resumo 80/20 — Os 6 Cursos na Ordem Recomendada

> **Princípio 80/20:** 20% do conteúdo gera 80% do resultado. Este documento extrai exatamente esse 20% dos 6 cursos, na ordem solicitada.

**Ordem:**
1. Introdução a Automações com Python (18 min)
2. Introdução a Python para Empresas (22 min)
3. Banco de Integrações com n8n (47 min)
4. N8N Open-Source (48 min)
5. Criando agentes de atendimento profissionais no WhatsApp (2h 29 min) — *core monetizável*
6. Fundamentos de análise de dados com IA (59 min)

**Tempo total:** ~5h02 — **Tempo 80/20:** ~1h15 focado

---

## Visão Geral 80/20 do Conjunto

Se você só puder lembrar de **3 ideias** dos 6 cursos:

1.  **Automação = trocar tarefa repetitiva por fluxo que roda sozinho.** O maior ganho não é técnico, é de **posicionamento**: você deixa de ser executor e vira solucionador. As duas intros (01 e 02) servem só para isso — pule rápido para a prática.
2.  **n8n só funciona quando o banco de integrações está pronto.** As 8 credenciais (Gmail, Telegram, OpenAI, Groq, ElevenLabs, Fal, Z-API, etc) são o gargalo. Configure uma vez (curso 03) e reutilize em tudo. Depois, tire do cloud (curso 04) para baratear e ter controle — VPS Hostinger + Docker + domínio + Traefik = R$30/mês vs R$150+ no cloud.
3.  **O dinheiro está no agente de WhatsApp via API Oficial.** É o único projeto dos 6 que é **vendável** (clínica, e-commerce). Ele junta tudo: webhook Meta, n8n, Postgres (histórico), OpenAI (prompt/tools). Se dominar o fluxo do curso 05, você consegue cobrar R$500-2k/mês por cliente. O curso 06 é o atalho para análise de dados com IA sem codar — use para validar valor de dados antes de mergulhar em Python.

---

## 80/20 por Curso (o que realmente importa)

### 01 — Introdução a Automações com Python (6 aulas, 18 min)
**20% que importa:**
- Definição: automação = sequência determinística que manipula arquivos, e-mails, planilhas, navegador.
- Mapa da trilha: 13 cursos. Ordem importa — não pule para PyAutoGUI sem antes fazer Lógica + Setup.
- Ponte com outras trilhas: automação alimenta dashboards e IA.

**Ignorável 80%:** motivacional sobre produtividade 100x — veja em 1.5x.

**Ação 80/20:** Liste 3 tarefas suas que levam >15 min/dia e marque qual curso da trilha resolve cada uma.

### 02 — Introdução a Python para Empresas (8 aulas, 22 min)
**20% que importa:**
- Pitch para gestores: Python vs Excel/VBA — Python ganha em escala, reuso e integração.
- Trilha Python para Empresas = 10 cursos (25h) focados em Streamlit, Pandas, automações.
- Onde Python se encaixa: automações (RPA), dashboards (Streamlit), IA.

**Ignorável:** história da Asimov.

**Ação 80/20:** Escolha 1 dor da sua empresa (ex: consolidar 10 planilhas) e prometa entregar em Streamlit — use o argumento do curso para vender internamente.

### 03 — Banco de Integrações com n8n (9 aulas, 47 min) ⭐ ALAVANCA
**20% que importa (80% do valor do n8n):**
- **Gmail/Sheets/Drive** via OAuth: escopos `gmail.send`, `spreadsheets`, `drive`. Sem isso nada integra.
- **Telegram:** criar bot com @BotFather, pegar token, usar webhook.
- **OpenAI + Groq:** mesma interface, Groq é 10x mais barato para testes.
- **Z-API vs API Oficial:** Z-API é gambiarra rápida (QR), Oficial é definitiva (pago, mas sem ban).

**Ignorável:** ElevenLabs/Fal.ai a menos que vá gerar áudio/imagem.

**Ação 80/20:** Em 1 hora, configure Gmail + Telegram + OpenAI no seu n8n e crie fluxo: `Manual Trigger → Gmail (lê) → OpenAI (resume) → Telegram (envia)`. Valida tudo.

### 04 — N8N Open-Source (5 aulas, 48 min) ⭐ ECONOMIA
**20% que importa:**
- `docker-compose` com n8n + Postgres + Traefik na Hostinger VPS.
- Domínio + SSL automático via Traefik/Let's Encrypt.
- Backup: `docker volume` + export de workflows JSON.

**Ignorável:** comparação teórica cloud vs self — decida: se vai vender, self-hosted.

**Ação 80/20:** Suba VPS Hostinger (R$29), rode `docker-compose up -d`, aponte `n8n.seudominio.com`, importe um workflow do curso 03 e confirme que roda 24/7.

### 05 — Agentes WhatsApp API Oficial (17 aulas, 2h29) ⭐ CORE MONETIZÁVEL
**20% que importa (o esqueleto que se repete):**
- **Meta App:** criar app em developers.facebook.com, token de longa duração, adicionar produto WhatsApp, registrar número virtual.
- **Webhook:** URL do n8n `/webhook/whatsapp` + token verify → Meta valida → mensagem entra.
- **Fluxo n8n:** `Webhook → Postgres (busca histórico) → OpenAI Agent (prompt + tools) → WhatsApp (responde) → Postgres (salva)`.
- **Prompt:** persona + regras + ferramentas (ex: `consultar_agenda`, `buscar_produto`). Sem tools, agente é só chat.
- **Tabela `n8n_chat_histories`:** `session_id`, `mensagem`, `resposta`, `timestamp` — sem isso não há memória.

**80% que é detalhe:** instalação Railway vs VPS, UI de cada nó.

**Ação 80/20:** Clone o fluxo base do curso, troque o prompt para um caso real (ex: clínica: “você é recepcionista, só agenda se horário livre”), teste 3 conversas multi-turno e printe para portfólio.

### 06 — Fundamentos de análise de dados com IA (10 aulas, 59 min)
**20% que importa:**
- **Upload CSV → Prompt direcionado:** “Analise vendas por mês, faça gráfico de linha e me diga 3 insights”.
- **Validar código gerado:** IA alucina números — sempre recalcule 1 métrica na mão.
- **Exportar:** peça `“gere XLSX com aba resumo e PNG do gráfico”`.

**Ignorável:** teoria do “novo analista”.

**Ação 80/20:** Pegue um CSV real seu (vendas, RH), faça upload no ChatGPT/Claude, rode 1 análise direcionada e 1 exploratória (“o que mais você vê?”), exporte relatório e entregue — em 20 min você tem case.

---

## Roteiro de Estudo 80/20 (1 semana)

| Dia | Curso | Fazer (não só assistir) |
|-----|-------|-------------------------|
| 1 | 01 + 02 | Assista 1.5x, liste 3 automações da sua rotina |
| 2 | 03 | Configure Gmail, Telegram, OpenAI no n8n |
| 3 | 04 | Suba VPS + n8n com domínio |
| 4-5 | 05 | Monte agente WhatsApp com 1 tool + memória |
| 6 | 06 | Gere 1 relatório com IA a partir de CSV real |
| 7 | Revisão | Grave vídeo de 2 min demo do agente + relatório — portfólio |

**Regra 80/20:** Se travar em 04 (VPS), use n8n.cloud temporariamente e siga para 05. Não deixe infra bloquear projeto vendável.

---

## O que NÃO fazer (economiza 80% do tempo perdido)

- Não tente decorar todas as integrações de 03 — foque Gmail + 1 LLM + 1 canal (Telegram ou WhatsApp).
- Não assista 05 sem ter 03 e 04 prontos — vai copiar sem entender webhook.
- Não use Z-API para cliente final — só para protótipo. API Oficial é o único caminho LGPD-safe.

---

*Resumos completos por curso em `curso/<pasta>/resumo.md` — este 80/20 é o extrato para execução rápida.*
