
import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """
    Creates a PostgreSQL database connection.
    """

    connection = psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        connect_timeout=5
    )

    return connection
