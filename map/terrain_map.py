from map.cell import Cell
from terrains.terrain_factories import RandomTerrainFactory
from terrains.terrain_proxy import TerrainProxy
from neutral_object import NeutralObject
from neutral_obj_factories import RandomNeutralObjFactory
from observer import Observer
from unit_event import UnitEvent, EventType
import logging
import sys

class TerrainMapIterator:
    def __init__(self, terrain_map: "TerrainMap"):
        self._terrain_map = terrain_map
        self._index_i = 0
        self._index_j = 0

    def __iter__(self):
        return TerrainMapIterator(self)

    def __next__(self):
        if self._index_i >= self._terrain_map.height:
            raise StopIteration
        cell = self._terrain_map.get_cell((self._index_i, self._index_j))
        self._index_j += 1
        if self._index_j >= self._terrain_map.width:
            self._index_i += 1
            self._index_j = 0
        return cell

class TerrainMap(Observer):
    def __init__(self, width, height, max_units):
        if width <= 0 or width > 50:
            raise ValueError("Недопустимая величина ширины поля")
        self._width = width
        if height <= 0 or height > 30:
            raise ValueError("Недопустимая величина высоты поля")
        self._height = height
        if max_units <= 0 or max_units > width * height // 2:
            raise ValueError("Недопустимое максимальное количество существ")
        self._max_units = max_units
        self._terrain_factory = RandomTerrainFactory()
        self._neutral_obj_factory = RandomNeutralObjFactory()
        self._cells = [
            [Cell((i, j), TerrainProxy(self._terrain_factory.create()), self._neutral_obj_factory.create())
            for i in range(1, width + 1)]
            for j in range(1, height + 1)
        ]
        self._logger = logging.getLogger(__name__)
            
    def on_unit_event(self, event: UnitEvent):
        if event.type == EventType.DESTROYED:
            self.get_cell(event.position).remove_unit()
        elif event.type == EventType.CREATED:
            unit = self.get_cell(event.position).base.get_unit(event.unit_id)
            self.place_unit_at(unit, unit.position)

    def _in_bounds(self, pos) -> bool:
        x, y = pos
        return 1 <= x <= self._width and 1 <= y <= self._height

    def get_cell(self, pos) -> Cell:
        if not self._in_bounds(pos):
            raise ValueError("Вне поля")
        x, y = pos
        return self._cells[y - 1][x - 1]

    def place_unit_at(self, unit, pos):
        self.get_cell(pos).place_unit(unit)

    def get_neutral_obj_at(self, pos) -> NeutralObject:
        return self.get_cell(pos).neutral

    def place_neutral_obj_at(self, neutral, pos):
        self.get_cell(pos).set_neutral(neutral)

    def deep_copy(self) -> "TerrainMap":
        new_terrain_map = TerrainMap(self._width, self._height, self._max_units)
        for i in range(self._height):
            for j in range(self._width):
                cell = self._cells[i][j]
                new_cell = new_terrain_map._cells[i][j]
                new_cell._terrain = cell.terrain.clone()
                if cell.unit is not None:
                    new_cell._unit = cell.unit.clone()
                if cell.neutral is not None:
                    new_cell._neutral = cell.neutral.clone()
        self._logger.debug("Карта скопирована")
        return new_terrain_map

    @property
    def width(self): return self._width

    @property
    def height(self): return self._height

    @property
    def size(self): return self._width * self._height

    def symbol(self, cell: Cell) -> str:
        if cell.base:
            return cell.base.symbol()
        elif cell.unit:
            return cell.unit.symbol()
        elif cell.neutral:
            return cell.neutral.symbol()
        else:
            return cell.terrain.symbol()

    def render(self) -> None:
        if not sys.stdout.isatty():
            return
        print("\033[H\033[J", end="", flush=True)

        COLORS = {
            "*": "\033[32m",
            "#": "\033[38;2;0;100;0m",
            "~": "\033[38;2;0;150;255m",
            "|": "\033[37m",
            "H": "\033[31m",
            "A": "\033[35m",
            "C": "\033[38;2;255;215;0m",
            "T": "\033[38;2;139;69;19m"
        }
        RESET = "\033[0m"
        WALL_COLOR = "\033[90m"
        CELL_W = 4

        lines = []
        raw_top = "X X" + "   X" * (self._width - 1) + " X"
        lines.append(f"{WALL_COLOR}{raw_top}{RESET}")
        for y in range(1, self._height + 1):
            row_parts = [f"{WALL_COLOR}X{RESET}"]
            for x in range(1, self._width + 1):
                cell = self.get_cell((x, y))
                sym = self.symbol(cell)
                padded = f"{sym:^{CELL_W}}"
                color = COLORS.get(sym, "")
                if color and sym:
                    padded = padded.replace(sym, f"{color}{sym}{RESET}", 1)
                row_parts.append(padded)
            row_parts[-1] = row_parts[-1][:-1]
            row_parts.append(f"{WALL_COLOR}X{RESET}")
            lines.append("".join(row_parts))
        lines.append(f"{WALL_COLOR}{raw_top}{RESET}")
        self._logger.debug("Карта отрисована")
        print("\n".join(lines))