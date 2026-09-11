# Salvamento e Categorização de Contatos pelo WhatsApp — Materiais

**Verificação:** 6 aulas verificadas aula a aula via Playwright (autenticado). **Nenhum botão Baixar materiais encontrado** em nenhuma atividade — confirmado via outerHTML.includes('Baixar materiais') == false e drive.google.com == 0 para todas as 6 aulas.

**O que este projeto realmente oferece:**
- Fluxo n8n construído passo a passo em vídeo (sem ZIP para download).
- 1 snippet de código encontrado em ormatando-data-e-manipulando-o-fluxo-de-dados:
  ``n8n
  {{ $now.format('yyyy/MM/dd') }}
  ``
  Usado para padronizar data antes de salvar no Google Sheets.

**Como reproduzir:**
- Siga os vídeos na ordem: Introdução ? Webhook ? Normalização ? Agente IA (categoriza via AI Extract Structured Data) ? Formata data ? Google Sheets Append Row.
- Não há workflow JSON para importar; monte manualmente seguindo o vídeo. O agente usa AI Extract para classificar contato como lead | suporte | venda.

**Arquivos nesta pasta:**
- codigo-formatando-data.md — snippet acima com explicação
- README.md — este inventário

Se precisar do workflow, use como base workflow-agente-asimov.json do curso 05 (estrutura similar, troque Sheets).
