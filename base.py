from unit_factory import UnitFactory
from observer import Observer
from unit_event import EventType, UnitEvent, CreateEvent
from units.unit import Unit
from datetime import datetime
import logging

class Base(Observer):
    def __init__(self, health: int, max_units: int, def_lvl: int, resourses: int, position: tuple[int, int]):
        self._health = health
        self._max_units = max_units
        self._def_lvl = def_lvl
        self._resources = resourses
        self._units: dict[int, Unit] = {}
        self._count_units = 0
        self._position = position
        self._logger = logging.getLogger(__name__)
        self._factory = UnitFactory()

    @property
    def position(self) -> tuple[int, int]: return self._position

    def create_unit(self, kind: str, pos: tuple[int, int]):
        if len(self._units) >= self._max_units:
            self._logger.debug("База не создала юнита (достигнуто максимальное количество)")
            return None
        x, y = pos
        unit = self._factory.create_unit(kind, x, y)
        self._units[unit.id] = unit
        unit.subscribe(self)
        self._count_units += 1
        self._logger.debug("Создан %s на клетке (%d, %d)", kind, pos[0], pos[1])
        return unit

    def remove_unit(self, unit_id: int):
        if unit_id not in self._units:
            self._logger.debug("База не удалила юнита (id не найден)")
            return None
        self._units.pop(unit_id)
        self._count_units -= 1
        self._logger.debug("База удалила юнита (id: %d)", unit_id)

    def on_unit_event(self, event: UnitEvent):
        if event.type is EventType.DESTROYED:
            self.remove_unit(event.unit_id)
            self._logger.debug("Юнит (id: %d) погиб (урон: %d)", event.unit_id, event.damage)
        elif event.type is EventType.DAMAGED:
            self._logger.debug("Юнит (id: %d) получил %d урона", event.unit_id, event.damage)
        elif event.type is EventType.GET_RESOURSES:
            self._resources += event.res_amount
            self._logger.debug("База получила %d золота от юнита (id: %d)", event.res_amount, event.unit_id)

    def get_unit(self, unit_id: int) -> Unit:
        if unit_id not in self._units:
            self._logger.error("Юнит (id: %d) отсутсвует", unit_id)
            raise RuntimeError(f"id: {unit_id} юнита не существует")
        return self._units[unit_id]

    def symbol(self):
        return "B"