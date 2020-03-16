from enum import Enum


class SignalType(Enum):
    BOOLEAN = "boolean"
    HEX = "hex"
    ASCII = "ascii"


class Signal:
    def __init__(self, names: [str], label: str = None, color: str = "black", type: str = "boolean"):
        self.names = names
        self.type = SignalType(type)
        self.label = label
        self.values = []
        self.separate_values = {}
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
        self.separate_values[iden] = None

    def buffer_empty(self):
        empty = True
        for iden in self.separate_values:
            if self.separate_values[iden] is not None:
                empty = False
        return empty

    def id_match(self, iden):
        return iden in self.separate_values

    def internal_merge(self):
        char = '0'
        for val in self.separate_values.values():
            if val != '0':
                char = val
        self.values.append(char)
        for iden in self.separate_values:
            self.separate_values[iden] = None

    def append_value(self, iden: str, value: str):
        if len(self.separate_values) == 1:
            self.values.append(value)
        else:
            self.separate_values[iden] = value

    def get_values_size(self):
        return len(self.values) + (0 if self.buffer_empty() else 1)

    def get_last_n_values(self, n: int):
        return self.values[-n:]

    def pad_to(self, max_length):
        if not self.buffer_empty():
            self.internal_merge()
        if self.get_values_size() == max_length:
            return
        try:
            self.values.append(self.values[-1])
            if self.get_values_size() != max_length:
                raise AssertionError(
                    "Failed consistency check for {}".format(self.get_label()))
        except IndexError:
            raise AssertionError(
                "{} not initialized properly".format(self.name))
