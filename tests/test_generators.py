from src.generators.telemetry import TelemetryGenerator


def test_telemetry_generator_returns_records():

    machines = [
        {"machine_id": "M001"},
        {"machine_id": "M002"}
    ]

    generator = TelemetryGenerator(machines, seed=42)

    records = generator.generate(
        days=1,
        interval_minutes=60
    )

    assert len(records) > 0

    for record in records:
        assert record["machine_id"] in ["M001", "M002"]
        assert record["temperature"] > -20
        assert record["pressure"] >= 0
        assert record["speed"] >= 0
        assert record["energy_consumption"] >= 0