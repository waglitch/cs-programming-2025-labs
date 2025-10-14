x = int(input("Введите число от 1 до 9:"))
if x < 1 or x > 9:
    print("надо от 1 до 9")
else:
    for i in range(1,11):
        n = x*i
        print(f"{x} x {i} = {n}")