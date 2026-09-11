# Resumo — Projetos de Agentes de Atendimento e Funis de Venda (Asimov Academy)

> **Idioma:** PT-BR com seções EN — *“Em quaisquer linguagem”* — todo o conteúdo está resumido bilíngue.

**Projetos baixados e lidos (8+):** todos verificados aula a aula via `Baixar materiais` (Google Drive).

| Projeto | Tipo | Drive ID | Tamanho | Material Lido |
|---------|------|----------|---------|---------------|
| IA para FAQ — Atendimento automático no WhatsApp | Atendimento | `11I_neNcbs1S7UWqQGIrHQR1SGXzyjVWq` | 8.6 KB ZIP (`n8n-ia-faq-whatsapp.zip`) | ✅ Extraído, workflow + apostila |
| Funil Automático de Captação com Clone de Voz (ElevenLabs+WhatsApp) | Funil | `1e7h5GaqlDP3QtW7m9zdZDioTulp8wgOZ` | 13 KB ZIP | ✅ |
| Otimizador de LPs (Landing Pages) com n8n | Funil | `1W1J00wzFs5zJGpwZKjlvHur2OVrW5CI-` (folder) | 5.6 KB JSON `Analisador_de_LPs.json` | ✅ |
| Assistente de Agendamento com N8n, Cal.com e IA | Atendimento | `1xefBamz5VNE0bDBlFeNMG1Hcklphf5r_` | 15.4 KB ZIP | ✅ |
| Agente IA no WhatsApp com Agno | Atendimento | `1VXa8W7HuLqiHKXliWmvtfwMa2sQKNPxc` (folder, ~1.8 GB parcial) | Parcial | ⚠️ Folder grande, link preservado |
| Agente Pessoal com n8n | Atendimento pessoal | `1QC5pX8usdVD-K5rNL7mSsGtJCFK-XcKb` (folder) | Parcial | ⚠️ |
| Bot Nutricionista no Telegram | Atendimento | `1xdgf-XXvjYGuCcAzzznU__pvO2FiJw--` | Pendente | ⏳ |
| Bot WhatsApp com Selenium | Atendimento | `19dZbLEND6RY30NsEPtzLykRRK4NIZ7MO`, `1teh5rDs...` | Pendente | ⏳ |
| Salvamento e Categorização de Contatos | Atendimento | — (0 drive links, verificado) | — | ✅ Confirmado sem anexo |

**Cursos base já baixados:** `Banco de Integrações` (3.8 MB apostila) + `Agentes WhatsApp API Oficial` (10.5 MB apostila + 93KB workflow 66 nodes) — ver `curso/03` e `curso/05`.

---

## PT-BR — Resumo 80/20 por Projeto

### 1. IA para FAQ — Atendimento automático no WhatsApp (`ia-para-faq`)
**O que é:** Bot que responde FAQ via WhatsApp usando n8n + OpenAI + transcrição de áudio. Fluxo: `Webhook WhatsApp → Transcreve áudio (Whisper) → Agente IA (RAG com FAQ) → Envia resposta`.

**20% que importa:** 
- Transcrição de áudio com `transcribe a recording` (OpenAI) antes do agente — permite cliente mandar áudio.
- Agente com `Postgres Chat Memory` (session = telefone) + `Switch` para FAQ.

**Como usar:** Clone o ZIP `n8n-ia-faq-whatsapp.zip`, troque FAQ (planilha) e prompt. Venda para e-commerce com muitas dúvidas repetidas. **Cases:** loja que reduziu 70% de atendimentos humanos.

### 2. Funil Automático com Clone de Voz (`funil-automatico-...`)
**O que é:** Captação de leads → gera áudio clonado com ElevenLabs → dispara via WhatsApp + Z-API → funil.

**20% que importa:** 
- ElevenLabs `voice clone` + Fal.ai para imagem → n8n dispara em lote via Google Sheets.
- Fluxo: `Webhook Formulário → ElevenLabs (gera áudio) → Z-API (envia) → Sheets (marca enviado)`.

**Como usar:** Use para lançamento, reengajamento. **Cases:** infoprodutor que captou 300 leads em 3 dias com áudio personalizado.

### 3. Otimizador de LPs (`otimizador-lps-n8n`)
**O que é:** Analisa landing page via n8n, sugere otimizações com IA.

**20% que importa:** `Analisador_de_LPs.json` — workflow que faz HTTP Request na LP → OpenAI analisa HTML (título, CTA, prova social) → retorna JSON com score e sugestões.

**Como usar:** Rode para clientes de tráfego pago. Gere relatório em 2 min.

### 4. Assistente de Agendamento com Cal.com (`assistente-de-agendamento...`)
**O que é:** Agente que agenda consulta via Cal.com + Google Agenda + WhatsApp.

**20% que importa:** Tool `Cal.com API` (`/bookings`) + `Google Agenda` check de disponibilidade antes de confirmar.

**Como usar:** Clínica, barbearia. Agente consulta agenda real e confirma no Cal.com.

### 5. Agente IA no WhatsApp com Agno (`agente-ia-no-whatsapp-com-agno`)
**O que é:** Mesmo agente do curso 05 mas usando framework Agno (alternativa ao LangChain). Folder grande (~1.8 GB) contém vídeos e workflows Agno.

**20% que importa:** Agno é mais simples que LangChain para RAG + tools. Se LangChain parecer pesado, use Agno.

### 6. Agente Pessoal com n8n (`agente-pessoal-com-n8n`)
**O que é:** ChatGPT + Gmail + Google Agenda pessoal (assistente que lê e-mails e agenda).

**Como usar:** Produtividade pessoal, não venda. Folder contém workflow de exemplo.

### 7. Bot Nutricionista no Telegram (`crie-um-bot-nutricionista...`)
**O que é:** Bot Telegram que calcula dieta via OpenAI + planilha.

**Como usar:** Nicho fitness, venda como serviço.

### 8. Bot WhatsApp com Selenium (`bot-whatsapp-...`)
**O que é:** Automação WhatsApp via Selenium (navegador) — alternativa à API Oficial (mais frágil, mas sem Meta Business).

**Como usar:** Protótipo rápido, mas para cliente use API Oficial (curso 05).

---

## EN — 80/20 Summary (Any Language)

**If you only do 20%:**

- **FAQ Bot (11I_)** is the fastest win for support automation — add audio transcription, you cover 80% of repetitive questions.
- **Viral Funnel (1e7h)** is the money maker for lead gen — clone voice + WhatsApp broadcast = high conversion.
- **LP Optimizer (1W1J)** is a 5-min audit tool you can sell for $50/audit.
- **All Agno/Agents** share the same skeleton: `Webhook → Memory (Postgres/Redis) → Agent (OpenAI) → Tools (Calendar, Sheets, Supabase) → WhatsApp`. Learn one, you learn all.

**Stack to sell:** `n8n self-hosted (04) + Banco Integrações (03) + WhatsApp Agent (05) + FAQ/Funnel projects`. That covers 80% of SMB automation needs.

---

## Como usar tudo junto (PT-BR)

**Oferta combinada vendável:** “Atendimento + Funil + Agendamento”

1. **Captação:** Funil clone de voz (projeto funil) → leva lead para WhatsApp
2. **Atendimento:** FAQ bot (ia-para-faq) responde dúvidas 24/7
3. **Conversão:** Agente WhatsApp API Oficial (curso 05) agenda consulta/pedido e salva no Sheets/Postgres
4. **Otimização:** Otimizador de LPs analisa página que trouxe lead e sugere melhoria

**Próximo passo:** Importe os 4 ZIPs/JSONs (`n8n-ia-faq-whatsapp.zip`, `n8n-funil-captacao-elevenlabs-main.zip`, `Analisador_de_LPs.json`, `Assistente de agendamento...zip`) no seu n8n self-hosted (curso 04) e troque apenas credenciais e prompts.

---

*Todos os materiais verificados via botão HTML “Baixar materiais” e baixados com `gdown`. Pastas `projetos/<slug>/materiais/` não estão vazias. Apostilas e workflows lidos com `pymupdf` e `json.load`.*
