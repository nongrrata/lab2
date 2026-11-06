from units.unit import Unit
from unit_factory import UnitFactory

class GameFieldIterator:
    def __init__(self, field: "GameField"):
        self._field = field
        self._keys = list(field._units.keys())
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._keys):
            raise StopIteration
        key = self._keys[self._index]
        self._index += 1
        return self._field._units[key]

class GameField:
    def __init__(self, width: int, height: int, max_units: int):
        if width <= 0 or width > 50:
            raise ValueError("Недопустимая величина ширины поля")
        self._width = width
        if height <= 0 or height > 30:
            raise ValueError("Недопустимая величина высоты поля")
        self._height = height
        if max_units <= 0 or max_units > width * height // 2:
            raise ValueError("Недопустимое максимальное количество существ")
        self._max_units = max_units
        self._units: dict[tuple[int, int], Unit] = {}

    def deep_copy(self) -> "GameField":
        new_field = GameField(self._width, self._height, self._max_units)
        for pos, unit in self._units.items():
            new_field._units[pos] = unit.clone()
        return new_field

    def add_unit(self, unit: Unit):
        if not self._in_bounds(unit._position):
            raise ValueError("Ошибка (попытка добавить существо вне поля)")
        if len(self._units) >= self._max_units:
            raise ValueError("Достигнуто максимальное количество существ на поле")
        self._units[unit._position] = unit

    def remove_unit(self, pos: tuple[int, int]):
        if pos not in self._units:
            raise ValueError("Ошибка при попытке удаления существа")
        del self._units[pos]

    def get_unit(self, pos: tuple[int, int]) -> Unit:
        if pos not in self._units:
            raise ValueError("Ошибка (существо не найдено)")
        return self._units[pos]

    def _in_bounds(self, pos: tuple[int, int]) -> bool:
        x, y = pos
        return (0 < x < self._width) and (0 < y < self._height)

    def move_unit(self, from_pos: tuple[int, int], to_pos: tuple[int, int]):
        if from_pos not in self._units:
            raise KeyError(f"Нет существа в клетке {from_pos}")
        if not self._in_bounds(to_pos):
            raise ValueError(f"Клетка {to_pos} вне поля")
        if to_pos in self._units:
            raise ValueError(f"Клетка {to_pos} уже занята")
        
        unit = self._units.pop(from_pos)
        unit.move(*to_pos)
        self._units[to_pos] = unit

    def spawn(self, factory: UnitFactory, kind: str, x: int, y: int) -> Unit:
        unit = factory.create_unit(kind, x, y)
        self.add_unit(unit)
        return unit

    def size(self) -> int:
        return len(self._units)

    def is_empty(self) -> bool:
        return self.size() == 0

    def clear(self):
        self._units.clear()

    def __iter__(self):
        return GameFieldIterator(self)

    def symbol(self, unit: Unit | None) -> str:
        if unit is None:
            return "."
        return unit.symbol()

    def render(self) -> str:
        lines = []
        lines.append("  ".join("X" * (self._width + 2)))
        for y in range(self._height):
            row = []
            for x in range(self._width):
                unit = self._units.get((x, y))
                CELL_W = 2
                sym = self.symbol(unit)
                row.append(f"{sym:^{CELL_W}}") 
            lines.append("X  " + " ".join(row) + " X")
        lines.append("  ".join("X" * (self._width + 2)))
        return "\n".join(lines)