# appointment-slots-service

appointment-slots-service — domain: appointments

- **Port:** 8601
- **Language:** Python 3.11 + Flask
- **Database:** `appointments` (Postgres, table `appointment_slots`)
- **Event bus:** Kafka

## API

| Method    | Path                       |
|-----------|----------------------------|
| GET       | `/api/appointment_slots/`          |
| POST      | `/api/appointment_slots/`          |
| GET       | `/api/appointment_slots/<id>`      |
| PUT/PATCH | `/api/appointment_slots/<id>`      |
| DELETE    | `/api/appointment_slots/<id>`      |
| GET       | `/health`                  |
| GET       | `/ready`                   |

## Events

**Publishes:** (none)
**Subscribes:** appointment.booked, appointment.cancelled

## HTTP peer dependencies

- `provider-schedule-service`
- `audit-log-service`

## Local dev

```bash
pip install -e ../../libs/py-healthcare-common
pip install -r requirements.txt
cp .env.example .env
(cd ../../infra && docker compose up -d postgres kafka kafka-init)
python -m app.main
```

## Tests

```bash
pytest
```
