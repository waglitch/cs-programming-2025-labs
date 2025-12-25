numbers = list(map(int,input("введите 10 чисел через пробел: ").split()))
if 3 in numbers:
    numbers[numbers.index(3)]=30
print(numbers)