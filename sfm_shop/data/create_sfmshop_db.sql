DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Таблица пользователей
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

Таблица товаров
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Таблица заказов
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Таблица товаров в заказах
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- Тестовые данные: 3 пользователя
INSERT INTO users (name, email) VALUES 
('Иван Иванов', 'ivan@example.com'),
('Мария Петрова', 'maria@example.com'),
('Алексей Смирнов', 'alex@example.com');

-- Тестовые данные: 5 товаров
INSERT INTO products (name, price, quantity) VALUES 
('Ноутбук', 50000.00, 10),
('Мышь', 1500.00, 50),
('Клавиатура', 3000.00, 20),
('Монитор', 15000.00, 5),
('Коврик', 500.00, 100);

-- Тестовые данные: 2 заказа
INSERT INTO orders (user_id, total) VALUES 
(1, 51500.00),
(2, 3000.00);