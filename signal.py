from enum import Enum
from functools import reduce
from timestamp import Timestamp, Unit
from value import BoolValue, AsciiValue


class SignalType(Enum):
    WIRE  = "wire"
    HEX   = "hex"
    ASCII = "ascii"


class Signal:
    def __init__(self, name: str, type_in: str = "wire", label: str = None, color: str = "black"):
        self.name = name
        self.type = SignalType(type_in)
        self.label = label
        self.color = color
        self.id = None
        self.values = []

    def get_label(self):
        return self.label if self.label else self.name

    def get_color(self):
        return self.color

    def get_type(self):
        return self.type

    def name_match(self, name: str):
        return name == self.name

    def set_id(self, name: str, iden: str):
        self.id = iden

    def get_id(self):
        return self.id

    def id_match(self, iden: str):
        return self.id == iden

    def append_value(self, iden: str, timestamp: Timestamp, value: str):
        if self.type == SignalType.WIRE:
            val = BoolValue(value)
        if self.type == SignalType.ASCII:
            val = AsciiValue(value)
        self.values.append((timestamp, val))

    def get_last_n_values(self, n: int):
        return self.values[-n:]

    def get_values_between(self, start: Timestamp, end: Timestamp, step: Timestamp):
        index = 0
        initial_value = self.values[0][1]
        while index < len(self.values) and self.values[index][0] < start:
            initial_value = self.values[index][1]
            index += 1

        result = []
        time = start
        while time <= end:
            if index < len(self.values) and self.values[index][0] <= time:
                result.append(self.values[index][1])
                index += 1
            else:
                if result != []:
                    result.append(result[-1])
                else:
                    result.append(initial_value)
            time += step
        return result



class CompoundSignal(Signal):
    def __init__(self, signals: [Signal], label: str = None, color: str = "black"):
        self.signals = signals
        for signal in signals:
            if signal.get_type() != SignalType.WIRE:
                raise ValueError("Only wire signals can be merged! " + signal.get_label())
        self.label = label
        self.color = color

    def get_label(self):
        return self.label if self.label else " ".join(signal.get_label() for signal in self.signals)

    def get_color(self):
        return self.color

    def get_type(self):
        return self.signals[0].get_type()

    def name_match(self, name: str):
        return any(signal.name_match(name) for signal in self.signals)

    def set_id(self, name: str, iden: str):
        for signal in self.signals:
            if signal.name_match(name):
                signal.set_id(name, iden)

    def get_id(self):
        for signal in self.signals:
            if signal.get_id() == None:
                return None
        return ""

    def id_match(self, iden: str):
        return any(signal.id_match(iden) for signal in self.signals)

    def append_value(self, iden: str, timestamp: Timestamp, value: str):
        for signal in self.signals:
            if signal.id_match(iden):
                signal.append_value(iden, timestamp, value)

    def get_last_n_values(self, n: int):
        value_matrix = [signal.get_last_n_values(n) for signal in self.signals]
        return [reduce(lambda l, r: l.merge(r), row) for row in value_matrix]

    def get_values_between(self, start: Timestamp, end: Timestamp, step: Timestamp):
        value_matrix = [signal.get_values_between(start, end, step) for signal in self.signals]
        return [reduce(lambda l, r: l.merge(r), row) for row in value_matrix]


class SignalStore:
    def __init__(self, clk: Signal, delimiter: Signal = None, signals: [Signal] = [], timescale: Timestamp = None):
        self.clk = clk
        self.delimiter = delimiter
        self.signals = signals
        self.timescale = timescale

    def update_timescale(self, timescale: Timestamp):
        self.timescale = timescale

    def get_timescale(self):
        return self.timescale

    def combined(self):
        return [self.clk] + self.signals + [self.delimiter] if self.delimiter else []

    def get_values_between(self, start: Timestamp, end: Timestamp):
        clk_values = self.clk.get_last_n_values(2)
        step = clk_values[1][0] - clk_values[0][0]
        return [(signal.get_label(), signal.get_values_between(start, end, step)) for signal in self.combined()]
