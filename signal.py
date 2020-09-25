from enum import Enum


class SignalType(Enum):
    WIRE = "wire"
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

    def append_value(self, iden: str, timestamp: int, value: str):
        self.values.append((timestamp, value))

    def get_last_n_values(self, n: int):
        return self.values[-n:]

    def get_values_between(self, start: int, end: int):
        results = []
        value_before = None
        for (timestamp, value) in self.values:
            if timestamp < start:
                value_before = value
            elif timestamp <= end:
                results.append((timestamp, value))
            else:
                break
        return {'before': value_before, 'values': results}



class CompoundSignal(Signal):
    def __init__(self, signals: [Signal], label: str = None, color: str = "black"):
        self.signals = signals
        # TODO: check if all signals have the same type
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

    def append_value(self, iden: str, timestamp: int, value: str):
        for signal in self.signals:
            if signal.id_match(iden):
                signal.append_value(iden, timestamp, value)

    def get_last_n_values(self, n: int):
        value_matrix = [signal.get_last_n_values(n) for signal in self.signals]
        return value_matrix[0]

    def get_values_between(self, start: int, end: int):
        value_matrix = [signal.get_values_between(start, end) for signal in self.signals]
        return value_matrix[0]


class SignalStore:
    def __init__(self, clk: Signal, delimiter: Signal = None, signals: [Signal] = [], timescale: int = 0, timescale_unit: str = ""):
        self.clk = clk
        self.delimiter = delimiter
        self.signals = signals
        self.timescale = timescale
        self.timescale_unit = timescale_unit  # s, ms, us, ns, ps, or fs

    def update_timescale(self, timescale: int, unit: str):
        self.timescale = timescale
        self.timescale_unit = unit

    def combined(self):
        return [self.clk] + self.signals + [self.delimiter] if self.delimiter else []

    def get_last_n(self, n: int):
        clk_values = self.clk.get_last_n_values(n)
        start = clk_values[0][0]
        end = clk_values[-1][0]
        step = clk_values[1][0] - start
        matrix = [(signal.get_label(), signal.get_values_between(start, end)) for signal in self.combined()]
        for (label, v) in matrix:
            time = start
            index = 0
            result = []
            while time <= end:
                if index < len(v['values']) and v['values'][index][0] == time:
                    result.append(v['values'][index][1])
                    index += 1
                else:
                    # TODO: initial value
                    if result != []:
                        result.append(result[-1])
                    else:
                        result.append(v['before'])
                time += step
            yield (label, result)
