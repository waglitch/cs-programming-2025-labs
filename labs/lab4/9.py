hour = int(input("Введите час (0-23): "))
if 0 <= hour <= 5:
    print("Сейчас ночь")
elif 6 <= hour <= 11:
    print("Сейчас утро")
elif 12 <= hour <= 17:
    print("Сейчас день")
elif 18 <= hour <= 23:
    print("Сейчас вечер")