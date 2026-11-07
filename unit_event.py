from enum import Enum
from abc import ABC

class EventType(Enum):
    CREATED = "created"
    DAMAGED = "damaged"
    DESTROYED = "destroyed"
    GET_RESOURSES = "get_resourses"
    BASE_CREATED = "base_created"
    BASE_DESTROYED = "base_destroyed"

class Event(ABC):
    def __init__(self, type: EventType, caller, pos: tuple[int, int], timestamp: float):
        self._type = type
        self._caller = caller
        self._position = pos
        self._timestamp = timestamp

    @property
    def type(self) -> EventType: return self._type

    @property
    def position(self) -> tuple[int, int]: return self._position

    @property
    def timestamp(self) -> float: return self._timestamp

class BaseEvent(Event):
    def __init__(self, type: EventType, base, pos: tuple[int, int], timestamp: float):
        super().__init__(type, base, pos, timestamp)

    @property
    def base(self): return self._caller

class CreateBaseEvent(BaseEvent):
    def __init__(self, base, pos: tuple[int, int], timestamp: float):
        super().__init__(EventType.BASE_CREATED, base, pos, timestamp)

class DestroyedBaseEvent(BaseEvent):
    def __init__(self, base, damage: int, pos: tuple[int, int], timestamp: float):
        super().__init__(EventType.BASE_DESTROYED, base, pos, timestamp)
        self._damage = damage

    @property
    def damage(self) -> int: return self._damage

class UnitEvent(Event):
    def __init__(self, type: EventType, unit_id: int, pos: tuple[int, int], timestamp: float):
        super().__init__(type, unit_id, pos, timestamp)

    @property
    def unit_id(self) -> int: return self._caller

class CreateEvent(UnitEvent):
    def __init__(self, unit, base_pos: tuple[int, int], timestamp: float):
        super().__init__(EventType.CREATED, unit.id, base_pos, timestamp)
        self._unit = unit

    @property
    def unit(self): return self._unit

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