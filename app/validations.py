
from datetime import datetime

def validate_date(date_str):
    try:
        # Пытаемся преобразовать строку в объект datetime
        datetime.strptime(date_str, "%d.%m.%Y")
        # Проверяем, что дата не в прошлом
        now = datetime.now()
 
        parsed_date = datetime.strptime(date_str, "%d.%m.%Y")
        if parsed_date <= now:
            return False
        return True
    except ValueError:
        # Если возникает ошибка ValueError, значит формат даты неверный
        return False
    
def validate_integer(input_value):
    try:
        # Пытаемся преобразовать введенное значение в целое число
        int_value = int(input_value)
        # Если преобразование прошло успешно, возвращаем True
        if int_value>=21:
            return False
        return True
    except ValueError:
        # Если преобразование вызвало ошибку (например, если введенная строка не является числом),
        # возвращаем False
        return False

def validate_price(input_value):
    try:
        # Пытаемся преобразовать введенное значение в целое число
        int_value = int(input_value)
        # Если преобразование прошло успешно, возвращаем True
        
        return True
    except ValueError:
        # Если преобразование вызвало ошибку (например, если введенная строка не является числом),
        # возвращаем False
        return False