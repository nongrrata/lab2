from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, mediator):
        self._mediator = mediator

    @abstractmethod
    def execute(self):
        pass