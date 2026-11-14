from abc import ABC, abstractmethod

class Handler(ABC):
    def __init__(self):
        self._next = None

    @abstractmethod
    def handle(self, cmd: str) -> bool:
        pass