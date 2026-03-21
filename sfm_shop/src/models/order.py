from datetime import datetime
from sfm_shop.src.models.exceptions import InvalidOrderError, ValidationError
from sfm_shop.src.models.mixins import LoggableMixin, ValidatableMixin, SerializableMixin
from sfm_shop.src.models.metaclasses import ModelMeta


class Order(LoggableMixin, ValidatableMixin, SerializableMixin, metaclass=ModelMeta):
    def __init__(self, user, products, order_id, total, created_at=None):
        self.user = user
        self.products = products
        self.order_id = order_id
        self.total = total
        self.created_at = created_at if created_at else datetime.now()
        OrderValidator.validate(self)
        self.log(f"Создан заказ: {order_id}, сумма: {total}")


    def add_product(self, product):
        if product not in self.products:
            self.products.append(product)
        else:
            print(f'Товар {product} уже есть в заказе')

    
    def __str__(self):
        return f'Заказ #{self.order_id} на сумму {self.total} руб. (Пользователь: {self.user})'


    def __eq__(self, other):
        if not isinstance(other, Order):
            return False
        return self.order_id == other.order_id
    

    def __lt__(self, other):
        if not isinstance(other, Order):
            return NotImplemented
        return self.created_at < other.created_at
    

class OrderCalculator:
    @staticmethod
    def calculate_total(order: Order) -> float:
        total = 0
        for product in order.products:
            total = total + product.get_total_price()
        return total


class OrderValidator:
    @staticmethod
    def validate(order: Order):
        if not order.user:
            raise ValidationError("Заказ должен иметь пользователя")
        if order.total < 0:
            raise ValidationError("Сумма заказа не может быть отрицательной")
        if not order.products:
            raise InvalidOrderError("Заказ невалиден: пустой список товаров")
        return True