password = input("Введите пароль: ")
errors = []
if len(password) < 8:
    errors.append("слишком короткий (менее 8 символов)")
has_upper = False
has_lower = False
has_digit = False
has_special = False
for char in password:
    if char.isupper() and char.isalpha():
        has_upper = True
    elif char.islower() and char.isalpha():
        has_lower = True
    elif char.isdigit():
        has_digit = True
    else:
        has_special = True
if not has_upper:
    errors.append("отсутствуют заглавные буквы")
if not has_lower:
    errors.append("отсутствуют строчные буквы")
if not has_digit:
    errors.append("отсутствуют числа")
if not has_special:
    errors.append("отсутствуют специальные символы")
if errors:
    print("Пароль ненадежный:", ", ".join(errors))
else:
    print("Пароль надежный!")