from abc import ABC, abstractmethod
from neutral_object import EnergySource, Altar, Trap, TreasureChest
from strategies import HealthRestoreStrategy, DamageStrategy, ResourceStrategy
from random import choices

class NeutralObjFactory(ABC):
    @abstractmethod
    def create(self):
        pass

class RandomNeutralObjFactory(NeutralObjFactory):
    def __init__(self):
        self._objects = [EnergySource(HealthRestoreStrategy()), Altar(), Trap(DamageStrategy()), TreasureChest(ResourceStrategy()), None]
        self._weights = [0.02, 0.02, 0.02, 0.02, 0.9]

    def create(self):
        return choices(self._objects, weights=self._weights, k=1)[0]