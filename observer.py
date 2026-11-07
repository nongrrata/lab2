from abc import ABC, abstractmethod
from unit_event import Event

class Observer(ABC):
    @abstractmethod
    def on_event(self, event: "Event"):
        pass

class Observable(ABC):
    @abstractmethod
    def subscribe(self, observer: "Observer"):
        pass

    @abstractmethod
    def unsubscribe(self, observer: "Observer"):
        pass

    @abstractmethod
    def notify(self, event: "Event"):
        pass