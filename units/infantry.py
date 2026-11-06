from abc import ABC, abstractmethod
from units.unit import Unit
from units.unit_type_info import UnitTypeInfo

class Infantry(Unit, ABC):
    pass

class Swordsman(Infantry):
    def __init__(self, info: UnitTypeInfo, x, y):
        super().__init__(info, x, y)

    def get_type(self) -> str:
        return "swordsman"

    def symbol(self) -> str:
        return "SW"

class Spearman(Infantry):
    def __init__(self, info: UnitTypeInfo, x, y):
        super().__init__(info, x, y)

    def get_type(self) -> str:
        return "spearman"

    def symbol(self) -> str:
        return "SP"