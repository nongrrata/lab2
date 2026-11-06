from enum import Enum
from typing import Dict
from attributes.health import Health
from attributes.armor import Armor
from attributes.attack import Attack
import logging

class UnitType(Enum):
    INFANTRY = "infantry"
    ARCHER = "archer"
    CAVALRY = "cavalry"

class UnitTypeInfo:
    _pool: Dict[UnitType, "UnitTypeInfo"] = {}
    _logger = logging.getLogger(__name__)

    def __init__(self, max_health: Health, base_armor: Armor, base_attack: Attack, base_speed: float, cost, type):
        self._max_health = max_health
        self._base_armor = base_armor
        self._base_attack = base_attack
        self._base_speed = base_speed
        self._cost = cost
        self._type = type

    @classmethod
    def get_info(cls, unit_type: UnitType) -> "UnitTypeInfo":
        if unit_type not in cls._pool:
            cls._logger.error("Ошибка при получении UnitTypeInfo для %s", unit_type.value)
            raise ValueError(f"Неизвестный тип существа: {unit_type}")
        cls._logger.debug("Получен UnitTypeInfo для %s", unit_type.value)
        return cls._pool[unit_type]