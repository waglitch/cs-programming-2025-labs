# задание 1
x=10  # int
fi = 4.1 # float
name ="xto i?" # str
bo = True #bool

# задание 2
my_name ="Timofey"
my_ago = 18
print(my_name,my_ago)

# задание 3
x1 = 342
x2 = 56.2
x3 = "43"
f = x1+x2+int(x3)
print(f)

# задание 4
a = 3
b = 8
b1 = (a+4*b)*(a-3*b) + a**2
print(b1)

# задание 5
boba1 = float(input("Введите длину треугольника:"))
boba2 = int(input("Введите ширину треугольника:"))
ploshad =  boba1 * boba2
perimetr = 2 * (boba1 + boba2)
print(ploshad)
print(perimetr)

# задание 6
print("*   *   *")
print(" * * * *")
print("  *   *")

# задание 7

m1 = 23
m2 = 346
print(m1-m2)
print(m1+m2)
print(m1*m2)
print(m1//m2)
print(m1/m2)
print(m1%m2)
print(m1**m2)
# задание 8

namee = "тимофей"
vozrast = "18"
kaka = f'Меня зовут {namee}, мне {vozrast} лет'
print(kaka)

# задание 9
sentense = "Съешь еще этих мягких французских булок, да выпей чаю"
part1 = sentense[:5]
part2 = sentense[6:11]
part3 = sentense[11:16]
part4 = sentense[16:22]
part5 = sentense[22:33]
part6 = sentense[34:]
new_sentense = part1 + " " + part2 + " " + part3+ " " + part4+ " " + part5 + " " + part6
print(new_sentense)

# задание 10
results1= (" НЕТ! ДА! ")*4
print(results1)

# задание 11
input_string = input("Введите три числа, разделенные запятыми: ")
a,b,c= map(int, input_string.split(","))
result4 = (a+c)//b
print(f"результат вычисления:{result4}")

# задание 12
wordd = input("Введите слово, содержащее не менее 10 символов: ")
if len(wordd) >= 10:
    print(wordd[:4])
    print(wordd[-2:])
    print(wordd[3:8])
    print(wordd[::-1])
else:
    print("Ошибка: длина слова должна быть не менее 10 символов.")

