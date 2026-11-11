
-- ==========================================
-- SEED DATA
-- ==========================================

-- PRODUCTION LINES

INSERT INTO production_lines (
    line_code,
    line_name,
    location,
    description
)
VALUES
(
    'LINE-01',
    'CNC Production',
    'Factory Hall A',
    'CNC machining production line'
),
(
    'LINE-02',
    'Pressing',
    'Factory Hall B',
    'Industrial pressing line'
),
(
    'LINE-03',
    'Assembly',
    'Factory Hall C',
    'Component assembly line'
)
ON CONFLICT (line_code) DO NOTHING;


-- MACHINES

INSERT INTO machines (
    machine_id,
    machine_name,
    machine_type,
    line_id,
    status,
    installation_date,
    manufacturer
)
VALUES
('M001', 'CNC-01', 'CNC', 1, 'ACTIVE', '2022-01-15', 'DMG MORI'),
('M002', 'CNC-02', 'CNC', 1, 'ACTIVE', '2022-03-20', 'DMG MORI'),
('M003', 'CNC-03', 'CNC', 1, 'MAINTENANCE', '2021-06-10', 'Mazak'),

('M004', 'PRESS-01', 'PRESS', 2, 'ACTIVE', '2020-02-10', 'Schuler'),
('M005', 'PRESS-02', 'PRESS', 2, 'ACTIVE', '2021-04-18', 'Schuler'),
('M006', 'PRESS-03', 'PRESS', 2, 'INACTIVE', '2019-09-12', 'Schuler'),

('M007', 'ROBOT-01', 'ROBOT', 3, 'ACTIVE', '2023-01-05', 'ABB'),
('M008', 'ROBOT-02', 'ROBOT', 3, 'ACTIVE', '2023-05-12', 'ABB'),
('M009', 'ASSEMBLY-01', 'ASSEMBLY', 3, 'ACTIVE', '2022-08-01', 'KUKA'),
('M010', 'ASSEMBLY-02', 'ASSEMBLY', 3, 'ACTIVE', '2022-10-20', 'KUKA')
ON CONFLICT (machine_id) DO NOTHING;


-- PRODUCTS

INSERT INTO products (
    product_id,
    sku,
    product_name,
    product_category,
    ideal_cycle_time_seconds
)
VALUES
('P001', 'BRK-001', 'Brake Component A', 'BRAKE', 4.500),
('P002', 'BRK-002', 'Brake Component B', 'BRAKE', 5.200),
('P003', 'ENG-001', 'Engine Component A', 'ENGINE', 6.100),
('P004', 'ENG-002', 'Engine Component B', 'ENGINE', 7.300),
('P005', 'ASM-001', 'Assembly Component A', 'ASSEMBLY', 8.000)
ON CONFLICT (product_id) DO NOTHING;


-- SHIFTS

INSERT INTO shifts (
    shift_name,
    start_time,
    end_time,
    description
)
VALUES
('Morning', '06:00', '14:00', 'Morning production shift'),
('Afternoon', '14:00', '22:00', 'Afternoon production shift'),
('Night', '22:00', '06:00', 'Night production shift')
ON CONFLICT (shift_name) DO NOTHING;


-- OPERATORS

INSERT INTO operators (
    employee_code,
    first_name,
    last_name,
    email,
    status,
    hire_date
)
VALUES
('EMP001', 'John', 'Smith', 'john.smith@example.com', 'ACTIVE', '2021-02-10'),
('EMP002', 'Anna', 'Brown', 'anna.brown@example.com', 'ACTIVE', '2022-05-15'),
('EMP003', 'Michael', 'Wilson', 'michael.wilson@example.com', 'ACTIVE', '2020-11-20'),
('EMP004', 'Sarah', 'Taylor', 'sarah.taylor@example.com', 'ACTIVE', '2023-01-10'),
('EMP005', 'David', 'Miller', 'david.miller@example.com', 'INACTIVE', '2019-07-05')
ON CONFLICT (employee_code) DO NOTHING;


-- ==========================================
-- END OF SEED DATA
-- ==========================================
