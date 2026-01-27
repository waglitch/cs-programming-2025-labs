"""
Модуль для работы с хранением данных
"""
import json
import os
from typing import Dict, List, Any
from datetime import datetime
from .models import Tank, Transaction, Statistics

class DataStorage:
    """Класс для работы с файловым хранилищем"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Создать директорию для данных если её нет"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def save_tanks(self, tanks: List[Tank]):
        """Сохранить состояние цистерн"""
        data = [tank.to_dict() for tank in tanks]
        self._save_json('tanks.json', data)
    
    def load_tanks(self) -> List[Tank]:
        """Загрузить состояние цистерн"""
        data = self._load_json('tanks.json')
        if not data:
            return []
        
        tanks = []
        for tank_data in data:
            tanks.append(Tank.from_dict(tank_data))
        return tanks
    
    def save_transaction(self, transaction: Transaction):
        """Сохранить транзакцию"""
        transactions = self.load_transactions()
        transactions.append(transaction.to_dict())
        self._save_json('transactions.json', transactions[-100:])  # Храним последние 100
    
    def load_transactions(self) -> List[Dict]:
        """Загрузить историю транзакций"""
        return self._load_json('transactions.json') or []
    
    def save_statistics(self, stats: Statistics):
        """Сохранить статистику"""
        self._save_json('statistics.json', stats.to_dict())
    
    def load_statistics(self) -> Statistics:
        """Загрузить статистику"""
        data = self._load_json('statistics.json')
        if data:
            return Statistics(
                total_cars=data['total_cars'],
                total_income=data['total_income'],
                fuel_stats=data['fuel_stats']
            )
        else:
            # Начальная статистика
            return Statistics(
                total_cars=0,
                total_income=0.0,
                fuel_stats={
                    fuel_type: {'liters': 0.0, 'income': 0.0}
                    for fuel_type in ["АИ-92", "АИ-95", "АИ-98", "ДТ"]
                }
            )
    
    def save_emergency_state(self, is_emergency: bool):
        """Сохранить состояние аварийного режима"""
        self._save_json('emergency_state.json', {'is_emergency': is_emergency})
    
    def load_emergency_state(self) -> bool:
        """Загрузить состояние аварийного режима"""
        data = self._load_json('emergency_state.json')
        return data.get('is_emergency', False) if data else False
    
    def _save_json(self, filename: str, data: Any):
        """Сохранить данные в JSON файл"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _load_json(self, filename: str) -> Any:
        """Загрузить данные из JSON файла"""
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return None
        return None