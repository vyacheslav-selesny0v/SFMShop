from SFMShop.src.models import InvalidOrderError


class Order:
    def __init__(self, user, products, order_id, total):
        if not products:
            raise InvalidOrderError("Заказ невалиден: пустой список товаров")
        self.user = user
        self.products = products
        self.order_id = order_id
        self.total = total


    def add_product(self, product):
        try:
            if product not in self.products:
                raise KeyError('Товар не найден в списке')
        except KeyError as e:
            print(f'Ошибка при создании заказа: {e}')

    
    def calculate_total(self):
        total = 0
        for product in self.products:
            total = total + product.get_total_price()
        return total

    def __str__(self):
        return f'Заказ #{self.order_id} на сумму {self.total} руб. (Пользователь: {self.user})'