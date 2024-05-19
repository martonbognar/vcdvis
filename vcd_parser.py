import io
import re
import sys
from typing import TextIO

from vcd_signal import SignalStore
from timestamp import Timestamp, Unit


def set_ids(file: TextIO, signals: SignalStore):
    upscope_str = r'\$scope\s+(?P<type>\S+)\s+(?P<name>\S+)\s+\$end'
    downscope_str = r'\$upscope\s+\$end'
    var_str = r'\$var\s*(?P<type>\w+)\s*\d+\s*(?P<id>\S+)\s*(?P<name>\w+)(\s*\[\d+:\d+\])?\s*\$end'
    timescale_inline_str = r'\$timescale\s+(?P<value>\d+)(?P<unit>\w+)'

    timescale_on_next = False

    scopes = []
    for line in file:
        line = line.strip()
        var_match = re.match(var_str, line)
        if var_match:
            name = ".".join(scopes + [var_match.group('name')])
            for signal in signals.combined():
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
                    timescale_inline_match = re.match(timescale_inline_str, line)
                    if timescale_inline_match or timescale_on_next:
                        # update timescale
                        if timescale_on_next:
                            timescale_on_next = False
                            timescale_inline_match = re.match(r'\s*(?P<value>\d+)(?P<unit>\w+)', line)
                        signals.update_timescale(Timestamp(int(timescale_inline_match.group('value')),
                                                           Unit(timescale_inline_match.group('unit'))))
                    else:
                        if line.startswith("$timescale"):
                            timescale_on_next = True
                        else:
                            if line.startswith("$dumpvars") or line.startswith("$enddefinitions"):
                                break

    for signal in signals.combined():
        if signal.get_id() is None:
            raise ValueError("A signal (" + signal.get_label() + ") has no ids")
    print("IDs collected for {}...".format(file.name), file=sys.stderr)


def load_values(file: TextIO, signals: SignalStore):
    timestamp = Timestamp(0, Unit.SECOND)
    for line in file:
        line = line.strip()
        if line.startswith('#'):
            timestamp = signals.get_timescale() * int(line[1:])
        else:
            match = re.match(r'(?P<value>(b[x01]+\s+|[x01]))?(?P<id>\S+)$', line)
            if match:
                iden = match.group('id')
                for signal in signals.combined():
                    if signal.id_match(iden):
                        signal.append_value(iden, timestamp, match.group('value').strip())
    print("Data collected for {}...".format(file.name), file=sys.stderr)


def parse_vcd(vcd_file: str, signals: SignalStore):
    with open(vcd_file) as file:
        set_ids(file, signals)
        load_values(file, signals)
