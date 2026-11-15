
import uuid
import random

from datetime import datetime, timedelta, timezone, date


NAMESPACE = uuid.UUID("a4e7d6d2-44e1-4c84-9a21-6c80bb2a7e02")


class ProductionGenerator:

    def __init__(
        self,
        machines,
        products,
        shifts,
        operators,
        seed=42
    ):
        self.machines = machines
        self.products = products
        self.shifts = shifts
        self.operators = operators
        self.random = random.Random(seed)

    def generate(self, days=30):

        today = datetime.now(timezone.utc).date()
        first_day = today - timedelta(days=days)

        records = []

        for day_offset in range(days):

            production_date = first_day + timedelta(
                days=day_offset
            )

            for machine in self.machines:

                for shift in self.shifts:

                    product = self.random.choice(self.products)
                    operator = self.random.choice(self.operators)

                    total = self.random.randint(300, 1500)

                    scrap = self.random.randint(
                        0,
                        max(1, int(total * 0.05))
                    )

                    good = total - scrap

                    start = datetime.combine(
                        production_date,
                        shift["start_time"],
                        tzinfo=timezone.utc
                    )

                    end = datetime.combine(
                        production_date,
                        shift["end_time"],
                        tzinfo=timezone.utc
                    )

                    # Obsługa zmiany przechodzącej przez północ.
                    if end <= start:
                        end += timedelta(days=1)

                    event_key = (
                        f"{machine['machine_id']}:"
                        f"{shift['shift_id']}:"
                        f"{production_date.isoformat()}"
                    )

                    records.append({
                        "source_event_id": str(
                            uuid.uuid5(NAMESPACE, event_key)
                        ),
                        "machine_id": machine["machine_id"],
                        "product_id": product["product_id"],
                        "shift_id": shift["shift_id"],
                        "operator_id": operator["operator_id"],
                        "started_at": start,
                        "completed_at": end,
                        "quantity_total": total,
                        "quantity_good": good,
                        "quantity_scrap": scrap
                    })

        return records
