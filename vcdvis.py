#!/usr/bin/env python3

import argparse
import json
import sys

import printer.ascii as PA
import printer.latex as PL
import vcd_parser
from vcd_signal import Signal, CompoundSignal, SignalStore
from timestamp import Timestamp


def get_parser():
    parser = argparse.ArgumentParser(
        description='Visualize a VCD waveform as ASCII or convert to a tikz figure.',
    )

    parser.add_argument(
        'output',
        help='the output type',
        choices=['latex', 'ascii', 'both'],
    )

    window = parser.add_mutually_exclusive_group(required=True)
    window.add_argument(
        '-cycles',
        type=float,
        help='the number of clock cycles AT THE END of the simulation to include in the output',
    )
    window.add_argument(
        '-start_tick',
        dest='start',
        help='the starting tick from the simulation to be included, e.g. 120ns',
    )

    parser.add_argument(
        '-end_tick',
        dest='end',
        help='the final tick from the simulation to be included, e.g. 180ns',
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
                    # todo: make sure that supplied type is in line with actual type
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
    print("Gathered signals...", file=sys.stderr)
    return SignalStore(clk=clk, delimiter=delimiter, signals=signals)


if __name__ == '__main__':
    args = get_parser()

    with open(args.config) as file:
        cfg = json.load(file)
    if args.file is not None:
        cfg['file_path'] = args.file

    if isinstance(cfg['file_path'], str):
        # one source file
        signals = gather_signals(cfg)
        vcd_parser.parse_vcd(cfg['file_path'], signals)

        if args.start is not None:
            start = Timestamp.from_string(args.start)
            if args.end is None:
                values = signals.clk.get_last_n_values(1)
                end = values[-1].get_timestamp()
            else:
                end = Timestamp.from_string(args.end)

        if args.cycles is not None:
            cycles = int(args.cycles * 2)
            values = signals.clk.get_last_n_values(cycles)
            start = values[0].get_timestamp()
            end = values[-1].get_timestamp()

        if start is None or end is None:
            raise ValueError("No window provided")

        if args.output in ['ascii', 'both']:
            PA.draw(signals, start, end)
        if args.output in ['latex', 'both']:
            PL.draw(signals, start, end)
    else:
        # multiple source files
        signals = {}
        for file in cfg['file_path']:
            signals[file] = gather_signals(file)
            vcd_parser.parse_vcd(file, signals[file])

        if args.start is not None and args.end is not None:
            start = Timestamp.from_string(args.start)
            end = Timestamp.from_string(args.end)

        if args.cycles is not None:
            cycles = int(args.cycles * 2)
            values = signals[cfg['file_path'][0]].clk.get_last_n_values(cycles)
            start = values[0].get_timestamp()
            end = values[-1].get_timestamp()

        print("Starting compare...", file=sys.stderr)
        selected = {}
        for key in signals:
            data = signals[key].get_values_between(start, end)
            for other_key in selected:
                for i in range(len(data)):
                    if data[i][1] != selected[other_key][i][1]:
                        print("Mismatch for signal", data[i][0].get_label())
            selected[key] = data
        print("Finished comparing", file=sys.stderr)
