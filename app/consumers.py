"""Kafka consumers for appointment-slots-service.

One handler per subscribed topic. Handlers are best-effort logging plus
audit — services override this file to implement real cross-domain behavior.
"""
from __future__ import annotations

import logging

from healthcare_common.audit import emit_audit

log = logging.getLogger("appointment-slots-service.consumers")


def register(svc) -> None:
    bus = svc.bus

    @bus.on("appointment.booked")
    def _on_appointment_booked(envelope: dict) -> None:
        log.info("appointment-slots-service: received appointment.booked id=%s", envelope.get("id"))
        emit_audit(bus, action="consume.appointment.booked", actor="system:appointment-slots-service",
                   target=None, details={"envelope_id": envelope.get("id")})

    @bus.on("appointment.cancelled")
    def _on_appointment_cancelled(envelope: dict) -> None:
        log.info("appointment-slots-service: received appointment.cancelled id=%s", envelope.get("id"))
        emit_audit(bus, action="consume.appointment.cancelled", actor="system:appointment-slots-service",
                   target=None, details={"envelope_id": envelope.get("id")})

