from unit_factory import UnitFactory
from observer import Observer, Observable
from unit_event import EventType, UnitEvent, DestroyedBaseEvent
from units.unit import Unit
from datetime import datetime
import logging

class Base(Observer, Observable):
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
        self._is_disposed = False
        self._observers: list[Observer] = []

    @property
    def position(self) -> tuple[int, int]: return self._position

    def create_unit(self, kind: str, pos: tuple[int, int]):
        if self._is_disposed:
            self._logger.error("База удалена - создание юнита запрещено")
            return None
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
        unit = self._units.pop(unit_id, None)
        if unit is None:
            self._logger.debug("База не удалила юнита (id не найден)")
            return None
        try:
            unit.unsubscribe(self)
        finally:
            self._count_units -= 1
        self._logger.debug("База удалила юнита (id: %d)", unit_id)
        return unit

    def dispose(self):
        if self._is_disposed:
            return
        self._is_disposed = True
        for unit in list(self._units.values()):
            unit.unsubscribe(self)
        for obs in list(self._observers):
            self.unsubscribe(obs)
        self._units.clear()
        self._count_units = 0
        self._logger.debug("База удалена")

    def take_damage(self, raw_damage: int):
        actual = (1.0 - self._def_lvl * 0.1) * raw_damage
        self._health -= actual
        if self._health <= 0:
            self._health = 0
            self._logger.debug("База получила смертельный урон: %d", raw_damage)
            self.notify(DestroyedBaseEvent(self, raw_damage, self.position, datetime.now().timestamp()))
            self.dispose()
        return actual

    def subscribe(self, observer):
        if observer not in self._observers:
            self._logger.debug("Добавлен наблюдатель для базы")
            self._observers.append(observer)

    def unsubscribe(self, observer):
        if observer in self._observers:
            self._logger.debug("Удален наблюдатель для базы")
            self._observers.remove(observer)

    def notify(self, event):
        for observer in list(self._observers):
            if observer in self._observers:
                self._logger.debug("Оповещение наблюдателей базой")
                observer.on_event(event)

    def on_event(self, event: UnitEvent):
        if self._is_disposed:
            return
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