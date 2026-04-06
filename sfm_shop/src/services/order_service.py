from sfm_shop.src.models.product import Product
from sfm_shop.src.models.order import Order


class OrderService:

    def add_product(product: Product, order: Order):
        if product not in order.products:
            order.products.append(product)
        else:
            print(f'Товар {product} уже есть в заказе')