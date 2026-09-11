# Módulo 2 — As Ferramentas do Agente

---

## 1. Disponibilidade — Consultar horários livres

```bash
curl -X GET "https://api.cal.com/v2/slots\
?eventTypeId={{ EVENT_TYPE_ID }}\
&start={{ START_DATE }}\
&end={{ END_DATE }}\
&timeZone={{ TIMEZONE }}" \
  -H "Authorization: Bearer {{ CAL_API_KEY }}" \
  -H "cal-api-version: 2024-09-04"
```

**Variáveis:**
- `EVENT_TYPE_ID` — ID do evento no Cal.com (ex: `5079051`)
- `START_DATE` — data inicial `YYYY-MM-DD` (ex: `2025-06-02`)
- `END_DATE` — data final `YYYY-MM-DD` (ex: `2025-06-06`)
- `TIMEZONE` — fuso horário (ex: `America/Sao_Paulo`)
- `CAL_API_KEY` — sua chave `cal_live_...`

> Se `slots` retornar vazio, não há horários disponíveis no período.

---

## 2. Agendar — Criar novo agendamento

```bash
curl -X POST "https://api.cal.com/v2/bookings" \
  -H "Authorization: Bearer {{ CAL_API_KEY }}" \
  -H "cal-api-version: 2024-08-13" \
  -H "Content-Type: application/json" \
  -d '{
    "start": "{{ START_ISO_UTC }}",
    "eventTypeId": {{ EVENT_TYPE_ID }},
    "attendee": {
      "name": "{{ ATTENDEE_NAME }}",
      "email": "{{ ATTENDEE_EMAIL }}",
      "timeZone": "{{ TIMEZONE }}",
      "language": "pt-BR",
      "phoneNumber": "{{ ATTENDEE_PHONE }}"
    },
    "metadata": {
      "origem": "Telegram"
    }
  }'
```

**Variáveis:**
- `START_ISO_UTC` — horário em UTC ISO 8601 (ex: `2025-06-02T18:00:00Z` = 15h em Brasília)
- `EVENT_TYPE_ID` — ID do tipo de evento (número, sem aspas)
- `ATTENDEE_NAME` — nome completo do cliente
- `ATTENDEE_EMAIL` — e-mail do cliente
- `ATTENDEE_PHONE` — telefone com DDI e DDD (ex: `+5511999999999`)

> **Conversão de fuso:** Brasília é UTC-3. Some 3h ao horário local → 15h vira `18:00:00Z`.

---

## 3. Buscar BookingUID — Listar agendamentos futuros

```bash
curl -X GET "https://api.cal.com/v2/bookings\
?status=upcoming\
&attendeeEmail={{ ATTENDEE_EMAIL }}\
&eventTypeId={{ EVENT_TYPE_ID }}\
&sortStart=asc\
&take=10" \
  -H "Authorization: Bearer {{ CAL_API_KEY }}" \
  -H "cal-api-version: 2024-08-13"
```

**Variáveis:**
- `ATTENDEE_EMAIL` — e-mail do cliente
- `EVENT_TYPE_ID` — ID do tipo de evento
- `CAL_API_KEY` — sua chave `cal_live_...`

> O `uid` necessário para reagendar ou cancelar está em `data[0].uid` da resposta.

---

## 4. Reagendar — Alterar horário de um agendamento

```bash
curl -X POST "https://api.cal.com/v2/bookings/{{ BOOKING_UID }}/reschedule" \
  -H "Authorization: Bearer {{ CAL_API_KEY }}" \
  -H "cal-api-version: 2024-08-13" \
  -H "Content-Type: application/json" \
  -d '{
    "start": "{{ NEW_START_ISO_UTC }}",
    "rescheduledBy": "{{ RESCHEDULED_BY_EMAIL }}",
    "reschedulingReason": "{{ REASON }}"
  }'
```

**Variáveis:**
- `BOOKING_UID` — UID obtido via **Buscar BookingUID** (ex: `abc123xyz`)
- `NEW_START_ISO_UTC` — novo horário em UTC ISO 8601
- `RESCHEDULED_BY_EMAIL` — e-mail registrado como responsável pelo reagendamento
- `REASON` — motivo (ex: `Cliente solicitou reagendamento`)

---

## 5. Cancelar — Cancelar um agendamento

```bash
curl -X POST "https://api.cal.com/v2/bookings/{{ BOOKING_UID }}/cancel" \
  -H "Authorization: Bearer {{ CAL_API_KEY }}" \
  -H "cal-api-version: 2024-08-13" \
  -H "Content-Type: application/json" \
  -d '{
    "cancellationReason": "{{ CANCELLATION_REASON }}",
    "cancelSubsequentBookings": false
  }'
```

**Variáveis:**
- `BOOKING_UID` — UID obtido via **Buscar BookingUID**
- `CANCELLATION_REASON` — motivo (ex: `Cliente cancelou a sessão`)

---

## Links do módulo

- Slots API: https://cal.com/docs/api-reference/v2/slots/get-available-slots
- Bookings API: https://cal.com/docs/api-reference/v2/bookings/create-a-booking
- HTTP Request Tool (n8n): https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest
