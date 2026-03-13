from SFMShop.src.models import NegativePriceError, InsufficientStockError


class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        try:
            if price < 0:
                raise NegativePriceError('Цена не может быть отрицательной')
            self.price = price
        except NegativePriceError as e:
            print(f'Ошибка при создании товара: {e}')
            self.price = 0
        
        try:
            if quantity < 0:
                raise ValueError('Количество не может быть отрицательным')
            self.quantity = quantity
        except ValueError as e:
            print(f'Ошибка при создании товара: {e}')
            self.quantity = 0


    def apply_discount(self):
        """Расчет скидки"""
        pass


    def sell(self, amount):
        if self.quantity < amount:
            raise InsufficientStockError(
                f"Товара недостаточно. На складе: {self.quantity}, требуется: {amount}"
            )
        self.quantity = self.quantity - amount
    
    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f'Товар: {self.name}, Цена: {self.price} руб.'

    def __repr__(self):
        return f'Product("{self.name}", {self.price}, {self.quantity})'
    
    def __lt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price
    
    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.name == other.name and self.price == other.price

    def check_stock(self):
        return self.quantity

    def update_stock(self, amount):
        new_quantity = self.quantity + amount
        if new_quantity < 0:
            raise InsufficientStockError("Результат обновления остатков не может быть отрицательным")
        self.quantity = new_quantity

    def set_price(self, price):
        if price < 0:
            raise NegativePriceError("Цена не может быть отрицательной")
        self.price = price