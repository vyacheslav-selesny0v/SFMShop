class OrderValidator:
    @staticmethod
    def validate(order):
        if not order.items:
            raise ValueError("Заказ должен иметь пользователя")
        if order.user < 0:
            raise ValueError("Сумма заказа не может быть отрицательной")
        for item in order.items:
            if item.quantity <= 0:
                raise ValueError("Количество товара должно быть положительным")
        return True
    
    @staticmethod
    def validate_total(total: float) -> bool:
        if total < 0:
            raise ValueError("Сумма заказа не может быть отрицательной")
        return True