# Módulo 1 — Cal.com e Criando o Agente

---

## Workflow para importar

Baixe o arquivo `assistente-multi-agendamento.json` e importe no n8n:
**Menu → Import from file → selecione o JSON**

Credenciais a configurar após importar:

| Nó | Credencial |
|---|---|
| `OpenAI Chat Model` + `Transcribe a recording` + `Analyze image` | OpenAI API Key |
| `Analyze video` | Google Gemini API Key |
| `Telegram Trigger` + `Send a text message` | Telegram Bot Token |
| `Postgres Chat Memory` | Postgres (host, user, senha, banco) |

---

## Variáveis do nó Config Cal.com

Altere apenas este nó para adaptar o assistente a qualquer profissional.

| Variável | Descrição | Exemplo |
|---|---|---|
| `cal_api_key` | Chave de API do Cal.com | `cal_live_xxxxxxxxxxxx` |
| `cal_event_type_slots` | ID do tipo de evento | `5079051` |
| `cal_event_type_booking` | ID do tipo de evento (bookings) | `5079051` |
| `cal_timezone` | Fuso horário | `America/Sao_Paulo` |
| `cal_rescheduled_by` | E-mail autor do reagendamento | `contato@seudominio.com` |
| `cal_api_version_slots` | Versão da API de slots | `2024-09-04` |
| `cal_api_version_booking` | Versão da API de bookings | `2024-08-13` |
| `profissional_nome` | Nome do profissional | `Maria Silva` |
| `profissional_email` | E-mail de contato | `maria@clinica.com` |
| `profissional_nicho` | Área de atuação | `psicologia` |
| `profissional_servico` | Nome do serviço | `consulta` |

---

## Links do módulo

### Cal.com
- Criar conta: https://app.cal.com/signup
- Criar Event Type: https://app.cal.com/event-types
- Gerar API Key: https://app.cal.com/settings/developer/api-keys
- Conectar Google Calendar / Outlook / Apple: https://app.cal.com/settings/my-account/calendars
- Documentação da API v2: https://cal.com/docs/api-reference/v2

### n8n
- AI Agent: https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent
- Expressões: https://docs.n8n.io/code/expressions

### Postgres (memória)
- Neon (gratuito): https://neon.tech
- Supabase (alternativa): https://supabase.com
