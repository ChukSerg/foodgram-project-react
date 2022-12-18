from django.core.validators import RegexValidator


class WordNameValidator(RegexValidator):
    regex = r'^[а-яА-ЯёЁa-zA-Z0-9 -]+$'
    message = (
        'Введите правильное имя. Оно должно включать только буквы, '
        'цифры, пробел и дефис.'
    )
    flags = 0
