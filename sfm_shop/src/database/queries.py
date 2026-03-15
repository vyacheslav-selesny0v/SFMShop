import psycopg2


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