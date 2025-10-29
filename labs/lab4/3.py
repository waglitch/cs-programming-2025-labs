text = input("Введите возраст собаки (в годах): ")
try:
    dog_age = float(text)
except:
    print("Ошибка: введено не число")
else:
    if dog_age < 1:
        print("Ошибка: возраст должен быть не меньше 1")
    elif dog_age > 22:
        print("Ошибка: возраст не должен превышать 22 года")
    else:
        if dog_age <= 2:
            human_age = dog_age * 10.5
        else:
            human_age = 21 + (dog_age - 2) * 4        
        if human_age.is_integer():
            human_age = int(human_age)
        print("Возраст собаки в человеческих годах:", human_age)