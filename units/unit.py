from abc import abstractmethod
from units.unit_type_info import UnitTypeInfo
from copy import copy
from observer import Observable, Observer
from unit_event import UnitEvent, DamageEvent, ResourceEvent, DestroyedEvent
from datetime import datetime
import logging

class Unit(Observable):
    _next_id = 0

    @classmethod
    def next_id(cls) -> int:
        current_id = cls._next_id
        cls._next_id += 1
        return current_id

    def __init__(self, info: UnitTypeInfo, x: int, y: int):
        self._id = Unit.next_id()
        self._info = info
        self._current_health = info._max_health.value
        self._current_attack = info._base_attack.value
        self._current_armor_bonus = 0
        self._position = (x, y)
        self._is_heavy: bool
        self._observers: list[Observer] = []
        self._logger = logging.getLogger(__name__)

    def subscribe(self, observer):
        if observer not in self._observers:
            self._logger.debug("Добавлен наблюдатель для юнита (id: %d)", self.id)
            self._observers.append(observer)

    def unsubscribe(self, observer):
        if observer in self._observers:
            self._logger.debug("Удален наблюдатель для юнита (id: %d)", self.id)
            self._observers.remove(observer)

    def notify(self, event: UnitEvent):
        for observer in self._observers:
            self._logger.debug("Оповещение наблюдателей юнитом (id: %d)", self.id)
            observer.on_unit_event(event)

    @property
    def health(self): return self._current_health

    @property
    def armor(self): return self._info._base_armor.value + self._current_armor_bonus

    @property
    def attack(self): return self._current_attack

    @property
    def speed(self): return self._info._base_speed

    @property
    def position(self): return self._position

    @property
    def id(self): return self._id

    @property
    def unit_type(self):
        for key, val in self._info._pool.items():
            if val == self._info:
                return key

    @abstractmethod
    def symbol(self) -> str: pass

    def clone(self) -> "Unit":
        new_unit = copy(self)
        new_unit._id = Unit.next_id()
        new_unit._position = (self._position[0], self._position[1])
        return new_unit

    @abstractmethod
    def get_type(self) -> str:
        pass

    def move(self, new_pos: tuple[int, int]):
        self._position = new_pos

    def take_damage(self, raw_damage: int):
        actual = max(0, raw_damage - self.armor)
        self._current_health -= actual
        if self._current_health <= 0:
            self._current_health = 0
            self.notify(DestroyedEvent(self.id, raw_damage, self.position, datetime.now().timestamp()))
        else:
            self.notify(DamageEvent(self.id, actual, self.position, datetime.now().timestamp()))
        return actual

    def is_alive(self) -> bool:
        return not self._current_health == 0

    def get_attack_boost(self, amount):
        self._current_attack += amount

    def heal(self):
        self._current_health = self._info._max_health.value

    def get_resourses(self, amount):
        self.notify(ResourceEvent(self.id, amount, self.position, datetime.now().timestamp()))