from .armor import Armor

class Attack:
    def __init__(self, value: int):
        if value < 0:
            raise ValueError("Величина атаки должна быть неотрицательной")
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def calculate_damage(self, target_armor: Armor) -> int:
        return target_armor.reduce_damage(self._value)