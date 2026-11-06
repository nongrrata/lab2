from abc import ABC, abstractmethod
from unit_event import UnitEvent

class Observer(ABC):
    @abstractmethod
    def on_unit_event(self, event: "UnitEvent"):
        pass

class Observable(ABC):
    @abstractmethod
    def subscribe(self, observer: "Observer"):
        pass

    @abstractmethod
    def unsubscribe(self, observer: "Observer"):
        pass

    @abstractmethod
    def notify(self, event: "UnitEvent"):
        pass