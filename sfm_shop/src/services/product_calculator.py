from abc import ABC, abstractmethod
from sfm_shop.src.models.product import Product


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


class ProductCalculator:
    @staticmethod
    def apply_discount(product: 'Product', discount: DiscountStrategy) -> float:
        return discount.apply(product.price)
    
    @staticmethod
    def calculate_total_value(product: 'Product'):
        return product.price * product.quantity