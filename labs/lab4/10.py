s = input("Введите число: ")
if not s.isdigit():
    print("Ошибка: введите целое число.")
else:
    n = int(s)
    if n <= 1:
        print(f"{n} - не является простым числом")
    else:
        prostoe = True
        for d in range(2, n):
            if n % d == 0:
                prostoe = False
                break
        if prostoe:
            print(f"{n} - простое число")
        else:
            print(f"{n} - составное число")