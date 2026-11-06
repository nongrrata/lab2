from base import Base
from map.terrain_map import TerrainMap
from neutral_object import Altar, Trap
from strategies import DamageStrategy
from unit_event import CreateEvent
from datetime import datetime
from math import dist
from time import sleep
import logging

class GameController:
    def __init__(self):
        self._base: Base
        self._terrain_map: TerrainMap
        self._logger = logging.getLogger(__name__)

    def setup_map(self, width: int, height: int, max_units: int):
        self._terrain_map = TerrainMap(width, height, max_units)
        self._logger.debug("Карта инициализирована")

    def setup_base(self, health: int, max_units: int, def_lvl: int, pos: tuple[int, int]):
        self._base = Base(health, max_units, def_lvl, 0, pos)
        self._terrain_map.get_cell(pos).place_base(self._base)
        self._logger.debug("База на клетке (%d, %d) создана", pos[0], pos[1])

    def spawn_unit(self, unit_type: str, pos: tuple[int, int]):
        cell = self._terrain_map.get_cell(pos)
        if not cell.is_free():
            self._logger.error("Ошибка при спавне. Клетка (%d, %d) занята", pos[0], pos[1])
            raise RuntimeError("Клетка занята")
        if not cell.terrain.is_passable(unit_type):
            self._logger.error("Ошибка при спавне. %s не может пройти через ландшафт", unit_type)
            raise RuntimeError(f"{unit_type} не может пройти через {cell.terrain}")
        unit = self._base.create_unit(unit_type, pos)
        unit.subscribe(self._terrain_map)
        unit.notify(CreateEvent(unit.id, self._base.position, datetime.now().timestamp()))
        self.interact(unit.id)

    def move_unit(self, unit_id: int, target_pos: tuple[int, int]):
        unit = self._base.get_unit(unit_id)
        unit_cell = self._terrain_map.get_cell(unit.position)
        target_cell = self._terrain_map.get_cell(target_pos)
        if not target_cell.is_free():
            self._logger.error("Ошибка при движении. Клетка (%d, %d) занята", target_pos[0], target_pos[1])
            raise RuntimeError("Клетка занята")
        if not target_cell.terrain.is_passable(unit.get_type()):
            self._logger.error("Ошибка при движении. Юнит (id: %d) не может пройти через ландшафт", unit_id)
            raise RuntimeError(f"{unit} не может пройти через {target_cell.terrain}")

        speed_modifier = unit_cell.terrain.get_speed_modifier(unit.unit_type)
        steps = unit.speed * speed_modifier
        if dist(unit.position, target_pos) > steps:
            self._logger.error("Ошибка при движении. Клетка (%d, %d) недоступна", target_pos[0], target_pos[1])
            raise RuntimeError(f"Не хватает скорости для передвижения на клетку {target_pos}")
        unit_cell.remove_unit()
        unit.move(target_pos)
        target_cell.place_unit(unit)
        self.interact(unit_id)
        self._logger.debug("Юнит (id: %d) переместился с (%d, %d) на (%d, %d)", unit_id, unit_cell.position[0], unit_cell.position[1], target_pos[0], target_pos[1])

    def interact(self, unit_id: int):
        unit = self._base.get_unit(unit_id)
        obj = self._terrain_map.get_cell(unit.position).take_neutral()
        if obj is not None:
            obj.interact(unit)
            self._logger.debug("Юнит (id: %d) использовал %s", unit_id, obj.symbol())

    def _scenario_create_base_and_units(self):
        self.setup_base(200, 20, 1, (1, 1))
        self._terrain_map.render()
        sleep(1)
        self.spawn_unit("swordsman", (1, 3))
        self.spawn_unit("light_archer", (3, 1))
        self._terrain_map.render()
        sleep(1)

    def _scenario_moving_units(self):
        self.move_unit(0, (2, 4))
        self.move_unit(1, (3, 2))
        self._terrain_map.render()
        sleep(1)

    def _scenario_with_neutral_obj(self):
        self._terrain_map.place_neutral_obj_at(Altar(), (3, 3))
        self._terrain_map.place_neutral_obj_at(Trap(DamageStrategy()), (4, 2))
        self._terrain_map.render()
        sleep(1)
        self.move_unit(0, (3, 3))
        self.move_unit(1, (4, 2))
        self._terrain_map.render()
        sleep(1)

    def _scenario_destroy_unit_with_notification(self):
        self._base.get_unit(0).take_damage(200)
        self._terrain_map.render()

    def run(self):
        self.setup_map(12, 17, 35)
        self._scenario_create_base_and_units()
        self._scenario_moving_units()
        self._scenario_with_neutral_obj()
        self._scenario_destroy_unit_with_notification()