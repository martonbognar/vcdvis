from enum import Enum


class SignalType(Enum):
    WIRE = "wire"
    ASCII = "ascii"


class Signal:
    def __init__(self, names: [str], label: str = None, color: str = "black", type: str = "wire"):
        self.names = names
        self.type = SignalType(type)
        self.label = label
        self.values = []
        self.separate_values = {}
        self.value_store = {}
        self.color = color

    def get_label(self):
        if self.label:
            return self.label
        else:
            return "".join(self.names)

    def get_color(self):
        return self.color

    def get_type(self):
        return self.type

    def name_match(self, name):
        return name in self.names

    def set_id(self, iden: str):
        self.value_store[iden] = []

    def get_ids(self):
        return list(self.value_store.keys())

    def id_match(self, iden):
        return iden in self.value_store

    def append_value(self, iden: str, timestamp: int, value: str):
        self.value_store[iden].append((timestamp, value))

    def get_last_n_values(self, n: int):
        values = [value[-n:] for value in self.separate_values.values()]
        buf = []
        for i in range(n):
            candidate = '0'
            for value in values:
                if value[i] != '0':
                    candidate = value[i]
            buf.append(candidate)
        return buf

    def pad_to(self, max_length):
        for values in self.separate_values.values():
            if len(values) == max_length:
                continue
            else:
                try:
                    values.append(values[-1])
                    if len(values) != max_length:
                        raise AssertionError(
                            "Failed consistency check for {}".format(self.get_label()))
                except IndexError:
                    raise AssertionError(
                        "{} not initialized properly".format(self.names))

class CompoundSignal(Signal):
    pass
