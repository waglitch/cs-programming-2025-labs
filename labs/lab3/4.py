x = int(input("Введите число:"))
n = 1
for i in range(1, x + 1):
    n *= i
print(f"факториал числа {x}: {n}")
