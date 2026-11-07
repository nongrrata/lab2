from terrains.terrain_proxy import TerrainProxy
from units.unit import Unit
from neutral_object import NeutralObject
from base import Base
import logging

class Cell:
    def __init__(self, pos: tuple[int, int], terrain: "TerrainProxy", neutral: NeutralObject | None = None, base: Base | None = None):
        self._terrain = terrain
        self._unit: Unit = None
        self._neutral = neutral
        self._base = base
        self._pos = pos
        self._logger = logging.getLogger(__name__)

    @property
    def terrain(self): return self._terrain

    @property
    def unit(self): return self._unit

    @property
    def neutral(self): return self._neutral

    @property
    def base(self): return self._base

    @property
    def position(self): return self._pos

    def is_free(self) -> bool:
        return self.unit is None

    def place_unit(self, unit):
        if not self.is_free():
            self._logger.error("Ошибка при размещении юнита на клетку (клетка занята)")
            raise RuntimeError("Клетка занята")
        self._unit = unit

    def remove_unit(self):
        if self._unit is None:
            self._logger.error("Ошибка при удалении юнита из клетки (клетка пуста)")
            raise RuntimeError("На клетке нет юнита")
        self._unit = None

    def set_neutral(self, obj):
        self._neutral = obj
        self._logger.debug("Установлен %s на клетку (%d, %d)", self.neutral.symbol(), self._pos[0], self._pos[1])

    def take_neutral(self):
        obj, self._neutral = self._neutral, None
        return obj

    def place_base(self, base):
        if not (self.unit is None and self.base is None):
            self._logger.error("Ошибка при размещении базы (клетка занята)")
            raise RuntimeError("Клетка занята")
        self._base = base

    def remove_base(self):
        if self._base is None:
            self._logger.error("Ошибка при удалении базы - база отсутствует")
            raise RuntimeError("База отсутствует")
        self._base = None