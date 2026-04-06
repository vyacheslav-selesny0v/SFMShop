import os
import psycopg2
from psycopg2 import Error
from contextlib import contextmanager
from dotenv import load_dotenv


load_dotenv()


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "sfmshop"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD")
}


@contextmanager
def get_connection():
    """Контекстный менеджер для подключения к БД"""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
        conn.commit()
    except Error as e:
        if conn:
            conn.rollback()
        print(f"❌ Ошибка БД: {e}")
        raise
    finally:
        if conn:
            conn.close()


def create_order(user_id, product_id, quantity, total):
    """Создание заказа с атомарными операциями"""
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO orders (user_id, total) VALUES (%s, %s)', (user_id, total))
                cur.execute('UPDATE products SET quantity = quantity - %s WHERE id = %s', (quantity, product_id))
                cur.execute('SELECT quantity FROM products WHERE id = %s', (product_id,))
                result = cur.fecthone()
                if result[0] < 0:
                    raise ValueError("Недостаточно товара")
        except Exception as e:
            print(f"Ошибка при создание заказа: {e}")
            raise