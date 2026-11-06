from terrains.terrain import Terrain
from units.unit import Unit
from units.unit_type_info import UnitType
import logging

class TerrainProxy(Terrain):
    def __init__(self, real_terrain: Terrain):
        self._real_terrain = real_terrain
        self._logger = logging.getLogger(__name__)
        self._cache: dict[tuple[str, Unit], float] = {}

    def is_passable(self, unit_type: str):
        result = self._real_terrain.is_passable(unit_type)
        self._logger.debug("is_passable для %s -> %s", unit_type, result)
        return result

    def get_speed_modifier(self, unit_type):
        key = ("speed", unit_type)
        if key in self._cache:
            return self._cache[key]
        value = self._real_terrain.get_speed_modifier(unit_type)
        self._cache[key] = value
        self._logger.debug("speed_modifier для %s -> %f", unit_type.value, value)
        return value

    def get_armor_bonus(self, unit_type):
        base = self._real_terrain.get_armor_bonus(unit_type)
        extra = 0.0
        if unit_type == UnitType.INFANTRY:
            extra += 0.25
        result = base + extra
        self._logger.debug("armor_bonus для %s -> %f", unit_type.value, result)
        return result

    def clone(self) -> "TerrainProxy":
        self._logger.debug("Копия TerrainProxy создана")
        return TerrainProxy(self._real_terrain.clone())

    def symbol(self):
        return self._real_terrain.symbol()