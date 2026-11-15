
import logging

from datetime import datetime, timedelta, timezone

from src.database.connection import get_connection
from src.database.repositories import fetch_reference_data

from src.generators.telemetry import TelemetryGenerator
from src.generators.production import ProductionGenerator
from src.generators.downtime import DowntimeGenerator
from src.generators.quality import QualityGenerator

from src.pipeline.ingestion import (
    load_telemetry,
    load_production,
    load_downtime,
    load_quality,
    get_production_records
)


# -------------------------
# LOGGING
# -------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# -------------------------
# PIPELINE
# -------------------------

def run_pipeline(days=30):

    logger.info("Starting Manufacturing Data Pipeline")

    pipeline_start = datetime.now(timezone.utc)

    with get_connection() as conn:

        # 1. Reference data

        logger.info("Loading reference data")

        reference = fetch_reference_data(conn)

        machines = reference["machines"]
        products = reference["products"]
        shifts = reference["shifts"]
        operators = reference["operators"]

        logger.info(
            "Loaded %s machines, %s products, %s shifts, %s operators",
            len(machines),
            len(products),
            len(shifts),
            len(operators)
        )

        if not all([machines, products, shifts, operators]):
            raise RuntimeError(
                "Missing reference data. Check Sprint 1 seed data."
            )

        # 2. Telemetry

        logger.info("Generating telemetry")

        telemetry_generator = TelemetryGenerator(
            machines=machines,
            seed=42
        )

        telemetry_records = telemetry_generator.generate(
            days=days,
            interval_minutes=15
        )

        logger.info(
            "Generated %s telemetry records",
            len(telemetry_records)
        )

        load_telemetry(conn, telemetry_records)

        logger.info("Telemetry ingestion completed")

        # 3. Production

        logger.info("Generating production records")

        production_generator = ProductionGenerator(
            machines=machines,
            products=products,
            shifts=shifts,
            operators=operators,
            seed=42
        )

        production_records = production_generator.generate(
            days=days
        )

        logger.info(
            "Generated %s production records",
            len(production_records)
        )

        load_production(conn, production_records)

        logger.info("Production ingestion completed")

        # 4. Downtime

        logger.info("Generating downtime events")

        downtime_generator = DowntimeGenerator(
            machines=machines,
            seed=42
        )

        downtime_records = downtime_generator.generate(
            days=days,
            events_per_day=4
        )

        logger.info(
            "Generated %s downtime events",
            len(downtime_records)
        )

        load_downtime(conn, downtime_records)

        logger.info("Downtime ingestion completed")

        # 5. Quality

        logger.info("Fetching saved production records")

        start_date = datetime.now(
            timezone.utc
        ) - timedelta(days=days + 1)

        saved_production = get_production_records(
            conn,
            start_date
        )

        logger.info(
            "Found %s production records for quality inspection",
            len(saved_production)
        )

        quality_generator = QualityGenerator(seed=42)

        quality_records = quality_generator.generate(
            saved_production
        )

        logger.info(
            "Generated %s quality inspections",
            len(quality_records)
        )

        load_quality(conn, quality_records)

        logger.info("Quality ingestion completed")

        # 6. Summary

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT
                    (SELECT COUNT(*) FROM machine_telemetry),
                    (SELECT COUNT(*) FROM production_records),
                    (SELECT COUNT(*) FROM downtime_events),
                    (SELECT COUNT(*) FROM quality_inspections);
            """)

            counts = cursor.fetchone()

    elapsed = (
        datetime.now(timezone.utc) - pipeline_start
    ).total_seconds()

    logger.info("=" * 50)
    logger.info("PIPELINE COMPLETED SUCCESSFULLY")
    logger.info("Telemetry records: %s", counts[0])
    logger.info("Production records: %s", counts[1])
    logger.info("Downtime events: %s", counts[2])
    logger.info("Quality inspections: %s", counts[3])
    logger.info("Execution time: %.2f seconds", elapsed)
    logger.info("=" * 50)


if __name__ == "__main__":

    try:
        run_pipeline(days=30)

    except Exception:
        logger.exception("Pipeline execution failed")
        raise
