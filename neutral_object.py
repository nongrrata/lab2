from abc import ABC, abstractmethod
from units.unit import Unit
from units.unit_type_info import UnitType
from strategies import InteractionStrategy, AttackBoostStrategy, HealthRestoreStrategy
from copy import copy

class NeutralObject(ABC):
    def __init__(self, strategy: "InteractionStrategy" = None):
        self._strategy = strategy

    @abstractmethod
    def interact(self, unit: Unit):
        pass

    def clone(self) -> "NeutralObject":
        return copy(self)

    @abstractmethod
    def symbol(self) -> str:
        pass

class TreasureChest(NeutralObject):
    def __radd__(self, unit):
        self._strategy.apply(unit)
        return unit

    def interact(self, unit):
        return unit + self

    def symbol(self):
        return "C"

class Trap(NeutralObject):
    def __rsub__(self, unit):
        self._strategy.apply(unit)
        return unit

    def interact(self, unit):
        return unit - self

    def symbol(self):
        return "T"

class Altar(NeutralObject):
    def __init__(self):
        self._strategies = {
            UnitType.INFANTRY: AttackBoostStrategy(),
            UnitType.ARCHER: HealthRestoreStrategy(),
            UnitType.CAVALRY: HealthRestoreStrategy(),
        }

    def __rmul__(self, unit: Unit):
        self._strategy: InteractionStrategy = self._strategies.get(unit.unit_type)
        self._strategy.apply(unit)
        return unit

    def interact(self, unit):
        return unit * self

    def symbol(self):
        return "A"

class EnergySource(NeutralObject):
    def __rtruediv__(self, unit):
        self._strategy.apply(unit)
        return unit

    def interact(self, unit):
        return unit / self

    def symbol(self):
        return "H"