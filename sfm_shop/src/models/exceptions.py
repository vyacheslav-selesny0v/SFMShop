class SFMShopException(Exception):
    """Базовый класс проекта"""
    pass

class ValidationError(SFMShopException):
    """Для ошибок валидации"""
    pass

class BusinessLogicError(SFMShopException):
    """Для ошибок бизнес-логики"""
    pass

class DatabaseError(SFMShopException):
    """Дя ошибок базы данных"""
    pass

class NegativePriceError(ValidationError):
    """Цена не может быть отрицательной"""
    pass

class InsufficientStockError(BusinessLogicError):
    """Недостаточно товара"""
    pass

class InvalidOrderError(BusinessLogicError):
    """Невалидный заказ"""
    pass