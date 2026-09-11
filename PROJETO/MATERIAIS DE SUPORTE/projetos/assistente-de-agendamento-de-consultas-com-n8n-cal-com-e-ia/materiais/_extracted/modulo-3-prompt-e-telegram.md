# Módulo 3 — Prompt do Agente e Telegram

---

## Estrutura do prompt

O prompt do agente está no nó **AI Agent → System Message** e é dividido em blocos:

| Bloco | Função |
|---|---|
| **Identidade** | Define quem o agente é e para quem trabalha |
| **Contexto dinâmico** | Injeta nome, nicho, serviço e e-mail do profissional via `Config Cal.com` |
| **Estrutura das mensagens** | Força parágrafos curtos e proíbe markdown |
| **Datas dinâmicas** | Injeta hoje e os próximos 8 dias para o agente raciocinar sobre datas |
| **Fluxo de atendimento** | Define os passos para novo agendamento, reagendamento e cancelamento |
| **Ferramentas disponíveis** | Explica quando e como usar cada ferramenta |
| **Regras obrigatórias** | Impede ações irreversíveis sem confirmação, evita inventar horários |
| **Memória persistente** | Orienta o agente a usar o histórico para não repetir perguntas |

---

## Variáveis dinâmicas usadas no prompt

Todos os valores abaixo são puxados automaticamente do nó `Config Cal.com`:

| Expressão no prompt | O que injeta |
|---|---|
| `$('Config Cal.com').item.json.profissional_nome` | Nome do profissional |
| `$('Config Cal.com').item.json.profissional_nicho` | Nicho/especialidade |
| `$('Config Cal.com').item.json.profissional_servico` | Nome do serviço |
| `$('Config Cal.com').item.json.profissional_email` | E-mail de contato |
| `$today.setLocale('pt-BR').toFormat("cccc, dd/MM/yyyy")` | Data de hoje por extenso |

---

## Configurando o bot no Telegram

1. Abra o Telegram e acesse @BotFather: https://t.me/BotFather
2. Digite `/newbot` e siga as instruções
3. Ao final, o BotFather fornece o **Bot Token** — copie e guarde
4. No n8n, crie uma credencial **Telegram API** com esse token
5. Vincule a credencial aos nós `Telegram Trigger` e `Send a text message`
6. Ative o workflow — o bot já estará ouvindo mensagens

---

## Links do módulo

### Telegram
- BotFather: https://t.me/BotFather
- Documentação da API: https://core.telegram.org/bots/api
- Nó Telegram Trigger (n8n): https://docs.n8n.io/integrations/builtin/trigger-nodes/n8n-nodes-base.telegramtrigger

### OpenAI (Whisper — transcrição de áudio)
- Documentação Whisper: https://platform.openai.com/docs/guides/speech-to-text
- Modelos disponíveis: https://platform.openai.com/docs/models
