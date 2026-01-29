"""
Основная логика системы управления АЗС
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import uuid
from data.models import Tank, Transaction, Statistics
from data.storage import DataStorage
import config

class AZSCore:
    """Основной класс управления АЗС"""
    
    def __init__(self):
        self.storage = DataStorage()
        self.tanks = self._init_tanks()
        self.stats = self.storage.load_statistics()
        self.is_emergency = self.storage.load_emergency_state()
        self._check_tank_levels()
    
    def _init_tanks(self) -> List[Tank]:
        """Инициализация цистерн"""
        tanks = self.storage.load_tanks()
        if not tanks:
            # Создаем начальные цистерны
            from config import INITIAL_TANKS
            for tank_data in INITIAL_TANKS:
                tanks.append(Tank(**tank_data))
            self.storage.save_tanks(tanks)
        return tanks
    
    def _check_tank_levels(self):
        """Проверка уровней всех цистерн"""
        for tank in self.tanks:
            tank.disable_if_low()
        self._save_state()
    
    def _save_state(self):
        """Сохранить состояние системы"""
        self.storage.save_tanks(self.tanks)
        self.storage.save_statistics(self.stats)
        self.storage.save_emergency_state(self.is_emergency)
    
    def _log_transaction(self, trans_type: str, details: Dict):
        """Записать транзакцию в историю"""
        transaction = Transaction(
            id=str(uuid.uuid4()),
            type=trans_type,
            timestamp=datetime.now().isoformat(),
            details=details
        )
        self.storage.save_transaction(transaction)
    
    def get_tank_by_fuel_and_column(self, fuel_type: str, column: int) -> Optional[Tank]:
        """Получить цистерну для типа топлива и колонки"""
        for tank in self.tanks:
            if (tank.fuel_type == fuel_type and 
                column in tank.connected_to and
                tank.enabled):
                return tank
        return None
    
    def get_available_fuels_for_column(self, column: int) -> Dict[str, Tank]:
        """Получить доступные виды топлива для колонки"""
        available = {}
        for tank in self.tanks:
            if column in tank.connected_to:
                available[tank.fuel_type] = tank
        return available
    
    def serve_customer(self, column: int, fuel_type: str, liters: float) -> Tuple[bool, str, float]:
        """Обслужить клиента"""
        if self.is_emergency:
            return False, "Аварийный режим! Заправка остановлена.", 0.0
        
        # Проверяем доступность топлива
        tank = self.get_tank_by_fuel_and_column(fuel_type, column)
        if not tank:
            return False, f"Топливо {fuel_type} недоступно на колонке {column}", 0.0
        
        # Проверяем наличие достаточного количества
        if liters > tank.current_volume:
            return False, f"Недостаточно топлива в цистерне. Доступно: {tank.current_volume:.1f} л", 0.0
        
        # Рассчитываем стоимость
        price_per_liter = config.FUEL_TYPES.get(fuel_type, 0)
        if price_per_liter == 0:
            return False, f"Неизвестный тип топлива: {fuel_type}", 0.0
        
        total_price = liters * price_per_liter
        
        # Списание топлива
        if not tank.remove_fuel(liters):
            return False, "Ошибка при списании топлива", 0.0
        
        # Обновление статистики
        self.stats.total_cars += 1
        self.stats.total_income += total_price
        
        if fuel_type not in self.stats.fuel_stats:
            self.stats.fuel_stats[fuel_type] = {'liters': 0.0, 'income': 0.0}
        
        self.stats.fuel_stats[fuel_type]['liters'] += liters
        self.stats.fuel_stats[fuel_type]['income'] += total_price
        
        # Логирование
        self._log_transaction('sale', {
            'column': column,
            'fuel_type': fuel_type,
            'liters': liters,
            'price_per_liter': price_per_liter,
            'total_price': total_price,
            'tank_id': tank.id
        })
        
        self._save_state()
        return True, "Операция выполнена успешно", total_price
    
    def refuel_tank(self, tank_id: str, liters: float) -> Tuple[bool, str]:
        """Пополнить цистерну"""
        if self.is_emergency:
            return False, "Аварийный режим! Операции невозможны."
        
        tank = next((t for t in self.tanks if t.id == tank_id), None)
        if not tank:
            return False, f"Цистерна {tank_id} не найдена"
        
        if not tank.add_fuel(liters):
            return False, f"Нельзя добавить {liters} л. Максимум: {tank.max_volume - tank.current_volume:.1f} л"
        
        # Логирование
        self._log_transaction('refuel', {
            'tank_id': tank_id,
            'liters_added': liters,
            'new_volume': tank.current_volume
        })
        
        self._save_state()
        return True, f"Цистерна {tank_id} пополнена на {liters} л. Текущий объем: {tank.current_volume:.1f} л"
    
    def transfer_fuel(self, from_tank_id: str, to_tank_id: str, liters: float) -> Tuple[bool, str]:
        """Перекачать топливо между цистернами"""
        if self.is_emergency:
            return False, "Аварийный режим! Операции невозможны."
        
        from_tank = next((t for t in self.tanks if t.id == from_tank_id), None)
        to_tank = next((t for t in self.tanks if t.id == to_tank_id), None)
        
        if not from_tank or not to_tank:
            return False, "Одна из цистерн не найдена"
        
        if from_tank.fuel_type != to_tank.fuel_type:
            return False, "Нельзя перекачивать разные типы топлива"
        
        if not from_tank.enabled:
            return False, f"Цистерна-источник {from_tank_id} отключена"
        
        if liters > from_tank.current_volume:
            return False, f"Недостаточно топлива в цистерне-источнике"
        
        if to_tank.current_volume + liters > to_tank.max_volume:
            return False, f"Цистерна-приемник не вмещает столько топлива"
        
        # Перекачка
        from_tank.current_volume -= liters
        to_tank.current_volume += liters
        
        # Проверка уровней после перекачки
        from_tank.disable_if_low()
        
        # Логирование
        self._log_transaction('transfer', {
            'from_tank': from_tank_id,
            'to_tank': to_tank_id,
            'liters': liters,
            'fuel_type': from_tank.fuel_type
        })
        
        self._save_state()
        return True, f"Перекачано {liters} л из {from_tank_id} в {to_tank_id}"
    
    def toggle_tank(self, tank_id: str, enable: bool) -> Tuple[bool, str]:
        """Включить/отключить цистерну"""
        tank = next((t for t in self.tanks if t.id == tank_id), None)
        if not tank:
            return False, f"Цистерна {tank_id} не найдена"
        
        if enable:
            if not tank.check_level():
                return False, f"Нельзя включить цистерну: уровень ниже минимального ({tank.min_level} л)"
            tank.enabled = True
            action = "включена"
        else:
            tank.enabled = False
            action = "отключена"
        
        # Логирование
        self._log_transaction('tank_toggle', {
            'tank_id': tank_id,
            'action': action,
            'new_state': tank.enabled,
            'volume': tank.current_volume
        })
        
        self._save_state()
        return True, f"Цистерна {tank_id} успешно {action}"
    
    def get_disabled_tanks(self) -> List[Tank]:
        """Получить список отключенных цистерн"""
        return [tank for tank in self.tanks if not tank.enabled]
    
    def get_column_status(self, column: int) -> Dict:
        """Получить статус колонки"""
        available_fuels = self.get_available_fuels_for_column(column)
        
        status = {
            'column': column,
            'available_fuels': {},
            'disabled_pistols': []
        }
        
        for fuel_type, tank in available_fuels.items():
            status['available_fuels'][fuel_type] = {
                'tank_id': tank.id,
                'tank_enabled': tank.enabled,
                'volume': tank.current_volume
            }
            
            if not tank.enabled:
                status['disabled_pistols'].append(fuel_type)
        
        return status
    
    def trigger_emergency(self) -> Tuple[bool, str]:
        """Активировать аварийный режим"""
        if self.is_emergency:
            return False, "Аварийный режим уже активен"
        
        self.is_emergency = True
        
        # Отключаем все цистерны
        for tank in self.tanks:
            tank.enabled = False
        
        # Логирование
        self._log_transaction('emergency', {
            'action': 'activated',
            'timestamp': datetime.now().isoformat()
        })
        
        self._save_state()
        return True, "Аварийный режим активирован! Все цистерны заблокированы. Вызываются аварийные службы..."
    
    def deactivate_emergency(self) -> Tuple[bool, str]:
        """Деактивировать аварийный режим"""
        if not self.is_emergency:
            return False, "Аварийный режим не активен"
        
        self.is_emergency = False
        
        # Логирование
        self._log_transaction('emergency', {
            'action': 'deactivated',
            'timestamp': datetime.now().isoformat()
        })
        
        self._save_state()
        return True, "Аварийный режим деактивирован. Цистерны остаются отключенными - включите их вручную."
    
    def get_recent_transactions(self, limit: int = 10) -> List[Dict]:
        """Получить последние транзакции"""
        transactions = self.storage.load_transactions()
        return list(reversed(transactions))[:limit]