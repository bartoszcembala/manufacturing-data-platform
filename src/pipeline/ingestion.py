
def load_telemetry(conn, records):

    query = """
        INSERT INTO machine_telemetry (
            source_event_id,
            machine_id,
            recorded_at,
            temperature,
            pressure,
            speed,
            energy_consumption
        )
        VALUES (
            %(source_event_id)s,
            %(machine_id)s,
            %(recorded_at)s,
            %(temperature)s,
            %(pressure)s,
            %(speed)s,
            %(energy_consumption)s
        )
        ON CONFLICT (source_event_id) DO NOTHING;
    """

    with conn.cursor() as cursor:
        cursor.executemany(query, records)

    conn.commit()


def load_production(conn, records):

    query = """
        INSERT INTO production_records (
            source_event_id,
            machine_id,
            product_id,
            shift_id,
            operator_id,
            started_at,
            completed_at,
            quantity_total,
            quantity_good,
            quantity_scrap
        )
        VALUES (
            %(source_event_id)s,
            %(machine_id)s,
            %(product_id)s,
            %(shift_id)s,
            %(operator_id)s,
            %(started_at)s,
            %(completed_at)s,
            %(quantity_total)s,
            %(quantity_good)s,
            %(quantity_scrap)s
        )
        ON CONFLICT (source_event_id) DO NOTHING;
    """

    with conn.cursor() as cursor:
        cursor.executemany(query, records)

    conn.commit()


def load_downtime(conn, records):

    query = """
        INSERT INTO downtime_events (
            source_event_id,
            machine_id,
            started_at,
            ended_at,
            reason_category,
            description,
            is_planned
        )
        VALUES (
            %(source_event_id)s,
            %(machine_id)s,
            %(started_at)s,
            %(ended_at)s,
            %(reason_category)s,
            %(description)s,
            %(is_planned)s
        )
        ON CONFLICT (source_event_id) DO NOTHING;
    """

    with conn.cursor() as cursor:
        cursor.executemany(query, records)

    conn.commit()


def load_quality(conn, records):

    query = """
        INSERT INTO quality_inspections (
            source_event_id,
            production_id,
            inspected_at,
            sample_size,
            defect_count,
            defect_type,
            result
        )
        VALUES (
            %(source_event_id)s,
            %(production_id)s,
            %(inspected_at)s,
            %(sample_size)s,
            %(defect_count)s,
            %(defect_type)s,
            %(result)s
        )
        ON CONFLICT (source_event_id) DO NOTHING;
    """

    with conn.cursor() as cursor:
        cursor.executemany(query, records)

    conn.commit()


def get_production_records(conn, start_date):

    query = """
        SELECT
            production_id,
            source_event_id,
            machine_id,
            product_id,
            shift_id,
            operator_id,
            started_at,
            completed_at,
            quantity_total,
            quantity_good,
            quantity_scrap
        FROM production_records
        WHERE started_at >= %s
        ORDER BY started_at;
    """

    with conn.cursor() as cursor:
        cursor.execute(query, (start_date,))
        columns = [col.name for col in cursor.description]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
