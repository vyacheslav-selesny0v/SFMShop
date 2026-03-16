import time
from sfm_shop.src.models.product import Product
from sfm_shop.src.models.order import Order

def calculate_discount(price, discount_rate):
    return price * discount_rate


def calculate_delivery(weight, base_cost=100):
    return base_cost + weight * 10


def calculate_final_price(price, discount_rate, delivery):
    discount_amount = calculate_discount(price, discount_rate)
    return price - discount_amount + delivery


def calculate_total_orders(orders):
    return sum(order.total for order in orders)


def sort_orders_by_date(orders):
    return sorted(orders, key=lambda x: x.created_at)


def create_test_products(count):
    return [Product(i, f"Товар {i}", i * 100, 100) for i in range(count)]


def create_test_orders(count):

    from datetime import datetime, timedelta
    base_date = datetime(2024, 1, 1)
    return [
        Order(i, [i % 10], i, 1000 + i * 100, base_date + timedelta(days=i % 365))
        for i in range(count)
    ]


def find_product_in_list(products, product_id):
    
    for product in products:
        if product.id == product_id:
            return product
    return None


def find_product_in_dict(products_index, product_id):
    return products_index.get(product_id)


def create_products_catalog(products):
    return {product.id: product for product in products}