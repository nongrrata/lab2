from abc import ABC, abstractmethod
from units.unit_type_info import UnitType
from copy import copy

class Terrain(ABC):
    @abstractmethod
    def is_passable(self, unit_type: str) -> bool:
        pass

    @abstractmethod
    def get_speed_modifier(self, unit_type: UnitType) -> float:
        pass

    @abstractmethod
    def get_armor_bonus(self, unit_type: UnitType) -> float:
        pass

    @abstractmethod
    def symbol(self) -> str:
        pass

    def clone(self) -> "Terrain":
        return copy(self)

class Plains(Terrain):
    def is_passable(self, unit_type):
        return True

    def get_speed_modifier(self, unit_type):
        return 1.0

    def get_armor_bonus(self, unit_type):
        return 1.0

    def symbol(self):
        return "#"

class Forest(Terrain):
    def is_passable(self, unit_type):
        return unit_type != "cataphract" and unit_type != "horse_archer" and unit_type != "heavy_archer"

    def get_speed_modifier(self, unit_type):
        return 0.5

    def get_armor_bonus(self, unit_type):
        return 1.5

    def symbol(self):
        return "*"

class Swamp(Terrain):
    def is_passable(self, unit_type):
        return True

    def get_speed_modifier(self, unit_type):
        return 0.3

    def get_armor_bonus(self, unit_type):
        return 0.75

    def symbol(self):
        return "~"

class Pathway(Terrain):
    def is_passable(self, unit_type):
        return True

    def get_speed_modifier(self, unit_type):
        return 2.0

    def get_armor_bonus(self, unit_type):
        return 1.0

    def symbol(self):
        return "||"