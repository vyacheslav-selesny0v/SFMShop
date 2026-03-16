class User:
    def __init__(self, name, email):
        self.name = name
        try:
            if '@' not in email:
                raise ValueError('Неверный формат email')
            self._email = email
        except ValueError as e:
            print(f'Ошибка при создании пользователя: {e}')
            self._email = ''
    
    def get_info(self):
        return "Пользователь: " + self.name + ", Email: " + self._email
