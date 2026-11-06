from abc import ABC, abstractmethod
from units.unit import Unit
from units.unit_type_info import UnitTypeInfo

class Cavalry(Unit, ABC):
    pass

class Cataphract(Cavalry):
    def __init__(self, info: UnitTypeInfo, x, y):
        super().__init__(info, x, y)

    def get_type(self):
        return "cataphract"

    def symbol(self) -> str:
        return "CP"

class HorseArcher(Cavalry):
    def __init__(self, info: UnitTypeInfo, x, y):
        super().__init__(info, x, y)

    def get_type(self):
        return "horse_archer"

    def symbol(self) -> str:
        return "HO"