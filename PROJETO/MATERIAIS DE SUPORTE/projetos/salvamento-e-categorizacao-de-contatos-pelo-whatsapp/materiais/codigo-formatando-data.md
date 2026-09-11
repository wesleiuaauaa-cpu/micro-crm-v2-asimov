# Código — Formatando Data para Google Sheets

Encontrado em projeto/atividade/formatando-data-e-manipulando-o-fluxo-de-dados/:

``n8n
{{ $now.format('yyyy/MM/dd') }}
``

**Contexto:** O n8n recebe   (data atual) e formata para yyyy/MM/dd antes de salvar na planilha. Saída deve ser 2025/09/22.

**Variações úteis:**
- {{ $now.format('dd/MM/yyyy HH:mm') }}
- {{ $json.data_criacao.format('yyyy-MM-dd') }} se a data vier do webhook.

**Uso no fluxo:** Node Set ou Edit Fields antes do Google Sheets Append Row.
