from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sfm_shop.src.database.connection import (
    connect_to_db,
    create_order_db,
    create_user_db,
    delete_product_db,
    get_all_products,
    get_all_users,
    get_product_by_id,
    get_user_by_id,
    update_product_price,
    update_product_quantity,
)
from sfm_shop.src.models.order import Order
from sfm_shop.src.models.product import Product
from sfm_shop.src.models.user import User


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class UserCreate(BaseModel):
    name: str
    email: str


app = FastAPI()


conn = None


@app.on_event("startup")
async def startup():
    global conn
    conn = connect_to_db()

@app.on_event("shutdown")
async def shutdown():
    if conn:
        conn.close()


def test_api():
    client = TestClient(app)
    
    # Тест GET /users
    response = client.get("/users")
    assert response.status_code == 200
    print("GET /users: OK")

    # Тест GET /users/{users_id}
    response = client.get("/users/1")
    assert response.status_code == 200
    print("GET /users/1: OK")
    
    # Тест POST /users
    response = client.post("/users", json={"name": "Тест Тестов", "email": "test@test.ru"})
    assert response.status_code == 201
    print("POST /users: OK")

    # Тест GET /products
    response = client.get("/products")
    assert response.status_code == 200
    print("GET /products: OK")
    
    # Тест GET /products/{id}
    response = client.get("/products/1")
    assert response.status_code == 200
    print("GET /products/1: OK")

    # Тест PUT /products/{product_id}
    res = client.put("/products/2", json={"price": 1600.0, "quantity": 45})
    assert res.status_code == 200
    print("PUT /products/2: OK")

    # Тест POST /orders
    response = client.post("/orders", json={"user_id": 1, "product_id": 2, "quantity": 1})
    assert response.status_code == 201
    print("POST /orders: OK")

    # Тест DELETE /products/{product_id}
    # Благодаря ON DELETE CASCADE в БД, это пройдет успешно
    res = client.delete("/products/5")
    assert res.status_code == 200
    print("DELETE /products/5: OK")


@app.get('/users')
def get_users(limit: int = 10, offset: int = 0):
    global conn
    try:
        users_data = get_all_users(conn)

        users = []
        for data in users_data:
            user = User(data[1], data[2])
            user.id = data[0]
            users.append(user.__dict__)

        total = len(users_data)
        paginated_users = users[offset:offset+limit]
        return {
            'total': total,
            'limit': limit,
            'offset': offset,
            'users': paginated_users
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get('/users/{users_id}')
def get_user(users_id: int):
    global conn
    try:
        data = get_user_by_id(conn, users_id)

        if data:
            user = User(data[1], data[2])
            user.id = data[0]
            return user.__dict__
        
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/products')
def get_products(limit: int = 10, offset: int = 0):
    global conn
    try:
        products_data = get_all_products(conn)

        products = []
        for data in products_data:
            product = Product(data[1], data[2], data[3])
            product.id = data[0]
            products.append(product.__dict__)

        total = len(products)
        paginated_products = products[offset:offset+limit]

        return {
            'total': total,
            'limit': limit,
            'offset': offset,
            'products': paginated_products
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/products/{product_id}')
def get_product(product_id: int):
    global conn
    try:
        data = get_product_by_id(conn, product_id)

        if data:
            product = Product(data['name'], data['price'], data['quantity'])
            product.id = data['id']
            return product.__dict__
        
        raise HTTPException(status_code=404, detail='Товар не найден')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/users', status_code=status.HTTP_201_CREATED)
def create_user_api(user: UserCreate):
    global conn
    try:
        new_user = create_user_db(conn, user.name, user.email)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/orders', status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):
    global conn
    try:
        product = get_product_by_id(conn, order.product_id)
        if not product:
            raise HTTPException(status_code=404, detail='Товар не найден')

        if product['quantity'] < order.quantity:
            raise HTTPException(status_code=400, detail='Недостаточно товара на складе')
        
        total_price = product['price'] * order.quantity

        order_id = create_order_db(conn, order.user_id, total_price)

        new_order_obj = OrderCreate(order.user_id, [order.product_id])

        new_order_obj.id = order_id
        new_order_obj.total_price = total_price
        new_order_obj.quantity = order.quantity

        new_stock = product['quantity'] - order.quantity
        update_product_quantity(conn, order.product_id, new_stock)

        return new_order_obj.__dict__
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.put('/products/{product_id}')
def update_product(product_id: int, product_data: dict):
    global conn
    try:
        product = get_product_by_id(conn, product_id)

        if not product:
            raise HTTPException(status_code=404, detail='Товар не найден')
        
        if 'price' in product_data:
            update_product_price(conn, product_id, product_data['price'])

        if 'quantity' in product_data:
            update_product_quantity(conn, product_id, product_data['quantity'])

        return {'id': product_id, 'message': 'Товар обновлен'}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    global conn
    try:
        product = get_product_by_id(conn, product_id)

        if not product:
            raise HTTPException(status_code=404, detail='Товар не найден')
        
        rows = delete_product_db(conn, product_id)

        if rows > 0:
            return {'id': product_id, 'message': 'Товар удален'}
        
        raise HTTPException(status_code=500, detail="Не удалось удалить товар")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    test_api()