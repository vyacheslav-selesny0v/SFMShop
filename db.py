import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="sfmshop",
    user="postgres",
    password="password"
)

# Создание курсора
cursor = conn.cursor()

# Выполнение запроса
cursor.execute("SELECT * FROM products")

# Получение результатов
results = cursor.fetchall()

# Закрытие курсора и соединения
cursor.close()
conn.close()