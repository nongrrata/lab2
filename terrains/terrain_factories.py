from abc import ABC, abstractmethod
from terrains.terrain import Terrain, Plains, Pathway, Swamp, Forest
from random import choices

class TerrainFactory(ABC):
    @abstractmethod
    def create(self) -> "Terrain":
        pass

class RandomTerrainFactory(TerrainFactory):
    def __init__(self):
        self._terrains = [Plains(), Forest(), Swamp(), Pathway()]
        self._weights = [0.7, 0.15, 0.05, 0.1]
    def create(self):
        return choices(self._terrains, weights=self._weights, k=1)[0]