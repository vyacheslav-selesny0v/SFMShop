import time
from functools import wraps
from sfm_shop.src.models.product import Product

def calculate_discount(price, discount_rate):
    return price * discount_rate


def calculate_delivery(weight, base_cost=100):
    return base_cost + weight * 10


def calculate_final_price(price, discount_rate, delivery):
    discount_amount = calculate_discount(price, discount_rate)
    return price - discount_amount + delivery


def calculate_total_orders(orders):
    return sum(
        product.get_total_price()
        for order in orders
        for product in order.products
    )


def benchmark_func(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f'Функция {func.__name__} выполнилась за {execution_time:.10f} секунд.')
        return result, execution_time
    return wrapper


@benchmark_func
def find_product_in_list(products, product_id):
    
    for product in products:
        if product.id == product_id:
            return product
    return None


@benchmark_func
def find_product_in_dict(products_dict, product_id):
    return products_dict.get(product_id)


products_list = [Product(i, f"Товар {i}", 100, 1) for i in range(10000)]
products_dict = {product.id: product for product in products_list}

target_id = 9999

res_list, time_list = find_product_in_list(products_list, target_id)
res_dict, time_dict = find_product_in_dict(products_dict, target_id)


speedup = time_list / time_dict

print("-" * 30)
print(f"Ускорение: поиск в словаре быстрее в {speedup:.2f} раз(а).")    