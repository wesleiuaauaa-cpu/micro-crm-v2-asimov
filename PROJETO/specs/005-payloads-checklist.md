# 005 — Payloads de Teste + Checklist RN

## Payloads curl (usar após capturar amostra real)

**T1 — Cliente novo (deve criar 3 linhas + auto-resposta):**
```bash
curl -X POST "https://hook.make.com/wa-mc-clinica" \
  -H "Content-Type: application/json" \
  -d '{"telefone":"5531999990001","texto":"Olá, quanto custa limpeza?","fromMe":false,"eh_grupo":false,"msg_id":"TEST-001"}'
# Esperado: CLIENTES + OPORTUNIDADES(novo) + INTERACOES + Telegram + HTTP
```

**T2 — Mesmo número em 10 min (não deve reenviar auto-resposta):**
```bash
curl -X POST "https://hook.make.com/wa-mc-clinica" \
  -d '{"telefone":"5531999990001","texto":"e clareamento?","fromMe":false,"eh_grupo":false,"msg_id":"TEST-002"}'
# Esperado: só INTERACOES + Telegram, sem HTTP (janela 24h)
```

**T3 — Mensagem do lojista (fromMe):**
```bash
curl -X POST "https://hook.make.com/wa-mc-clinica" \
  -d '{"telefone":"5531999990001","texto":"ok","fromMe":true,"eh_grupo":false,"msg_id":"TEST-003"}'
# Esperado: 1 op total, nada criado
```

**WAHA vs Z-API (trocar URL/header):**
- WAHA: `POST http://waha:3000/api/sendText` `{"chatId":"55319...@c.us","text":"...","session":"wa-clinica"}`
- Z-API: `POST https://api.z-api.io/instances/ID/token/TK/send-text` `{"phone":"55319...","message":"..."}`

## Checklist RN-01..17 (auditoria de blueprint)

- [ ] RN-01 telefone_norm só dígitos, prefixo 55, fallback 8 dígitos
- [ ] RN-02 fromMe/grupo ignorados, Path C 0 módulos
- [ ] RN-03 cadeia CLIENTES→INTERACOES→OPORTUNIDADES com FK
- [ ] RN-04 proximo_contato = hoje + dias_followup (2), digest filtra ≤hoje
- [ ] RN-05 janela 24h para auto-resposta
- [ ] RN-06 digest 08:00 America/Sao_Paulo, relatório domingo
- [ ] RN-07 fechado/perdido fora dos alertas, perdido exige motivo
- [ ] RN-08 AGENDAMENTOS pendente_sync + reprocesso SC2
- [ ] RN-09 log só erro + auto-resposta, router não consome
- [ ] RN-10 SC2 é 1 cenário (Router domingo)
- [ ] RN-11 isolamento: pasta MC-<slug>, conexões google-<slug>
- [ ] RN-12 LGPD: Sheets na conta do lojista
- [ ] RN-13 datas como date real, fuso CONFIG
- [ ] RN-15 estágio só por edição na planilha
- [ ] RN-16 formatDate dddd == Sunday em inglês
- [ ] RN-17 segredos só nas conexões Make, nunca na planilha

## Testes T4-T10 (do V2, executar após M1-M3)
T4 proximo_contato ontem/amanhã, T5 perdido sem motivo, T6 agendamento, T7 HTTP inválido, T8 domingo, T9 digest sem novidade, T10 replicação.

→ Skipped: teste de carga (>100 msgs) — add quando atingir 50 msgs/dia.
