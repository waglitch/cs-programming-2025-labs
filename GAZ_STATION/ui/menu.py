"""
Модуль пользовательского интерфейса (меню)
"""
import os
from typing import Dict, List
from core.azs_core import AZSCore
import config

class AZSMenu:  # ВАЖНО: класс должен называться именно AZSMenu
    """Класс для отображения меню и взаимодействия с пользователем"""
    
    def __init__(self):
        self.azs = AZSCore()
        self.running = True
    
    def clear_screen(self):
        """Очистить экран консоли"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Вывести заголовок АЗС"""
        print("=" * 50)
        print("АЗС <<СеверНефть>>")
        print("Система управления заправочной станцией")
        print("=" * 50)
        
        # Показываем предупреждения об отключенных цистернах
        disabled_tanks = self.azs.get_disabled_tanks()
        if disabled_tanks:
            print("\nВНИМАНИЕ!")
            print("Обнаружены отключённые цистерны:")
            for tank in disabled_tanks:
                reason = "низкий уровень топлива" if tank.current_volume < tank.min_level else "ручное отключение"
                print(f" - {tank.fuel_type} {tank.id.split('_')[-1]} ({reason})")
        
        if self.azs.is_emergency:
            print("\n🚨🚨🚨 АВАРИЙНЫЙ РЕЖИМ! 🚨🚨🚨")
            print("Все операции заблокированы!")
        
        print("-" * 50)
    
    def wait_for_enter(self):
        """Ожидание нажатия Enter"""
        input("\nНажмите Enter для продолжения...")
    
    def show_main_menu(self):
        """Показать главное меню"""
        self.clear_screen()
        self.print_header()
        
        print("Выберите действие:")
        print("1) Обслужить клиента (касса)")
        print("2) Проверить состояние цистерн")
        print("3) Оформить пополнение топлива")
        print("4) Баланс и статистика")
        print("5) История операций")
        print("6) Перекачка топлива")
        print("7) Управление цистернами")
        print("8) Состояние колонок")
        print("9) EMERGENCY - аварийная ситуация")
        print("0) Выход")
        
        return input("\n> ")
    
    def serve_customer_menu(self):
        """Меню обслуживания клиента"""
        self.clear_screen()
        print("--- Обслуживание клиента ---\n")
        
        print("Доступные колонки:")
        for i in range(1, 9):
            print(f"{i}) Колонка {i}")
        
        try:
            column = int(input("\nВыберите колонку: "))
            if column < 1 or column > 8:
                print("ОШИБКА: Неверный номер колонки")
                self.wait_for_enter()
                return
        except ValueError:
            print("ОШИБКА: Введите число от 1 до 8")
            self.wait_for_enter()
            return
        
        # Получаем доступные виды топлива для выбранной колонки
        available_fuels = self.azs.get_available_fuels_for_column(column)
        
        if not available_fuels:
            print(f"ОШИБКА: Колонка {column} не имеет доступных видов топлива")
            self.wait_for_enter()
            return
        
        print(f"\nКолонка {column}")
        print("\nДоступные виды топлива:")
        
        fuels_list = list(available_fuels.items())
        for i, (fuel_type, tank) in enumerate(fuels_list, 1):
            status = "✓ ВКЛ" if tank.enabled else "✗ ВЫКЛ"
            print(f"{i}) {fuel_type:8} (цистерна {tank.id}) [{status}]")
        
        try:
            fuel_choice = int(input("\nВыберите тип топлива: "))
            if fuel_choice < 1 or fuel_choice > len(fuels_list):
                print("ОШИБКА: Неверный выбор")
                self.wait_for_enter()
                return
        except ValueError:
            print("ОШИБКА: Введите число")
            self.wait_for_enter()
            return
        
        fuel_type, tank = fuels_list[fuel_choice - 1]
        
        if not tank.enabled:
            print(f"\nОШИБКА:")
            print(f"Цистерна {tank.id} отключена.")
            print("Отпуск топлива невозможен.")
            self.wait_for_enter()
            return
        
        try:
            liters = float(input("\nВведите количество литров: "))
            if liters <= 0:
                print("ОШИБКА: Количество должно быть положительным")
                self.wait_for_enter()
                return
        except ValueError:
            print("ОШИБКА: Введите число")
            self.wait_for_enter()
            return
        
        # Рассчет стоимости
        price_per_liter = config.FUEL_TYPES.get(fuel_type, 0)
        total_price = liters * price_per_liter
        
        print(f"\nСтоимость:")
        print(f"{liters} л × {price_per_liter:.2f} ₽ = {total_price:.2f} ₽")
        
        confirm = input("\nПодтвердить оплату? (y/n): ").lower()
        if confirm != 'y':
            print("Операция отменена")
            self.wait_for_enter()
            return
        
        # Выполнение операции
        success, message, _ = self.azs.serve_customer(column, fuel_type, liters)
        
        print(f"\n{message}")
        if success:
            print("Спасибо за покупку!")
        
        self.wait_for_enter()
    
    def show_tanks_status(self):
        """Показать статус цистерн"""
        self.clear_screen()
        print("--- Состояние цистерн ---\n")
        
        print("Доступные цистерны:")
        for i, tank in enumerate(self.azs.tanks, 1):
            status = "ВКЛ" if tank.enabled else "ВЫКЛ"
            warning = ""
            
            if tank.current_volume < tank.min_level:
                warning = " (ниже порога)"
            elif tank.current_volume < tank.min_level * 2:
                warning = " (низкий уровень)"
            
            print(f"{i}) {tank.fuel_type:6} {tank.id.split('_')[-1]:3} | "
                  f"{tank.current_volume:7.1f} / {tank.max_volume:7.1f} л | "
                  f"{status}{warning}")
        
        self.wait_for_enter()
    
    def refuel_tank_menu(self):
        """Меню пополнения цистерны"""
        self.clear_screen()
        print("--- Пополнение топлива ---\n")
        
        print("Доступные цистерны:")
        for i, tank in enumerate(self.azs.tanks, 1):
            print(f"{i}) {tank.fuel_type:6} {tank.id.split('_')[-1]:3} | "
                  f"Текущий объем: {tank.current_volume:.1f} л | "
                  f"Максимум: {tank.max_volume:.1f} л | "
                  f"Свободно: {tank.max_volume - tank.current_volume:.1f} л")
        
        try:
            choice = int(input("\nВыберите цистерну: "))
            if choice < 1 or choice > len(self.azs.tanks):
                print("ОШИБКА: Неверный выбор")
                self.wait_for_enter()
                return
        except ValueError:
            print("ОШИБКА: Введите число")
            self.wait_for_enter()
            return
        
        tank = self.azs.tanks[choice - 1]
        
        try:
            liters = float(input(f"\nВведите количество литров для добавления в {tank.id}: "))
            if liters <= 0:
                print("ОШИБКА: Количество должно быть положительным")
                self.wait_for_enter()
                return
        except ValueError:
            print("ОШИБКА: Введите число")
            self.wait_for_enter()
            return
        
        success, message = self.azs.refuel_tank(tank.id, liters)
        
        print(f"\n{message}")
        self.wait_for_enter()
    
    def show_statistics(self):
        """Показать статистику"""
        self.clear_screen()
        print("--- Баланс и статистика ---\n")
        
        stats = self.azs.stats
        
        print(f"Обслужено автомобилей: {stats.total_cars}")
        print(f"Общий доход: {stats.total_income:,.2f} ₽\n")
        
        print("Продано топлива:")
        for fuel_type in ["АИ-92", "АИ-95", "АИ-98", "ДТ"]:
            if fuel_type in stats.fuel_stats:
                fuel_stat = stats.fuel_stats[fuel_type]
                liters = fuel_stat['liters']
                income = fuel_stat['income']
                print(f"{fuel_type:6} - {liters:7.1f} л ({income:10,.2f} ₽)")
            else:
                print(f"{fuel_type:6} -    0.0 л (       0.00 ₽)")
        
        self.wait_for_enter()
    
    def show_history(self):
        """Показать историю операций"""
        self.clear_screen()
        print("--- История операций ---\n")
        
        transactions = self.azs.get_recent_transactions(15)
        
        if not transactions:
            print("История операций пуста")
        else:
            for trans in transactions:
                trans_type = trans['type']
                timestamp = trans['timestamp'][:19].replace('T', ' ')
                details = trans['details']
                
                if trans_type == 'sale':
                    print(f"[{timestamp}] Продажа: {details['liters']} л {details['fuel_type']} "
                          f"на колонке {details['column']} за {details['total_price']:.2f} ₽")
                elif trans_type == 'refuel':
                    print(f"[{timestamp}] Пополнение: +{details['liters_added']} л в {details['tank_id']} "
                          f"(новый объем: {details['new_volume']} л)")
                elif trans_type == 'transfer':
                    print(f"[{timestamp}] Перекачка: {details['liters']} л {details['fuel_type']} "
                          f"из {details['from_tank']} в {details['to_tank']}")
                elif trans_type == 'tank_toggle':
                    state = "ВКЛ" if details['new_state'] else "ВЫКЛ"
                    print(f"[{timestamp}] Цистерна {details['tank_id']} {details['action']} ({state})")
                elif trans_type == 'emergency':
                    action = "активирован" if details['action'] == 'activated' else "деактивирован"
                    print(f"[{timestamp}] Аварийный режим {action}")
        
        self.wait_for_enter()
    
    def transfer_fuel_menu(self):
        """Меню перекачки топлива"""
        self.clear_screen()
        print("--- Перекачка топлива ---\n")
        
        print("Доступные цистерны:")
        for i, tank in enumerate(self.azs.tanks, 1):
            print(f"{i}) {tank.id:10} ({tank.fuel_type}) | {tank.current_volume:7.1f} л | "
                  f"{'ВКЛ' if tank.enabled else 'ВЫКЛ'}")
        
        try:
            from_choice = int(input("\nВыберите цистерну-источник: "))
            if from_choice < 1 or from_choice > len(self.azs.tanks):
                print("ОШИБКА: Неверный выбор")
                self.wait_for_enter()
                return
        except ValueError:
            print("ОШИБКА: Введите число")
            self.wait_for_enter()
            return
        
        from_tank = self.azs.tanks[from_choice - 1]
        
        # Показываем только цистерны с тем же типом топлива
        same_type_tanks = [t for t in self.azs.tanks 
                          if t.fuel_type == from_tank.fuel_type and t.id != from_tank.id]
        
        if not same_type_tanks:
            print(f"\nОШИБКА: Нет других цистерн с топливом {from_tank.fuel_type}")
            self.wait_for_enter()
            return
        
        print(f"\nЦистерны с топливом {from_tank.fuel_type} (кроме источника):")
        for i, tank in enumerate(same_type_tanks, 1):
            print(f"{i}) {tank.id:10} | {tank.current_volume:7.1f} л | "
                  f"Свободно: {tank.max_volume - tank.current_volume:.1f} л")
        
        try:
            to_choice = int(input("\nВыберите цистерну-приемник: "))
            if to_choice < 1 or to_choice > len(same_type_tanks):
                print("ОШИБКА: Неверный выбор")
                self.wait_for_enter()
                return
        except ValueError:
            print("ОШИБКА: Введите число")
            self.wait_for_enter()
            return
        
        to_tank = same_type_tanks[to_choice - 1]
        
        try:
            liters = float(input(f"\nВведите количество литров для перекачки (макс. {from_tank.current_volume:.1f} л): "))
            if liters <= 0:
                print("ОШИБКА: Количество должно быть положительным")
                self.wait_for_enter()
                return
            if liters > from_tank.current_volume:
                print(f"ОШИБКА: Недостаточно топлива в цистерне-источнике")
                self.wait_for_enter()
                return
        except ValueError:
            print("ОШИБКА: Введите число")
            self.wait_for_enter()
            return
        
        success, message = self.azs.transfer_fuel(from_tank.id, to_tank.id, liters)
        
        print(f"\n{message}")
        self.wait_for_enter()
    
    def manage_tanks_menu(self):
        """Меню управления цистернами"""
        self.clear_screen()
        print("--- Управление цистернами ---\n")
        
        print("Доступные действия:")
        print("1) Включить цистерну")
        print("2) Отключить цистерну")
        print("3) Назад")
        
        try:
            action = int(input("\nВыберите действие: "))
        except ValueError:
            print("ОШИБКА: Введите число")
            self.wait_for_enter()
            return
        
        if action == 3:
            return
        
        if action == 1:  # Включить
            tanks_to_enable = [t for t in self.azs.tanks if not t.enabled and t.check_level()]
            
            if not tanks_to_enable:
                print("\nНет цистерн, доступных для включения")
                self.wait_for_enter()
                return
            
            print("\nЦистерны, доступные для включения:")
            for i, tank in enumerate(tanks_to_enable, 1):
                print(f"{i}) {tank.id:10} ({tank.fuel_type}) | {tank.current_volume:7.1f} л")
            
            try:
                choice = int(input("\nВыберите цистерну: "))
                if choice < 1 or choice > len(tanks_to_enable):
                    print("ОШИБКА: Неверный выбор")
                    self.wait_for_enter()
                    return
            except ValueError:
                print("ОШИБКА: Введите число")
                self.wait_for_enter()
                return
            
            tank = tanks_to_enable[choice - 1]
            success, message = self.azs.toggle_tank(tank.id, True)
            
        elif action == 2:  # Отключить
            tanks_to_disable = [t for t in self.azs.tanks if t.enabled]
            
            if not tanks_to_disable:
                print("\nВсе цистерны уже отключены")
                self.wait_for_enter()
                return
            
            print("\nЦистерны, доступные для отключения:")
            for i, tank in enumerate(tanks_to_disable, 1):
                print(f"{i}) {tank.id:10} ({tank.fuel_type}) | {tank.current_volume:7.1f} л")
            
            try:
                choice = int(input("\nВыберите цистерну: "))
                if choice < 1 or choice > len(tanks_to_disable):
                    print("ОШИБКА: Неверный выбор")
                    self.wait_for_enter()
                    return
            except ValueError:
                print("ОШИБКА: Введите число")
                self.wait_for_enter()
                return
            
            tank = tanks_to_disable[choice - 1]
            success, message = self.azs.toggle_tank(tank.id, False)
        
        else:
            print("ОШИБКА: Неверное действие")
            self.wait_for_enter()
            return
        
        print(f"\n{message}")
        self.wait_for_enter()
    
    def show_columns_status(self):
        """Показать состояние колонок"""
        self.clear_screen()
        print("--- Состояние колонок ---\n")
        
        for column in range(1, 9):
            status = self.azs.get_column_status(column)
            
            print(f"Колонка {column}:")
            
            if not status['available_fuels']:
                print("  Нет доступных видов топлива")
                continue
            
            for fuel_type, info in status['available_fuels'].items():
                status_text = "✓" if info['tank_enabled'] else "✗"
                print(f"  {status_text} {fuel_type:6} (цистерна {info['tank_id']}) - "
                      f"{info['volume']:.1f} л")
            
            if status['disabled_pistols']:
                print(f"  Отключенные пистолеты: {', '.join(status['disabled_pistols'])}")
            
            print()
        
        self.wait_for_enter()
    
    def emergency_menu(self):
        """Меню аварийной ситуации"""
        self.clear_screen()
        print("--- Аварийный режим ---\n")
        
        if self.azs.is_emergency:
            print("Текущий статус: 🚨 АКТИВЕН 🚨")
            print("\nВсе операции заблокированы.")
            print("Цистерны отключены.")
            print("\nДействия:")
            print("1) Деактивировать аварийный режим")
            print("2) Назад")
            
            try:
                choice = int(input("\nВыберите действие: "))
            except ValueError:
                print("ОШИБКА: Введите число")
                self.wait_for_enter()
                return
            
            if choice == 1:
                confirm = input("\nВы уверены, что хотите деактивировать аварийный режим? (y/n): ").lower()
                if confirm == 'y':
                    success, message = self.azs.deactivate_emergency()
                    print(f"\n{message}")
                else:
                    print("Операция отменена")
            
            elif choice == 2:
                return
            
            else:
                print("ОШИБКА: Неверный выбор")
        
        else:
            print("Текущий статус: Нормальный режим")
            print("\nДействия:")
            print("1) Активировать аварийный режим")
            print("2) Назад")
            
            try:
                choice = int(input("\nВыберите действие: "))
            except ValueError:
                print("ОШИБКА: Введите число")
                self.wait_for_enter()
                return
            
            if choice == 1:
                print("\n⚠️ ВНИМАНИЕ! ⚠️")
                print("Активация аварийного режима приведет к:")
                print("- Блокировке ВСЕХ операций")
                print("- Отключению ВСЕХ цистерн")
                print("- Автоматическому вызову аварийных служб")
                print("- Остановке заправочной станции")
                
                confirm = input("\nВы уверены, что хотите активировать аварийный режим? (y/n): ").lower()
                if confirm == 'y':
                    success, message = self.azs.trigger_emergency()
                    print(f"\n{message}")
                else:
                    print("Операция отменена")
            
            elif choice == 2:
                return
            
            else:
                print("ОШИБКА: Неверный выбор")
        
        self.wait_for_enter()
    
    def run(self):
        """Запуск главного цикла программы"""
        while self.running:
            choice = self.show_main_menu()
            
            if choice == '0':
                print("Выход из системы...")
                self.running = False
            
            elif choice == '1':
                self.serve_customer_menu()
            
            elif choice == '2':
                self.show_tanks_status()
            
            elif choice == '3':
                self.refuel_tank_menu()
            
            elif choice == '4':
                self.show_statistics()
            
            elif choice == '5':
                self.show_history()
            
            elif choice == '6':
                self.transfer_fuel_menu()
            
            elif choice == '7':
                self.manage_tanks_menu()
            
            elif choice == '8':
                self.show_columns_status()
            
            elif choice == '9':
                self.emergency_menu()
            
            else:
                print("Неверный выбор. Попробуйте еще раз.")
                self.wait_for_enter()