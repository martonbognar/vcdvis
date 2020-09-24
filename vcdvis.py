#!/usr/bin/env python3

import json
import argparse
import vcd_parser
from signal import Signal, CompoundSignal, SignalStore
import printer.ascii as PA
import printer.latex as PL


def get_parser():
    parser = argparse.ArgumentParser(
        description='Visualize a VCD waveform as ASCII or convert to a tikz figure.',
    )

    parser.add_argument(
        'cycles',
        type=float,
        help='the number of clock cycles AT THE END of the simulation to include in the output',
    )
    parser.add_argument(
        'output',
        help='the output type',
        choices=['latex', 'ascii', 'both'],
    )
    parser.add_argument(
        '-c',
        dest='config',
        default='config.json',
        help='configuration file (default: config.json)',
    )
    parser.add_argument(
        '-f',
        dest='file',
        help='the VCD file to parse (default: taken from the config file)',
    )

    return parser.parse_args()


def parse_config(config_file: str, file_arg: str, cycles: float):
    with open(config_file) as file:
        cfg = json.load(file)
        if file_arg is not None:
            cfg['file_path'] = file_arg
        cfg['cycles'] = int(cycles * 2)
        return cfg


def gather_signals(config) -> SignalStore:
    clk = Signal(cfg['clk_signal'])
    delimiter = Signal(cfg['delimiter']) if 'delimiter' in cfg else None
    signals = []
    for signal in cfg['signals']:
        if isinstance(signal['name'], str):
            # creating a simple signal
            signals.append(
                Signal(
                    name=signal['name'],
                    type_in=signal.get('type', 'wire'),
                    label=signal['label'],
                    color=signal['color'],
                )
            )
        else:
            # creating a compound signal
            subsignals = [Signal(name=name, color=signal['color']) for name in signal['name']]
            signals.append(
                CompoundSignal(
                    signals=subsignals,
                    label=signal['label'],
                    color=signal['color'],
                )
            )
    return SignalStore(clk=clk, delimiter=delimiter, signals=signals)


if __name__ == '__main__':
    args = get_parser()

    cfg = parse_config(
        config_file=args.config,
        file_arg=args.file,
        cycles=args.cycles,
    )
    signals = gather_signals(cfg)
    vcd_parser.parse_vcd(cfg['file_path'], signals)

    if args.output in ['ascii', 'both']:
        PA.draw(cfg['cycles'], signals)
    if args.output in ['latex', 'both']:
        [print(f) for f in PL.tikz(cfg['cycles'], signals)]
