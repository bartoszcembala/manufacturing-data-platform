
import uuid
import random

from datetime import datetime, timedelta, timezone


NAMESPACE = uuid.UUID("a4e7d6d2-44e1-4c84-9a21-6c80bb2a7e01")


class TelemetryGenerator:

    def __init__(self, machines, seed=42):
        self.machines = machines
        self.random = random.Random(seed)

    def generate(self, days=30, interval_minutes=15):

        now = datetime.now(timezone.utc)

        # Zaokrąglenie do pełnego interwału.
        minute = (
            now.minute // interval_minutes
        ) * interval_minutes

        end_time = now.replace(
            minute=minute,
            second=0,
            microsecond=0
        )

        start_time = end_time - timedelta(days=days)

        records = []

        for machine in self.machines:

            machine_id = machine["machine_id"]
            current_time = start_time

            while current_time <= end_time:

                temperature = self.random.uniform(55, 90)
                pressure = self.random.uniform(3.5, 7.0)
                speed = self.random.uniform(800, 1500)
                energy = self.random.uniform(2.0, 6.0)

                # Sporadyczne anomalie.
                if self.random.random() < 0.02:
                    temperature += self.random.uniform(20, 40)

                if self.random.random() < 0.01:
                    pressure += self.random.uniform(2, 5)

                # Stabilny identyfikator dla maszyny i czasu.
                event_key = f"{machine_id}:{current_time.isoformat()}"

                records.append({
                    "source_event_id": str(
                        uuid.uuid5(NAMESPACE, event_key)
                    ),
                    "machine_id": machine_id,
                    "recorded_at": current_time,
                    "temperature": round(temperature, 2),
                    "pressure": round(pressure, 2),
                    "speed": round(speed, 2),
                    "energy_consumption": round(energy, 3)
                })

                current_time += timedelta(
                    minutes=interval_minutes
                )

        return records
