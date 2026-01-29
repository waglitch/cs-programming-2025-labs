import random
import json
import os

# ========================
# Классы персонажей и врагов
# ========================

class Character:
    def __init__(self, name, race, hp, attack, defense, agility, height, weight):
        self.name = name
        self.race = race
        self.base_hp = hp
        self.hp = hp
        self.base_attack = attack
        self.base_defense = defense
        self.base_agility = agility
        self.height = height
        self.weight = weight
        self.level = 1
        self.exp = 0
        self.exp_to_next = 100
        self.skill_points = 0
        self.inventory = []
        self.equipped = {"weapon": None, "armor": None}

    @property
    def attack(self):
        bonus = self.equipped["weapon"].attack_bonus if self.equipped["weapon"] else 0
        return self.base_attack + bonus

    @property
    def defense(self):
        bonus = self.equipped["armor"].defense_bonus if self.equipped["armor"] else 0
        return self.base_defense + bonus

    @property
    def evasion_chance(self):
        # Пример: ловкость + влияние роста/веса
        base = self.base_agility * 0.5
        size_factor = max(0, 10 - (self.height / 10 + self.weight / 10))
        return min(70, base + size_factor)  # максимум 70% уклонения

    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_to_next:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next
        self.exp_to_next = int(self.exp_to_next * 1.5)
        self.skill_points += 3
        self.base_hp += random.randint(10, 20)
        self.hp = self.base_hp
        print(f"\n🌟 Вы достигли уровня {self.level}!")
        print(f"Получено 3 очка навыков. Всего: {self.skill_points}")

    def spend_skill_point(self, stat):
        if self.skill_points <= 0:
            print("Нет свободных очков!")
            return False
        if stat == "hp":
            self.base_hp += 10
            self.hp = self.base_hp
        elif stat == "attack":
            self.base_attack += 1
        elif stat == "defense":
            self.base_defense += 1
        elif stat == "agility":
            self.base_agility += 1
        else:
            return False
        self.skill_points -= 1
        return True

    def is_alive(self):
        return self.hp > 0

    def to_dict(self):
        return {
            "name": self.name,
            "race": self.race,
            "base_hp": self.base_hp,
            "hp": self.hp,
            "base_attack": self.base_attack,
            "base_defense": self.base_defense,
            "base_agility": self.base_agility,
            "height": self.height,
            "weight": self.weight,
            "level": self.level,
            "exp": self.exp,
            "exp_to_next": self.exp_to_next,
            "skill_points": self.skill_points,
            "inventory": [item.to_dict() for item in self.inventory],
            "equipped": {
                "weapon": self.equipped["weapon"].to_dict() if self.equipped["weapon"] else None,
                "armor": self.equipped["armor"].to_dict() if self.equipped["armor"] else None
            }
        }

    @classmethod
    def from_dict(cls, data):
        char = cls(
            data["name"], data["race"],
            data["base_hp"], data["base_attack"], data["base_defense"], data["base_agility"],
            data["height"], data["weight"]
        )
        char.hp = data["hp"]
        char.level = data["level"]
        char.exp = data["exp"]
        char.exp_to_next = data["exp_to_next"]
        char.skill_points = data["skill_points"]
        char.inventory = [Item.from_dict(item) for item in data["inventory"]]
        eq = data["equipped"]
        char.equipped["weapon"] = Item.from_dict(eq["weapon"]) if eq["weapon"] else None
        char.equipped["armor"] = Item.from_dict(eq["armor"]) if eq["armor"] else None
        return char


class Enemy:
    def __init__(self, name, hp, attack, defense, exp_reward, loot):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward
        self.loot = loot

    def is_alive(self):
        return self.hp > 0


# ========================
# Предметы
# ========================

class Item:
    def __init__(self, name, item_type, attack_bonus=0, defense_bonus=0, healing=0, value=0):
        self.name = name
        self.type = item_type  # 'weapon', 'armor', 'potion', 'gold'
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.healing = healing
        self.value = value  # для золота

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "attack_bonus": self.attack_bonus,
            "defense_bonus": self.defense_bonus,
            "healing": self.healing,
            "value": self.value
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        return cls(
            data["name"], data["type"],
            data["attack_bonus"], data["defense_bonus"],
            data["healing"], data["value"]
        )

# ========================
# Генерация контента
# ========================

RACE_STATS = {
    "Человек": {"hp": (80, 100), "atk": (10, 14), "def": (5, 9), "agi": (8, 12)},
    "Эльф": {"hp": (70, 90), "atk": (12, 16), "def": (4, 8), "agi": (12, 16)},
    "Дворф": {"hp": (90, 110), "atk": (11, 13), "def": (8, 12), "agi": (6, 10)},
}

ENEMIES_BY_FLOOR = {
    1: [
        Enemy("Гоблин", 30, 8, 3, 40, [Item("Кинжал", "weapon", attack_bonus=3)]),
        Enemy("Крыса", 20, 5, 1, 20, [Item("Зелье здоровья", "potion", healing=20)]),
    ],
    2: [
        Enemy("Орк", 60, 12, 6, 70, [Item("Топор", "weapon", attack_bonus=5)]),
        Enemy("Скелет", 45, 10, 5, 60, [Item("Кожаная броня", "armor", defense_bonus=4)]),
    ],
    3: [
        Enemy("Тролль", 100, 15, 8, 120, [Item("Меч", "weapon", attack_bonus=7), Item("Золото", "gold", value=50)]),
    ]
}

CHESTS = [
    [Item("Зелье здоровья", "potion", healing=30)],
    [Item("Стальной меч", "weapon", attack_bonus=6)],
    [Item("Кольчуга", "armor", defense_bonus=5)],
    [Item("Золото", "gold", value=30)],
]

# ========================
# Игровые функции
# ========================

def create_character():
    print("Выберите расу:")
    races = list(RACE_STATS.keys())
    for i, race in enumerate(races, 1):
        print(f"{i} - {race}")
    while True:
        try:
            choice = int(input("> ")) - 1
            if 0 <= choice < len(races):
                race = races[choice]
                break
            else:
                print("Неверный выбор.")
        except ValueError:
            print("Введите число.")

    stats = RACE_STATS[race]
    hp = random.randint(*stats["hp"])
    atk = random.randint(*stats["atk"])
    defense = random.randint(*stats["def"])
    agi = random.randint(*stats["agi"])
    height = random.randint(150, 200)
    weight = random.randint(50, 100)

    name = input("Введите имя персонажа: ")
    return Character(name, race, hp, atk, defense, agi, height, weight)


def show_status(char):
    print("\n--- Статус ---")
    print(f"Имя: {char.name} ({char.race}) | Уровень: {char.level}")
    print(f"HP: {char.hp}/{char.base_hp}")
    print(f"Атака: {char.attack} | Защита: {char.defense} | Ловкость: {char.base_agility}")
    print(f"Уклонение: {char.evasion_chance:.1f}%")
    print(f"Опыт: {char.exp}/{char.exp_to_next} | Очков навыков: {char.skill_points}")
    print("---------------\n")


def rest_room(char):
    print("\nВы вошли в комнату отдыха.")
    while char.skill_points > 0:
        print(f"\nСвободные очки: {char.skill_points}")
        print("Распределите очки:")
        print("1 - +10 HP")
        print("2 - +1 Атака")
        print("3 - +1 Защита")
        print("4 - +1 Ловкость")
        print("5 - Пропустить")
        choice = input("> ").strip()
        if choice == "1":
            char.spend_skill_point("hp")
        elif choice == "2":
            char.spend_skill_point("attack")
        elif choice == "3":
            char.spend_skill_point("defense")
        elif choice == "4":
            char.spend_skill_point("agility")
        elif choice == "5":
            break
        else:
            print("Неверный выбор.")
    print("Отдых завершён.")


def battle(char, enemy, floor):
    print(f"\n⚔️  Бой с {enemy.name}!")
    while char.is_alive() and enemy.is_alive():
        print(f"\n{enemy.name}: {enemy.hp}/{enemy.max_hp} HP")
        print("Ваши действия:")
        print("1 - Атаковать")
        print("2 - Использовать предмет")
        print("3 - Попытаться уклониться")
        action = input("> ").strip()

        if action == "1":
            # Атака игрока
            damage = max(1, char.attack - enemy.defense // 2)
            enemy.hp -= damage
            print(f"Вы нанесли {damage} урона!")
        elif action == "2":
            use_item_in_battle(char)
            continue
        elif action == "3":
            if random.random() * 100 < char.evasion_chance:
                print("Вы уклонились от атаки!")
                continue
            else:
                print("Не удалось уклониться!")
        else:
            print("Пропуск хода.")
        
        # Атака врага
        if enemy.is_alive():
            if random.random() * 100 < char.evasion_chance:
                print(f"{enemy.name} атакует, но вы уклоняетесь!")
            else:
                damage = max(1, enemy.attack - char.defense // 2)
                char.hp -= damage
                print(f"{enemy.name} наносит вам {damage} урона!")

    if char.is_alive():
        print(f"\n✅ Вы победили {enemy.name}!")
        char.gain_exp(enemy.exp_reward)
        for item in enemy.loot:
            char.inventory.append(item)
            print(f"Получено: {item.name}")
    else:
        print("\n💀 Вы погибли... Игра окончена.")
        exit()


def use_item_in_battle(char):
    potions = [item for item in char.inventory if item.type == "potion"]
    if not potions:
        print("Нет зелий!")
        return
    print("Выберите зелье:")
    for i, p in enumerate(potions, 1):
        print(f"{i} - {p.name} (+{p.healing} HP)")
    try:
        idx = int(input("> ")) - 1
        if 0 <= idx < len(potions):
            potion = potions[idx]
            char.hp = min(char.base_hp, char.hp + potion.healing)
            char.inventory.remove(potion)
            print(f"Вы использовали {potion.name}. HP: {char.hp}")
        else:
            print("Неверный выбор.")
    except ValueError:
        print("Неверный ввод.")


def chest_room(char):
    print("\nВы нашли сундук!")
    loot = random.choice(CHESTS)
    for item in loot:
        char.inventory.append(item)
        print(f"Получено: {item.name}")


def explore_room(char, room_type, floor):
    if room_type == "battle":
        enemy = random.choice(ENEMIES_BY_FLOOR.get(floor, ENEMIES_BY_FLOOR[3]))
        battle(char, enemy, floor)
    elif room_type == "rest":
        rest_room(char)
    elif room_type == "chest":
        chest_room(char)


def show_inventory(char):
    if not char.inventory:
        print("\nИнвентарь пуст.")
        return
    print("\n--- Инвентарь ---")
    for i, item in enumerate(char.inventory, 1):
        if item.type == "gold":
            print(f"{i}. {item.name} ({item.value} монет)")
        elif item.type == "potion":
            print(f"{i}. {item.name} (+{item.healing} HP)")
        elif item.type == "weapon":
            print(f"{i}. {item.name} (Атака +{item.attack_bonus})")
        elif item.type == "armor":
            print(f"{i}. {item.name} (Защита +{item.defense_bonus})")
    print("------------------")


def manage_inventory(char):
    while True:
        show_inventory(char)
        print("\nДействия:")
        print("1 - Экипировать предмет")
        print("2 - Выбросить предмет")
        print("3 - Назад")
        choice = input("> ").strip()
        if choice == "1":
            equip_item(char)
        elif choice == "2":
            discard_item(char)
        elif choice == "3":
            break
        else:
            print("Неверный выбор.")


def equip_item(char):
    weapons = [item for item in char.inventory if item.type == "weapon"]
    armors = [item for item in char.inventory if item.type == "armor"]
    print("\nОружие:")
    for i, w in enumerate(weapons, 1):
        print(f"{i}. {w.name} (+{w.attack_bonus} ATK)")
    if weapons:
        try:
            idx = int(input("Выберите оружие (0 — ничего не экипировать): ")) - 1
            if idx == -1:
                char.equipped["weapon"] = None
            elif 0 <= idx < len(weapons):
                char.equipped["weapon"] = weapons[idx]
        except ValueError:
            pass
    print("\nБроня:")
    for i, a in enumerate(armors, 1):
        print(f"{i}. {a.name} (+{a.defense_bonus} DEF)")
    if armors:
        try:
            idx = int(input("Выберите броню (0 — ничего не экипировать): ")) - 1
            if idx == -1:
                char.equipped["armor"] = None
            elif 0 <= idx < len(armors):
                char.equipped["armor"] = armors[idx]
        except ValueError:
            pass
    print("Экипировка обновлена.")


def discard_item(char):
    if not char.inventory:
        print("Нечего выбрасывать.")
        return
    show_inventory(char)
    try:
        idx = int(input("Номер предмета для удаления (0 — отмена): ")) - 1
        if idx == -1:
            return
        if 0 <= idx < len(char.inventory):
            removed = char.inventory.pop(idx)
            print(f"Выброшено: {removed.name}")
    except ValueError:
        print("Неверный ввод.")


def save_game(char, floor):
    data = {
        "character": char.to_dict(),
        "floor": floor
    }
    with open("savegame.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Игра сохранена!")


def load_game():
    if not os.path.exists("savegame.json"):
        return None, None
    try:
        with open("savegame.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        char = Character.from_dict(data["character"])
        floor = data["floor"]
        return char, floor
    except Exception as e:
        print("Ошибка загрузки:", e)
        return None, None


# ========================
# Главный цикл игры
# ========================

def main():
    print("=== Текстовая RPG ===")
    print("1 - Новая игра")
    print("2 - Загрузить игру")
    choice = input("> ").strip()
    if choice == "2":
        char, floor = load_game()
        if char is None:
            print("Сохранение не найдено. Начинаем новую игру.")
            char = create_character()
            floor = 1
    else:
        char = create_character()
        floor = 1

    room_count = 0
    while True:
        show_status(char)
        room_count += 1

        # Определяем типы комнат на развилке
        left_type = random.choice(["battle", "rest", "chest"])
        right_type = random.choice(["battle", "rest", "chest"])

        # Определяем, видны ли комнаты
        left_known = random.choice([True, False])
        right_known = random.choice([True, False])

        print("\nПеред вами развилка.")
        left_desc = left_type if left_known else "???"
        right_desc = right_type if right_known else "???"
        print(f"(1) Слева: {left_desc}")
        print(f"(2) Справа: {right_desc}")
        print("(3) Инвентарь")
        print("(4) Сохранить игру")

        action = input("> ").strip()
        if action == "1":
            explore_room(char, left_type, floor)
        elif action == "2":
            explore_room(char, right_type, floor)
        elif action == "3":
            manage_inventory(char)
            continue
        elif action == "4":
            save_game(char, floor)
            continue
        else:
            print("Неверный выбор.")
            continue

        if not char.is_alive():
            break

        # Переход на новый этаж каждые 5 комнат
        if room_count % 5 == 0:
            floor += 1
            print(f"\n🚪 Вы спустились на этаж {floor}!")


if __name__ == "__main__":
    main()