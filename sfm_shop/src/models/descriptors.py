from sfm_shop.src.models.exceptions import ValidationError


class PositiveNumber:
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name)
    
    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise ValidationError(f"{self.public_name} должно быть числом")
        if value < 0:
            raise ValidationError(f"{self.public_name} не может быть отрицательным")
        setattr(instance, self.private_name, value)


class CachedProperty:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        value = self.func(instance)
        instance.__dict__[self.func.__name__] = value

        return value

    