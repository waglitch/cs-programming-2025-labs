"""
Вспомогательные функции для валидации
"""

def validate_positive_number(value: str) -> tuple[bool, float]:
    """Проверить что значение является положительным числом"""
    try:
        num = float(value)
        if num > 0:
            return True, num
        else:
            return False, 0
    except ValueError:
        return False, 0

def validate_integer(value: str, min_val: int = None, max_val: int = None) -> tuple[bool, int]:
    """Проверить что значение является целым числом в диапазоне"""
    try:
        num = int(value)
        if min_val is not None and num < min_val:
            return False, 0
        if max_val is not None and num > max_val:
            return False, 0
        return True, num
    except ValueError:
        return False, 0