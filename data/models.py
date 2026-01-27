"""
Модели данных для системы АЗС
"""
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime
import json

@dataclass
class Tank:
    """Модель цистерны"""
    id: str
    fuel_type: str
    max_volume: float
    current_volume: float
    min_level: float
    enabled: bool
    connected_to: List[int]
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    def check_level(self) -> bool:
        """Проверка минимального уровня"""
        return self.current_volume >= self.min_level
    
    def disable_if_low(self):
        """Отключить если уровень ниже минимального"""
        if self.current_volume < self.min_level:
            self.enabled = False
            return True
        return False
    
    def add_fuel(self, volume: float) -> bool:
        """Добавить топливо в цистерну"""
        if self.current_volume + volume > self.max_volume:
            return False
        self.current_volume += volume
        return True
    
    def remove_fuel(self, volume: float) -> bool:
        """Отпустить топливо из цистерны"""
        if not self.enabled:
            return False
        if volume > self.current_volume:
            return False
        self.current_volume -= volume
        
        # Автоматическое отключение при низком уровне
        if self.current_volume < self.min_level:
            self.enabled = False
        
        return True

@dataclass
class Transaction:
    """Модель транзакции"""
    id: str
    type: str  # 'sale', 'refuel', 'transfer', 'emergency', 'tank_toggle'
    timestamp: str
    details: Dict
    
    def to_dict(self):
        return asdict(self)

@dataclass
class Statistics:
    """Статистика продаж"""
    total_cars: int
    total_income: float
    fuel_stats: Dict[str, Dict]  # fuel_type: {'liters': float, 'income': float}
    
    def to_dict(self):
        return asdict(self)