
CREATE TABLE machine_telemetry (
    telemetry_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_event_id UUID NOT NULL UNIQUE,
    machine_id VARCHAR(20) NOT NULL
        REFERENCES machines(machine_id),
    recorded_at TIMESTAMPTZ NOT NULL,
    temperature NUMERIC(8,2) NOT NULL,
    pressure NUMERIC(8,2) NOT NULL,
    speed NUMERIC(10,2) NOT NULL,
    energy_consumption NUMERIC(10,3) NOT NULL,

    CONSTRAINT chk_temperature
        CHECK (temperature BETWEEN -20 AND 200),

    CONSTRAINT chk_pressure
        CHECK (pressure >= 0),

    CONSTRAINT chk_speed
        CHECK (speed >= 0),

    CONSTRAINT chk_energy
        CHECK (energy_consumption >= 0)
);

CREATE TABLE production_records (
    production_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_event_id UUID NOT NULL UNIQUE,
    machine_id VARCHAR(20) NOT NULL
        REFERENCES machines(machine_id),
    product_id VARCHAR(20) NOT NULL
        REFERENCES products(product_id),
    shift_id INTEGER NOT NULL
        REFERENCES shifts(shift_id),
    operator_id INTEGER NOT NULL
        REFERENCES operators(operator_id),
    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ NOT NULL,
    quantity_total INTEGER NOT NULL,
    quantity_good INTEGER NOT NULL,
    quantity_scrap INTEGER NOT NULL,

    CONSTRAINT chk_production_time
        CHECK (completed_at > started_at),

    CONSTRAINT chk_quantities
        CHECK (
            quantity_total > 0
            AND quantity_good >= 0
            AND quantity_scrap >= 0
            AND quantity_total = quantity_good + quantity_scrap
        )
);

CREATE TABLE downtime_events (
    downtime_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_event_id UUID NOT NULL UNIQUE,
    machine_id VARCHAR(20) NOT NULL
        REFERENCES machines(machine_id),
    started_at TIMESTAMPTZ NOT NULL,
    ended_at TIMESTAMPTZ,
    reason_category VARCHAR(50) NOT NULL,
    description TEXT,
    is_planned BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT chk_downtime_time
        CHECK (ended_at IS NULL OR ended_at > started_at)
);

CREATE TABLE quality_inspections (
    inspection_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_event_id UUID NOT NULL UNIQUE,
    production_id BIGINT NOT NULL
        REFERENCES production_records(production_id),
    inspected_at TIMESTAMPTZ NOT NULL,
    sample_size INTEGER NOT NULL,
    defect_count INTEGER NOT NULL,
    defect_type VARCHAR(50),
    result VARCHAR(10) NOT NULL,

    CONSTRAINT chk_sample_size
        CHECK (sample_size > 0),

    CONSTRAINT chk_defect_count
        CHECK (defect_count BETWEEN 0 AND sample_size),

    CONSTRAINT chk_quality_result
        CHECK (result IN ('PASS', 'FAIL'))
);

CREATE INDEX idx_telemetry_machine_time
    ON machine_telemetry(machine_id, recorded_at);

CREATE INDEX idx_production_machine_time
    ON production_records(machine_id, started_at);

CREATE INDEX idx_downtime_machine_time
    ON downtime_events(machine_id, started_at);

CREATE INDEX idx_quality_production
    ON quality_inspections(production_id);
