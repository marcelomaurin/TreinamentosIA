import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "usuario"),
    "password": os.getenv("DB_PASSWORD", "senha"),
    "database": os.getenv("DB_NAME", "IAdb"),
}
