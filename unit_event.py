from enum import Enum
from abc import ABC

class EventType(Enum):
    CREATED = "created"
    DAMAGED = "damaged"
    DESTROYED = "destroyed"
    GET_RESOURSES = "get_resourses"

class UnitEvent(ABC):
    def __init__(self, type: EventType, unit_id: int, pos: tuple[int, int], timestamp: float):
        self._type = type
        self._unit_id = unit_id
        self._position = pos
        self._timestamp = timestamp

    @property
    def type(self) -> EventType: return self._type

    @property
    def unit_id(self) -> int: return self._unit_id

    @property
    def position(self) -> tuple[int, int]: return self._position

    @property
    def timestamp(self) -> float: return self._timestamp

class CreateEvent(UnitEvent):
    def __init__(self, unit_id: int, base_pos: tuple[int, int], timestamp: float):
        super().__init__(EventType.CREATED, unit_id, base_pos, timestamp)

class DamageEvent(UnitEvent):
    def __init__(self, unit_id: int, damage: int, pos: tuple[int, int], timestamp: float):
        super().__init__(EventType.DAMAGED, unit_id, pos, timestamp)
        self._damage = damage

    @property
    def damage(self) -> int: return self._damage

class DestroyedEvent(UnitEvent):
    def __init__(self, unit_id: int, damage: int, pos: tuple[int, int], timestamp: float):
        super().__init__(EventType.DESTROYED, unit_id, pos, timestamp)
        self._damage = damage

    @property
    def damage(self) -> int: return self._damage

class ResourceEvent(UnitEvent):
    def __init__(self, unit_id: int, res_amount: int, pos: tuple[int, int], timestamp: float):
        super().__init__(EventType.GET_RESOURSES, unit_id, pos, timestamp)
        self._res_amount = res_amount

    @property
    def res_amount(self) -> int: return self._res_amount