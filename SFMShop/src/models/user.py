from SFMShop.src.models import ValidationError


class User:
    def __init__(self, name, email):
        self.name = name
        try:
            if '@' not in email:
                raise ValidationError('Неверный формат email')
            self.email = email
        except ValidationError as e:
            print(f'Ошибка при создании пользователя: {e}')
            self.email = ''
    
    def get_info(self):
        return "Пользователь: " + self.name + ", Email: " + self.email
