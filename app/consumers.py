"""Kafka consumers for appointment-slots-service.

One handler per subscribed topic. Real handlers write to this service's own
database and/or publish follow-up events; stub handlers just log + audit.
"""
from __future__ import annotations

import logging

from psycopg.types.json import Json

from healthcare_common.audit import emit_audit

log = logging.getLogger("appointment-slots-service.consumers")

TABLE = "appointment_slots"


def register(svc) -> None:
    bus = svc.bus
    db = svc.db
    clients = svc.clients

    @bus.on("appointment.booked")
    def _on_appointment_booked(envelope: dict) -> None:
        data = envelope.get("data") or {}
        try:
                    # Mark slot occupied.
                    slot_id = data.get("slot_id")
                    if slot_id:
                        db.execute(f"UPDATE {TABLE} SET status='booked', updated_at=now() "
                                   f"WHERE id = %s", (int(slot_id),))
        except Exception as e:
            log.exception("appointment-slots-service/appointment.booked handler failed: %s", e)
        emit_audit(bus, action="consume.appointment.booked", actor="system:appointment-slots-service",
                   target=None, details={"envelope_id": envelope.get("id")})

    @bus.on("appointment.cancelled")
    def _on_appointment_cancelled(envelope: dict) -> None:
        data = envelope.get("data") or {}
        try:
                    slot_id = data.get("slot_id")
                    if slot_id:
                        db.execute(f"UPDATE {TABLE} SET status='open', updated_at=now() "
                                   f"WHERE id = %s", (int(slot_id),))
        except Exception as e:
            log.exception("appointment-slots-service/appointment.cancelled handler failed: %s", e)
        emit_audit(bus, action="consume.appointment.cancelled", actor="system:appointment-slots-service",
                   target=None, details={"envelope_id": envelope.get("id")})

