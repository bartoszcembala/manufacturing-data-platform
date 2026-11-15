
from psycopg.rows import dict_row


def fetch_reference_data(conn):

    queries = {
        "machines": """
            SELECT machine_id
            FROM machines
            WHERE status = 'ACTIVE'
            ORDER BY machine_id;
        """,

        "products": """
            SELECT product_id
            FROM products
            ORDER BY product_id;
        """,

        "shifts": """
            SELECT shift_id, start_time, end_time
            FROM shifts
            ORDER BY shift_id;
        """,

        "operators": """
            SELECT operator_id
            FROM operators
            WHERE status = 'ACTIVE'
            ORDER BY operator_id;
        """
    }

    result = {}

    with conn.cursor(row_factory=dict_row) as cursor:

        for name, query in queries.items():
            cursor.execute(query)
            result[name] = cursor.fetchall()

    return result
