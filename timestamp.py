import re
from enum import Enum


class Unit(Enum):
    SECOND = "s"
    MILLISECOND = "ms"
    MICROSECOND = "us"
    NANOSECOND = "ns"
    PICOSECOND = "ps"
    FEMTOSECOND = "fs"


POWERS = {
    Unit.SECOND: 1000000000000000,
    Unit.MILLISECOND: 1000000000000,
    Unit.MICROSECOND: 1000000000,
    Unit.NANOSECOND: 1000000,
    Unit.PICOSECOND: 1000,
    Unit.FEMTOSECOND: 1,
}


class Timestamp:
    def __init__(self, value: int, unit: Unit):
        self.value = value
        self.unit = unit

    @classmethod
    def from_string(cls, string: str):
        match = re.match(r'\s*(?P<value>\d+)(?P<unit>\w+)', string)
        if match:
            return cls(int(match.group('value')), Unit(match.group('unit')))
        else:
            raise ValueError("Incorrect timestamp format")

    def convert_to(self, unit: Unit) -> float:
        power_from = POWERS[self.unit]
        power_to = POWERS[unit]
        div = power_from / power_to
        return self.value * div

    def __eq__(self, other):
        return self.convert_to(Unit.FEMTOSECOND) == other.convert_to(Unit.FEMTOSECOND)

    def __lt__(self, other):
        return self.convert_to(Unit.FEMTOSECOND) < other.convert_to(Unit.FEMTOSECOND)

    def __le__(self, other):
        return self.convert_to(Unit.FEMTOSECOND) <= other.convert_to(Unit.FEMTOSECOND)

    def __add__(self, other):
        value = self.convert_to(Unit.FEMTOSECOND) + other.convert_to(Unit.FEMTOSECOND)
        return Timestamp(value, Unit.FEMTOSECOND)

    def __sub__(self, other):
        value = self.convert_to(Unit.FEMTOSECOND) - other.convert_to(Unit.FEMTOSECOND)
        return Timestamp(value, Unit.FEMTOSECOND)

    def __mul__(self, number: int):
        value = self.value * number
        return Timestamp(value, self.unit)


t_0 = Timestamp(0, Unit.SECOND)
