import string

import timestamp


class Value:
    def __init__(self, value, timestamp):
        self.value = value
        self.timestamp = timestamp

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        raise NotImplementedError

    def merge(self, other):
        raise NotImplementedError

    def get_timestamp(self):
        return self.timestamp


class ValueArray:
    def __init__(self, values):
        self.values = values

    def __getitem__(self, key):
        return self.values[key]

    def __len__(self):
        return len(self.values)

    def print_ascii(self):
        raise NotImplementedError

    def print_tikz(self):
        raise NotImplementedError


class BoolValue(Value):
    def __init__(self, value, timestamp=timestamp.t_0):
        self.timestamp = timestamp
        if value == 'x':
            self.value = 0
            return
            # todo: proper solution
        int_value = int(value)
        if (int_value not in [0, 1]):
            raise ValueError("Incorrect value for a bool signal: " + value)
        self.value = int_value

    def __str__(self):
        return '█' if self.value == 1 else ' '

    def merge(self, other):
        return BoolValue(self.value | other.value, self.timestamp)  # todo: ?


class AsciiValue(Value):
    def __init__(self, value, timestamp=timestamp.t_0):
        self.timestamp = timestamp
        if value == 'x':
            self.value = 0
            return
            # todo: proper solution
        # value should be in the form ?b?010110101...
        int_val = int(value, 2)
        hx = hex(int_val)[2:].ljust(2, '0')
        text = bytearray.fromhex(hx).decode('ascii', errors='ignore')
        text = ''.join(filter(lambda c: c in set(string.printable), text))
        text = text.strip()
        # text = text.replace('&', '\\&').replace('#', '\\#')
        self.value = text

    def __str__(self):
        return self.value


class BoolArray(ValueArray):
    def __init__(self, values: [BoolValue]):
        self.values = values

    def print_ascii(self) -> str:
        return "".join([str(value) for value in self.values])


class AsciiArray(ValueArray):
    def __init__(self, values: [AsciiValue]):
        self.values = values

    def print_ascii(self) -> str:
        length = len(self.values)
        boundary = 0
        output = ""
        for (index, value) in enumerate(self.values):
            if value != self.values[boundary] or index == length - 1:
                if index == length - 1:
                    index += 1
                period = index - boundary
                cutoff = str(self.values[boundary]).center(period)[:period]
                output += cutoff
                boundary = index
        return output
