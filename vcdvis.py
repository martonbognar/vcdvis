#!/usr/bin/env python3

import json
import argparse
import vcd_parser
from signal import Signal
import printer.ascii as PA
import printer.latex as PL


def parse_config(config_file: str, file_arg: str):
    with open(config_file) as file:
        cfg = json.load(file)
        if file_arg is not None:
            cfg["file_path"] = file_arg
        return cfg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Visualize a VCD waveform as ASCII or convert to a tikz figure.')
    parser.add_argument(
        'cycles', type=int, help='the number of clock cycles AT THE END of the simulation to include in the output')
    parser.add_argument('-c', dest="config", default="config.json",
                        help='configuration file (default: config.json)')
    parser.add_argument(
        '-f', dest="file", help='the VCD file to parse (default: taken from the config file)')

    args = parser.parse_args()

    cfg = parse_config(config_file=args.config, file_arg=args.file)
    cfg["cycles"] = args.cycles

    signals = [Signal([cfg["clk_signal"]])]

    for signal in cfg["signals"]:
        if isinstance(signal["name"], str):
            signal["name"] = [signal["name"]]
        signals.append(Signal(signal["name"], signal["label"], signal["color"], signal.get("type", "boolean")))

    signals.append(Signal([cfg["delimiter"]]))

    vcd_parser.parse_vcd(cfg["file_path"], signals)

    PA.draw(cfg["cycles"], signals)
    [print(figure) for figure in PL.tikz(cfg["cycles"], cfg["delimiter"], signals)]
