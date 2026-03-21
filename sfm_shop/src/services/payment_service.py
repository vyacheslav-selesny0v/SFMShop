from sfm_shop.src.models.payment import Payment, PaymentMethod
from abc import ABC, abstractmethod


class PaymentValidator:
    @staticmethod
    def validate(payment: Payment) -> bool:
        if payment.amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        return True


class PaymentRepository(ABC):
    @abstractmethod
    def save(self, payment: Payment):
        pass


class PostgreSQLPaymentRepository(PaymentRepository):
    def save(self, payment: Payment):
        print(f"Сохранение платежа {payment.order_id} в PostgreSQL")


class NotificationService(ABC):
    @abstractmethod
    def send(self, payment: Payment):
        pass


class EmailNotificationService(NotificationService):
    def send(self, payment: Payment):
        print(f"Отправка email о платеже {payment.order_id}")


class PaymentProcessor:
    def __init__(self, payment_method: PaymentMethod, repository: PaymentRepository, notification_service: NotificationService):
        self.payment_method = payment_method
        self.repository = repository
        self.notification_service = notification_service

    def process_payment(self, payment: Payment) -> str:
            PaymentValidator.validate(payment)
            
            success = self.payment_method.process(payment.amount)
            
            if success:
                payment.status = "completed"
            else:
                payment.status = "failed"
                raise ValueError(f"Ошибка обработки платежа методом {type(self.payment_method).__name__}")
            
            self.repository.save(payment)
            
            self.notification_service.send(payment)
            
            return payment.status