from units.unit import Unit
from units.infantry import Swordsman, Spearman
from units.archer import LightArcher, HeavyArcher
from units.cavalry import Cataphract, HorseArcher
from units.unit_type_info import UnitTypeInfo, UnitType

class UnitFactory:
    def create_unit(self, kind: str, x: int, y: int) -> Unit:
        if kind == "swordsman":
            return Swordsman(UnitTypeInfo.get_info(UnitType.INFANTRY), x, y)
        elif kind == "spearman":
            return Spearman(UnitTypeInfo.get_info(UnitType.INFANTRY), x, y)
        elif kind == "light_archer":
            return LightArcher(UnitTypeInfo.get_info(UnitType.ARCHER), x, y)
        elif kind == "heavy_archer":
            return HeavyArcher(UnitTypeInfo.get_info(UnitType.ARCHER), x, y)
        if kind == "cataphract":
            return Cataphract(UnitTypeInfo.get_info(UnitType.CAVALRY), x, y)
        elif kind == "horse_archer":
            return HorseArcher(UnitTypeInfo.get_info(UnitType.CAVALRY), x, y)
        else:
            raise ValueError(f"Неизвестный тип: {kind}")