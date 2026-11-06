class Armor:
    def __init__(self, value: int):
        if value < 0:
            raise ValueError("Величина брони должна быть неотрицательной")
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def reduce_damage(self, damage: int) -> int:
        if damage < 0:
            raise ValueError("Величина урона должна быть неотрицательной")
        return max(0, damage - self._value)