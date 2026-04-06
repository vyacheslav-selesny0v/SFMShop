from psycopg2.extensions import ISOLATION_LEVEL_REPEATABLE_READ
from psycopg2 import Error
from sfm_shop.src.database.connection import get_connection





def generate_sales_report(start_date):
    """Генерация отчета с правильным уровнем изоляции"""
    with get_connection() as conn:
        conn.set_session(isolation_level=ISOLATION_LEVEL_REPEATABLE_READ)
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COALESCE(SUM(total), 0), COUNT(*) FROM orders WHERE created_at >= %s", (start_date,))
                total, count = cur.fetchone()

                return {"total": total, "count": count}

        except Error as e:
            print(f"Ошибка при генерации отчета: {e}")
            raise


def create_order(user_id, product_id, quantity, total):
    """Создание заказа с атомарными операциями"""
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO orders (user_id, total) VALUES (%s, %s)', (user_id, total))
                order_id = cur.fetchone()[0]
                cur.execute('UPDATE products SET quantity = quantity - %s WHERE id = %s', (quantity, product_id))
                cur.execute('SELECT quantity FROM products WHERE id = %s', (product_id,))
                result = cur.fetchone()
                if result[0] < 0:
                    raise ValueError("Недостаточно товара")
                return order_id
        except Error as e:
            print(f"Ошибка при создание заказа: {e}")
            raise


def transfer_money(from_user_id, to_user_id, amount):
    """Функция перевода денег с использованием транзакций"""
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute('UPDATE users SET amount = amount - %s WHERE id = %s AND amount >= %s', (amount, from_user_id, amount))
                if cur.rowcount == 0:
                    raise ("Недостаточно средств или отправитель не найден")
                cur.execute('UPDATE users SET amount = amount + %s WHERE id = %s', (amount, to_user_id))
                cur.execute('SELECT balance FROM users WHERE id = %s', (from_user_id))
                row = cur.fetchone()
                if row is None:
                    raise ValueError(f"Пользователь {from_user_id} не найден")
                if row[0] < 0:
                    raise ValueError("Отрицательный баланс пользователя: {from_user_id}: {row[0]}")
                return True
        except Error as e:
            print(f"Ошибка при переводе денег: {e}")
            raise


def get_user_order_history(conn, user_id):
    """Получить заказы пользователя с товарами"""
    cursor = conn.cursor()
    query = '''
        SELECT 
            orders.id, 
            products.name, 
            order_items.quantity, 
            order_items.price 
        FROM orders
        JOIN order_items ON orders.id = order_items.order_id
        JOIN products ON order_items.product_id = products.id
        WHERE orders.user_id = %s
        ORDER BY orders.created_at DESC
    '''
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()
    cursor.close()
    return results


def get_order_statistics(conn):
    """Статистика: заказы и суммы по пользователям"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_id, COUNT(*) as order_count, SUM(total) as total_sum 
        FROM orders 
        GROUP BY user_id
        ORDER BY total_sum DESC
    ''')
    results = cursor.fetchall()
    cursor.close()
    return results


def get_top_products(conn, limit=5):
    """Топ товаров по количеству проданных единиц"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT products.name, SUM(order_items.quantity) AS total_count
        FROM products 
        JOIN order_items ON products.id = order_items.product_id
        GROUP BY products.id, products.name
        ORDER BY total_count DESC
        LIMIT %s
    ''', (limit,))
    results = cursor.fetchall()
    cursor.close()
    return results