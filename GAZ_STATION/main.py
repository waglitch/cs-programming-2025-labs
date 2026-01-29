#!/usr/bin/env python3
"""
Главный файл системы управления АЗС
"""
import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.menu import AZSMenu

def main():
    """Главная функция программы"""
    print("Загрузка системы управления АЗС...")
    
    try:
        menu = AZSMenu()
        menu.run()
        
        print("Система завершена. Данные сохранены.")
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()