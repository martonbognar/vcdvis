class Value:
    def merge(self, other):
        raise NotImplementedError

class BoolValue(Value):
    def __init__(self, value):
        if value == 'x':
            self.value = 0
            return
            # todo: proper solution
        int_value = int(value)
        if (int_value not in [0, 1]):
            raise ValueError("Incorrect value for a bool signal: " + value)
        self.value = int_value

    def __str__(self):
        return str(self.value)

    def merge(self, other):
        return BoolValue(self.value | other.value)

class AsciiValue(Value):
    def __init__(self, value):
        if value == 'x':
            self.value = 0
            return
            # todo: proper solution
        # value should be in the form ?b?010110101...
        int_val = int(value, 2)
        hx = hex(int_val)[2:].ljust(2, '0')
        text = bytearray.fromhex(hx).decode().replace(
            '&', '\\&').replace('#', '\\#')
        self.value = text

    def __str__(self):
        return self.value
