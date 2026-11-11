
-- ==========================================
-- MANUFACTURING DATA PLATFORM
-- DATABASE SCHEMA V1.0
-- ==========================================

-- 1. PRODUCTION LINES

CREATE TABLE IF NOT EXISTS production_lines (
    line_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    line_code VARCHAR(20) NOT NULL UNIQUE,

    line_name VARCHAR(100) NOT NULL,

    location VARCHAR(100) NOT NULL,

    description TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- 2. MACHINES

CREATE TABLE IF NOT EXISTS machines (
    machine_id VARCHAR(20) PRIMARY KEY,

    machine_name VARCHAR(100) NOT NULL,

    machine_type VARCHAR(50) NOT NULL,

    line_id INTEGER NOT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',

    installation_date DATE,

    manufacturer VARCHAR(100),

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_machine_line
        FOREIGN KEY (line_id)
        REFERENCES production_lines(line_id),

    CONSTRAINT chk_machine_status
        CHECK (status IN ('ACTIVE', 'INACTIVE', 'MAINTENANCE'))
);


-- 3. PRODUCTS

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(20) PRIMARY KEY,

    sku VARCHAR(50) NOT NULL UNIQUE,

    product_name VARCHAR(100) NOT NULL,

    product_category VARCHAR(50) NOT NULL,

    ideal_cycle_time_seconds NUMERIC(10, 3) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_cycle_time
        CHECK (ideal_cycle_time_seconds > 0)
);


-- 4. SHIFTS

CREATE TABLE IF NOT EXISTS shifts (
    shift_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    shift_name VARCHAR(50) NOT NULL UNIQUE,

    start_time TIME NOT NULL,

    end_time TIME NOT NULL,

    description TEXT,

    CONSTRAINT chk_shift_times
        CHECK (start_time <> end_time)
);


-- 5. OPERATORS

CREATE TABLE IF NOT EXISTS operators (
    operator_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    employee_code VARCHAR(30) NOT NULL UNIQUE,

    first_name VARCHAR(100) NOT NULL,

    last_name VARCHAR(100) NOT NULL,

    email VARCHAR(255) UNIQUE,

    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',

    hire_date DATE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_operator_status
        CHECK (status IN ('ACTIVE', 'INACTIVE'))
);


-- ==========================================
-- INDEXES
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_machines_line_id
    ON machines(line_id);

CREATE INDEX IF NOT EXISTS idx_machines_status
    ON machines(status);

CREATE INDEX IF NOT EXISTS idx_products_category
    ON products(product_category);

CREATE INDEX IF NOT EXISTS idx_operators_status
    ON operators(status);


-- ==========================================
-- END OF SCHEMA
-- ==========================================
