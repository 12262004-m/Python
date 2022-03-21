class IncorrectDataError(Exception):
    def __str__(self):
        return 'Получены некорректные данные'

class DictInputError(Exception):
    def __str__(self):
        return 'Аргумент функции должен быть словарём'

class MissingFieldError(Exception):
    def __init__(self, missing_field):
        self.missing_field = missing_field
    def __str__(self):
        return f'В принятом словаре отсутствует обязательное поле {self.missing_field}'