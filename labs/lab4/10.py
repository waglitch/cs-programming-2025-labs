# Пытаемся прочитать число
s = input("Введите число: ")

# Проверяем, что ввели целое число
if not s.lstrip('-').isdigit():
    print("Ошибка: введите целое число.")
else:
    n = int(s)
    if n <= 1:
        print(f"{n} - не является простым числом")
    else:
        # Считаем, что число простое
        prostoe = True
        # Проверяем делители от 2 до n-1
        for d in range(2, n):
            if n % d == 0:
                prostoe = False
                break

        if prostoe:
            print(f"{n} - простое число")
        else:
            print(f"{n} - составное число")