from abc import ABC, abstractmethod



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
    

class OrderCalculator:
    @staticmethod
    def calculate_total(order) -> float:
        total = 0
        for product in order.products:
            total += product.calculate_total_value()
        return total
    
    @staticmethod
    def calculate_discount(total: float, discount_rate: float) -> float:
        return total * discount_rate
    
    @staticmethod
    def calculate_final_total(total: float, discount: float) -> float:
        return total - discount