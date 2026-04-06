from datetime import datetime
from sfm_shop.src.models.mixins import LoggableMixin, SerializableMixin
from sfm_shop.src.services.order_validator import OrderValidator
from sfm_shop.src.models.descriptors import PositiveNumber


class Order(LoggableMixin, SerializableMixin):
    order_id = PositiveNumber()

    def __init__(self, user, products, order_id, total, created_at=None):
        self.user = user
        self.products = products
        self.order_id = order_id
        self.total = total
        self.created_at = created_at if created_at else datetime.now()
        OrderValidator.validate(self)
        self.log(f"Создан заказ: {order_id}, сумма: {total}")


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