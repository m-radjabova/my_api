import psycopg2
from dotenv import load_dotenv
import os

from psycopg2.extras import RealDictCursor

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        cursor_factory=RealDictCursor
    )
    return conn