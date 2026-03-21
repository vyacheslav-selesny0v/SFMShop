from dataclasses import dataclass
from sfm_shop.src.models.exceptions import NegativePriceError, InsufficientStockError, ValidationError
from sfm_shop.src.models.mixins import LoggableMixin, ValidatableMixin, SerializableMixin
from abc import ABC, abstractmethod
from sfm_shop.src.models.metaclasses import ModelMeta


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: float) -> float:
        pass


class PercentDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent
    def apply(self, price: float) -> float:
        return price * (1 - self.percent / 100)
    

class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        self.amount = amount
    def apply(self, price: float) -> float:
        return price - self.amount
    

@dataclass
class Product(LoggableMixin, ValidatableMixin, SerializableMixin, metaclass=ModelMeta):
    product_id: int
    name: str
    _price: float
    _quantity: int = 0
        

    def __post_init__(self):
        self.validate()
        self.log(f"Создан товар: {self.name}, цена: {self.price}")


    def validate(self):
        if self._price < 0:
            raise NegativePriceError("Цена не может быть отрицательной")
        if self._quantity < 0:
            raise ValidationError("Количество не может быть отрицательным")
        return True    


    @property
    def price(self):
        return self._price
    

    @price.setter
    def price(self, value):
        if value < 0:
            raise NegativePriceError("Цена не может быть отрицательной")
        self._price = value


    @property
    def quantity(self):
        return self._quantity
    

    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise ValidationError("Количество не может быть отрицательным")
        self._quantity = value


    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            product_id=data['product_id'],
            name=data['name'],
            _price=data['_price'],
            _quantity=data.get('_quantity', 0)
        )


    def calculate_price(self, discount: DiscountStrategy):
        return discount.apply(self.price)


    def sell(self, amount):
        if self.quantity < amount:
            raise InsufficientStockError(
                f"Товара недостаточно. На складе: {self.quantity}, требуется: {amount}"
            )
        self.quantity = self.quantity - amount
    

    def get_total_price(self):
        return self.price * self.quantity


    def __str__(self):
        return f'Товар: {self.name}, Цена: {self.price} руб., Количество: {self.quantity}'


    def __repr__(self):
        return f'Product("{self.name}", {self.price}, {self.quantity})'
    
    
    def __lt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self._price < other._price
    

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.name == other.name and self.price == other.price


    def update_stock(self, amount):
        new_quantity = self.quantity + amount
        if new_quantity < 0:
            raise InsufficientStockError("Результат обновления остатков не может быть отрицательным")
        self.quantity = new_quantity