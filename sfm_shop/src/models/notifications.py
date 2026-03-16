from abc import ABC, abstractmethod


class Notification(ABC):

    @abstractmethod
    def send(self, message: str):
        pass


class EmailNotification(Notification):
    def __init__(self, email: str):
        self.email = email


    def send(self, message: str):
        print(f'Отправка email на {self.email}: {message}')


class SMSNotification(Notification):
    def __init__(self, phone: str):
        self.phone = phone


    def send(self, message: str):
        print(f'Отправка sms на {self.phone}: {message}')


def send_notification(notifications: list[Notification], message: str):
    for notification in notifications:
        notification.send(message)