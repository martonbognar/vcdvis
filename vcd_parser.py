import io
import re
from signal import Signal, SignalStore


def set_ids(file: io.TextIOWrapper, signals: [Signal]):
    upscope_str = r'\$scope (?P<type>\w+) (?P<name>\w+) \$end'
    downscope_str = r'\$upscope \$end'
    var_str = r'\$var (?P<type>\w+) \d+ (?P<id>\S+) (?P<name>\w+)( \[\d+:0\])? \$end'

    scopes = []
    for line in file:
        var_match = re.match(var_str, line)
        if var_match:
            name = ".".join(scopes + [var_match.group('name')])
            for signal in signals:
                if signal.name_match(name):
                    signal.set_id(name, var_match.group('id'))
        else:
            upscope_match = re.match(upscope_str, line)
            if upscope_match:
                scopes.append(upscope_match.group('name'))
            else:
                downscope_match = re.match(downscope_str, line)
                if downscope_match:
                    scopes = scopes[:-1]
                else:
                    if line.startswith("$dumpvars"):
                        for signal in signals:
                            if signal.get_id() == None:
                                raise ValueError("A signal (" + signal.get_label() + ") has no ids")
                        return


def load_values(file: io.TextIOWrapper, signals: [Signal]):
    timestamp = 0
    for line in file:
        if line.startswith('#'):
            timestamp = int(line[1:])
        else:
            match = re.match(r'[b]?(?P<value>([\d]+|x))[ ]?(?P<id>\S+)$', line)
            if match:
                iden = match.group('id')
                for signal in signals:
                    if signal.id_match(iden):
                        signal.append_value(iden, timestamp, match.group('value'))


def parse_vcd(vcd_file: str, signals: SignalStore):
    with open(vcd_file) as file:
        set_ids(file, signals.combined())
        load_values(file, signals.combined())
