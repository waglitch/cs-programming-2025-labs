numbers= list(map(int,input("Введите 5 целых чисел через пробел:").split()))
squares = [x*x for x in numbers ]
print(squares)