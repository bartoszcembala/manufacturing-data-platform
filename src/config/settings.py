import os
from dotenv import load_dotenv

load_dotenv()

def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}"
        )

    return value

DB_CONFIG = {
    "host": get_required_env("POSTGRES_HOST"),
    "port": int(get_required_env("POSTGRES_PORT")),
    "dbname": get_required_env("POSTGRES_DB"),
    "user": get_required_env("POSTGRES_USER"),
    "password": get_required_env("POSTGRES_PASSWORD"),
}
