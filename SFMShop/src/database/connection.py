import psycopg2
from psycopg2 import Error


def connect_to_db():
    """Подключение к базе данных PostgreSQL"""
    try:
        return psycopg2.connect(
            host='localhost',
            database='sfmshop',
            user='postgres',
            password=''
        )
    except Error as e:
        print(f'❌ Ошибка подключения: {e}')
        exit()   


def create_user_db(conn, name, email):
    """Создание пользователя"""
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)',
        (name, email)
        )
        conn.commit()
        cursor.close()
        print(f'Пользователь создан: {name}, {email}')
    except Error as e:
        conn.rollback()
        print(f'❌ Ошибка при создании пользователя: {e}')


def add_product(conn, name, price, quantity):
    """Добавить товар в базу данных"""
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)',
            (name, price, quantity)
        )
        conn.commit()
        cursor.close()
        print(f'Товар добавлен: {name}, {price}, {quantity}')
    except Error as e:
        conn.rollback()
        print(f'❌ Ошибка добавления товара "{name}": {e}')


def get_all_products(conn):
    """Получить все товары из базы данных"""
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        cursor.close()
        return products
    except Error as e:
        conn.rollback()
        print(f'❌ Ошибка при получении списка товаров: {e}')
        return []


def get_product_by_id(conn, product_id):
    """Получение товара"""
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, price, quantity FROM products WHERE id = %s', (product_id,))
        product = cursor.fetchone()
        cursor.close()
        if product:
            return {'id': product[0], 'name': product[1], 'price': product[2], 'quantity': product[3]}
        return None
    except Error as e:
        conn.rollback()
        print(f'❌ Ошибка при получении товара: {e}')
        return None


def update_product_price(conn, product_id, new_price):
    """Обновить цену товара"""
    try:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE products SET price = %s WHERE id = %s',
            (new_price, product_id)
        )
        conn.commit()
        cursor.close()
        print(f'Цена обновлена: {new_price}')
    except Error as e:
        conn.rollback()
        print(f'❌ Ошибка при обновлении цены товара: {e}')


def update_product_quantity(conn, product_id, new_quantity):
    """Обновить количество товара на складе"""
    try:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE products SET quantity = %s WHERE id = %s',
            (new_quantity, product_id)
        )
        conn.commit()
        cursor.close()
    except Exception as e:
        conn.rollback()
        print(f'❌ Ошибка при обновлении количества товара: {e}')


def get_all_users(conn):
    """Получение всех пользователей"""
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT *  FROM users')
        users = cursor.fetchall()
        cursor.close()
        return users
    except Error as e:
        conn.rollback()
        print(f'❌ Ошибка при получении списка пользователей: {e}')
        return []


def get_user_by_id(conn, user_id):
    """Получение пользователя"""
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return {'id': user[0], 'name': user[1], 'email': user[2]}
        return None
    except Error as e:
        conn.rollback()
        print(f'❌ Ошибка при получении пользователя: {e}')
        return None


def create_order_db(conn, user_id, total):
    """Создание заказа"""
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO orders (user_id, total) VALUES (%s, %s) RETURNING id', 
        (user_id, total)
        )

        result = cursor.fetchone() 
        order_id = result[0] if result else None

        conn.commit()
        cursor.close()
        return order_id
    except Error as e:
        conn.rollback()
        print(f'❌ Ошибка при создании заказа: {e}')
        return None


def get_user_orders(conn, user_id):
    """Получение заказов пользователя"""
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE user_id = %s', (user_id,))
        orders = cursor.fetchall()
        cursor.close()
        return orders
    except Error as e:
        conn.rollback()
        print(f'❌ Ошибка при получении заказов пользователя: {e}')
        return []


def delete_order(conn, order_id):
    """Удаленные заказы"""
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM orders WHERE id = %s', (order_id,))
        deleted_rows = cursor.rowcount
        conn.commit()
        cursor.close()
        return deleted_rows
    except Error as e:
        conn.rollback()
        print(f'❌ Ошибка при удалении заказа: {e}')
        return 0
    

def delete_product_db(conn, product_id):
    """Удаление товара"""
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE id = %s', (product_id))
        deleted_rows = cursor.rowcount
        conn.commit()
        cursor.close()
        return deleted_rows
    except Error as e:
        conn.rollback()
        print(f'❌ Ошибка при удалении товара: {e}')
        return 0
