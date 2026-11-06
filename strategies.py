from abc import ABC, abstractmethod
from units.unit import Unit

class InteractionStrategy(ABC):
    @abstractmethod
    def apply(self, unit: Unit):
        pass

class AttackBoostStrategy(InteractionStrategy):
    def apply(self, unit):
        unit.get_attack_boost(5)

class HealthRestoreStrategy(InteractionStrategy):
    def apply(self, unit):
        unit.heal()

class DamageStrategy(InteractionStrategy):
    def apply(self, unit):
        unit.take_damage(15)

class ResourceStrategy(InteractionStrategy):
    def apply(self, unit):
        unit.get_resourses(50)