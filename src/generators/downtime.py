
import uuid
import random

from datetime import datetime, timedelta, timezone


NAMESPACE = uuid.UUID("a4e7d6d2-44e1-4c84-9a21-6c80bb2a7e03")


DOWNTIME_REASONS = {
    "MECHANICAL_FAILURE": [
        "Hydraulic system failure",
        "Bearing damage",
        "Motor malfunction"
    ],
    "ELECTRICAL_FAILURE": [
        "Power supply interruption",
        "Sensor failure",
        "Control system error"
    ],
    "MATERIAL_SHORTAGE": [
        "Raw material unavailable",
        "Delayed material delivery"
    ],
    "CHANGEOVER": [
        "Product changeover",
        "Machine setup"
    ],
    "MAINTENANCE": [
        "Scheduled maintenance",
        "Preventive inspection"
    ]
}


class DowntimeGenerator:

    def __init__(self, machines, seed=42):
        self.machines = machines
        self.random = random.Random(seed)

    def generate(self, days=30, events_per_day=4):

        now = datetime.now(timezone.utc)
        start = now - timedelta(days=days)

        records = []

        for day in range(days):

            current_day = start + timedelta(days=day)

            for event_number in range(events_per_day):

                machine = self.random.choice(self.machines)

                reason = self.random.choice(
                    list(DOWNTIME_REASONS.keys())
                )

                description = self.random.choice(
                    DOWNTIME_REASONS[reason]
                )

                started_at = current_day + timedelta(
                    minutes=self.random.randint(0, 1439)
                )

                duration_minutes = self.random.randint(10, 180)

                ended_at = started_at + timedelta(
                    minutes=duration_minutes
                )

                # Nie generujemy przyszłych zakończeń.
                if ended_at > now:
                    continue

                is_planned = reason in (
                    "CHANGEOVER",
                    "MAINTENANCE"
                )

                event_key = (
                    f"{machine['machine_id']}:"
                    f"{started_at.isoformat()}:"
                    f"{event_number}"
                )

                records.append({
                    "source_event_id": str(
                        uuid.uuid5(NAMESPACE, event_key)
                    ),
                    "machine_id": machine["machine_id"],
                    "started_at": started_at,
                    "ended_at": ended_at,
                    "reason_category": reason,
                    "description": description,
                    "is_planned": is_planned
                })

        return records
