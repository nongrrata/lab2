from abc import ABC, abstractmethod
from units.unit import Unit
from units.unit_type_info import UnitTypeInfo

class Archer(Unit, ABC):
    pass

class LightArcher(Archer):
    def __init__(self, info: UnitTypeInfo, x, y):
        super().__init__(info, x, y)

    def get_type(self):
        return "light_archer"

    def symbol(self) -> str:
        return "LA"

class HeavyArcher(Archer):
    def __init__(self, info: UnitTypeInfo, x, y):
        super().__init__(info, x, y)

    def get_type(self):
        return "heavy_archer"

    def symbol(self) -> str:
        return "HA"