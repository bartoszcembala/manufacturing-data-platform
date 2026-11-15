
import uuid
import random

from datetime import timedelta, timezone


NAMESPACE = uuid.UUID("a4e7d6d2-44e1-4c84-9a21-6c80bb2a7e04")


DEFECT_TYPES = [
    "DIMENSIONAL_ERROR",
    "SURFACE_DEFECT",
    "MATERIAL_DEFECT",
    "ASSEMBLY_ERROR"
]


class QualityGenerator:

    def __init__(self, seed=42):
        self.random = random.Random(seed)

    def generate(self, production_records):

        records = []

        for production in production_records:

            sample_size = self.random.choice(
                [20, 30, 50, 100]
            )

            defect_count = self.random.randint(
                0,
                min(8, sample_size)
            )

            # Symulacja kontroli jakości.
            result = (
                "FAIL"
                if defect_count >= 5
                else "PASS"
            )

            defect_type = (
                self.random.choice(DEFECT_TYPES)
                if defect_count > 0
                else None
            )

            # Kontrola wykonywana po zakończeniu produkcji.
            inspected_at = (
                production["completed_at"]
                + timedelta(minutes=self.random.randint(5, 60))
            )

            event_key = (
                f"{production['production_id']}:"
                f"{inspected_at.isoformat()}"
            )

            records.append({
                "source_event_id": str(
                    uuid.uuid5(NAMESPACE, event_key)
                ),
                "production_id": production["production_id"],
                "inspected_at": inspected_at,
                "sample_size": sample_size,
                "defect_count": defect_count,
                "defect_type": defect_type,
                "result": result
            })

        return records
