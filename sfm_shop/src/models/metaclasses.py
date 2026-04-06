class ModelMeta(type):
    _registry = {}

    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(mcs, name, bases, attrs)
        if name != 'BaseModel':  # Не регистрируем базовый класс, если он есть
            mcs._registry[name] = new_class
        
        # Добавляем метод to_dict, если его нет
        if 'to_dict' not in attrs:
            def to_dict(self):
                return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
            new_class.to_dict = to_dict
        return new_class

    @classmethod
    def get_registry(mcs):
        return mcs._registry