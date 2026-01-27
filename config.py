"""
Конфигурационные параметры системы АЗС
"""

# Типы топлива и их цены (руб/литр)
FUEL_TYPES = {
    "АИ-92": 55.50,
    "АИ-95": 58.30,
    "АИ-98": 64.20,
    "ДТ": 56.80
}

# Начальные данные для цистерн
INITIAL_TANKS = [
    {
        "id": "АИ-92_1",
        "fuel_type": "АИ-92",
        "max_volume": 20000,
        "current_volume": 12400,
        "min_level": 1000,
        "enabled": True,
        "connected_to": [1, 2, 3, 4, 5, 6]
    },
    {
        "id": "АИ-95_1",
        "fuel_type": "АИ-95",
        "max_volume": 20000,
        "current_volume": 9800,
        "min_level": 1000,
        "enabled": True,
        "connected_to": [1, 2, 3, 4]
    },
    {
        "id": "АИ-95_2",
        "fuel_type": "АИ-95",
        "max_volume": 20000,
        "current_volume": 1200,
        "min_level": 1000,
        "enabled": False,
        "connected_to": [5, 6, 7, 8]
    },
    {
        "id": "АИ-98_1",
        "fuel_type": "АИ-98",
        "max_volume": 15000,
        "current_volume": 10000,
        "min_level": 800,
        "enabled": False,
        "connected_to": [3, 4, 5, 6]
    },
    {
        "id": "ДТ_1",
        "fuel_type": "ДТ",
        "max_volume": 25000,
        "current_volume": 15600,
        "min_level": 1500,
        "enabled": True,
        "connected_to": [3, 4, 5, 6, 7, 8]
    }
]

# Конфигурация колонок
COLUMNS_CONFIG = {
    1: ["АИ-92", "АИ-95"],
    2: ["АИ-92", "АИ-95"],
    3: ["АИ-92", "АИ-95", "АИ-98", "ДТ"],
    4: ["АИ-92", "АИ-95", "АИ-98", "ДТ"],
    5: ["АИ-92", "АИ-95", "АИ-98", "ДТ"],
    6: ["АИ-92", "АИ-95", "АИ-98", "ДТ"],
    7: ["АИ-95", "ДТ"],
    8: ["АИ-95", "ДТ"]
}