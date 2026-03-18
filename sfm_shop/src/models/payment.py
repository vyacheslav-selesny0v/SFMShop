class Payment:
    def __init__(self, amount):
        self.amount = amount
    
    def process_payment(self):
        print("Payment.process_payment()")


class Loggable:
    def log(self):
        print("Loggable.log()")
    

class CardPayment(Payment, Loggable):
    def __init__(self, amount, card_number):
        super().__init__(amount)
        self.__card_number = card_number
    
    def process_payment(self):
        self.log()
        super().process_payment()
        masked_card = "**** " + self.__card_number[-4:]
        return f"Оплата картой {masked_card}: {self.amount} руб."

class PayPalPayment(Payment):
    def __init__(self, amount, email):
        super().__init__(amount)
        self.email = email
    
    def process_payment(self):
        return "Оплата PayPal ({self._email}): {self.amount} руб."