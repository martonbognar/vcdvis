import io
import re
import signal


def set_ids(file: io.TextIOWrapper, signals: [signal.Signal]):
    for line in file:
        match = re.match(
            r'\$var (?P<type>\w+) \d+ (?P<id>\S+) (?P<name>\w+)( \[\d+:0\])? \$end', line)
        if match:
            name = match.group('name')
            for signal in signals:
                if signal.name_match(name):
                    signal.set_id(match.group('id'))
        else:
            if line.startswith("$dumpvars"):
                return


def load_values(file: io.TextIOWrapper, signals: [signal.Signal]):
    for line in file:
        if line.startswith('#'):
            consistency_check(signals)
        else:
            match = re.match(r'[b]?(?P<value>([\d]+|x))[ ]?(?P<id>\S+)$', line)
            if match:
                iden = match.group('id')
                for signal in signals:
                    if signal.id_match(iden):
                        signal.append_value(iden, match.group('value'))


def consistency_check(signals: [(str, signal.Signal)]):
    max_length = max([signal.get_values_size() for signal in signals])
    for signal in signals:
        signal.pad_to(max_length)


def parse_vcd(vcd_file: str, signals: [signal.Signal]):
    with open(vcd_file) as file:
        set_ids(file, signals)
        load_values(file, signals)
        consistency_check(signals)
