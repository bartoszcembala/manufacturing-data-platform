
from src.database.connection import get_connection


def get_all_machines():

    query = """
        SELECT
            m.machine_id,
            m.machine_name,
            m.machine_type,
            m.status,
            l.line_name

        FROM machines m

        JOIN production_lines l
            ON m.line_id = l.line_id

        ORDER BY m.machine_id;
    """

    with get_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute(query)

            rows = cursor.fetchall()

            for row in rows:

                print({
                    "machine_id": row[0],
                    "machine_name": row[1],
                    "machine_type": row[2],
                    "status": row[3],
                    "line_name": row[4]
                })


if __name__ == "__main__":
    get_all_machines()
