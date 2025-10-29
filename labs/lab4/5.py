# Спрашиваем пароль у пользователя
password = input("Введите пароль: ")

# Список ошибок — сюда будем добавлять, чего не хватает
errors = []

# Проверка 1: длина не менее 8 символов
if len(password) < 8:
    errors.append("слишком короткий (менее 8 символов)")

# Флаги для проверки содержимого
has_upper = False
has_lower = False
has_digit = False
has_special = False

# Проверяем каждый символ в пароле
for char in password:
    if char.isupper() and char.isalpha():
        has_upper = True
    elif char.islower() and char.isalpha():
        has_lower = True
    elif char.isdigit():
        has_digit = True
    else:
        # Любой символ, который не буква и не цифра — считаем спецсимволом
        has_special = True

# Проверка 2–5: наличие нужных типов символов
if not has_upper:
    errors.append("отсутствуют заглавные буквы")
if not has_lower:
    errors.append("отсутствуют строчные буквы")
if not has_digit:
    errors.append("отсутствуют числа")
if not has_special:
    errors.append("отсутствуют специальные символы")

# Вывод результата
if errors:
    # Если есть ошибки — выводим их через запятую
    print("Пароль ненадежный:", ", ".join(errors))
else:
    print("Пароль надежный!")