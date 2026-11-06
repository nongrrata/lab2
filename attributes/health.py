class Health:
    def __init__(self, value: int):
        if value < 0:
            raise ValueError("Величина здоровья должна быть неотрицательной")
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def decrease(self, amount: int):
        if amount < 0:
            raise ValueError("Величина урона должна быть неотрицательной")
        self._value = max(0, self._value - amount)

    def increase(self, amount: int):
        if amount < 0:
            raise ValueError("Величина лечения должна быть неотрицательной")
        self._value += amount

    def is_zero(self) -> bool:
        return self._value == 0