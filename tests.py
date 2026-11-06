from unit_factory import UnitFactory
from game_field import GameField
from units.infantry import Swordsman
from attributes.health import Health
from attributes.armor import Armor
from attributes.attack import Attack
from units.unit_type_info import UnitType, UnitTypeInfo
from map.terrain_map import TerrainMap

def test_create_field_via_factory():
    factory = UnitFactory()
    field = GameField(10, 10, 50)

    unit = factory.create_unit("swordsman", 1, 1)
    field.add_unit(unit)

    assert field.size() == 1, "Существо не добавилось"
    assert field.get_unit((1, 1)) is unit, "Существо лежит не там"
    print("✅ Сценарий 1: создание через фабрику")

def test_deep_copy_independence():
    field = GameField(10, 10, 50)
    field.add_unit(Swordsman(UnitTypeInfo.get_info(UnitType.INFANTRY), 1, 1))

    copy = field.deep_copy()

    assert copy.size() == field.size(), "Размер копии не совпал"

    orig_unit = field.get_unit((1, 1))
    copy_unit = copy.get_unit((1, 1))
    assert orig_unit is not copy_unit, "Копия ссылается на тот же объект"

    copy_unit.take_damage(50)
    assert orig_unit.health == 100, "Оригинал изменился вместе с копией"
    assert copy_unit.health == 70, "Копия не получила урон"

    print("✅ Сценарий 2: глубокое копирование независимо")

def test_iteration_mass_action():
    field = GameField(10, 10, 50)
    for i in range(1, 6, 1):
        field.add_unit(Swordsman(UnitTypeInfo.get_info(UnitType.INFANTRY), i, 1))

    count = 0
    for unit in field:
        unit.take_damage(30)
        count += 1

    assert count == 5, f"Обошли {count} существ вместо 5"
    for unit in field:
        assert unit.health == 90, "Урон применился не ко всем"

    print(field.render())

    print("✅ Сценарий 4: массовое действие через итератор")

def test_render():
    pass

def set_units_info():
    UnitTypeInfo._pool[UnitType.INFANTRY] = UnitTypeInfo(Health(100), Armor(20), Attack(20), 9.0, 15, UnitType.INFANTRY)
    UnitTypeInfo._pool[UnitType.ARCHER] = UnitTypeInfo(Health(75), Armor(10), Attack(25), 8.0, 10, UnitType.ARCHER)
    UnitTypeInfo._pool[UnitType.CAVALRY] = UnitTypeInfo(Health(125), Armor(5), Attack(15), 10.0, 35, UnitType.CAVALRY)

def run_all_tests():
    set_units_info()
    test_create_field_via_factory()
    test_deep_copy_independence()
    test_iteration_mass_action()