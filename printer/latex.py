from signal import SignalType, SignalStore
from timestamp import Timestamp
from value import Value


def print_ascii(arr, offset, color) -> str:
    period_start = 0
    output = ""
    for index, elem in enumerate(arr):
        if elem != arr[period_start] or index == len(arr) - 1:
            int_val = int(arr[period_start], 2)
            hx = hex(int_val)[2:].ljust(2, '0')
            text = bytearray.fromhex(hx).decode().replace(
                '&', '\\&').replace('#', '\\#')
            if index == len(arr) - 1:
                index += 1
            output += "\\draw [{},ultra thick] ({},{}) rectangle ({},{});\n".format(
                color, period_start, offset, index, offset + 1)
            output += "\\node at ({},{}) {{{}}};\n".format(
                (period_start + index) / 2, offset + 0.5, text)
            period_start = index
    return output


def print_wire(arr, offset, color) -> str:
    output = ""
    output += "\\draw [help lines,lightgray,line width=0.01mm] (0,{}) grid ({},{});\n".format(
        offset,
        len(arr),
        offset + 1)
    for ix, elem in enumerate(arr):
        y = offset + 1 if elem == '1' else offset
        output += "\\draw [{3},ultra thick] ({0},{2}) -- ({1},{2});\n".format(
            ix, ix + 1, y, color)
        if ix != 0 and elem != arr[ix - 1]:
            output += "\\draw [{3},ultra thick] ({0},{1}) -- ({0},{2});\n".format(
            ix, offset, offset + 1, color)
    return output


def figure(signals: [(str, [Value])], total_cycles, start_cycle, end_cycle) -> str:
    output = ""
    output += "\\begin{figure}[h]\n"
    output += "\\begin{tikzpicture}[yscale=0.5]\n"
    for i in range(total_cycles):
        output += "\\node at ({0}, {1}) {{\\footnotesize {2}}};\n".format(i * 2 + 1, len(signals) * 2, i + 1)
    for i in range(len(signals)):
        if signals[i].get_type() == SignalType.WIRE:
            output += print_wire(signals[i][1][start_cycle:end_cycle], i * 2, signals[i].get_color())
        elif signals[i].get_type() == SignalType.ASCII:
            output += print_ascii(signals[i][1][start_cycle:end_cycle], i * 2, signals[i].get_color())
        output += "\\node [left] at (0,{}) {{{}}};\n".format(
            i * 2 + 0.5, signals[i].get_label().replace('_', '\\_'))
    output += "\\end{tikzpicture}\n"
    output += "\\end{figure}\n\n"
    return output


def draw(signals: SignalStore, start: Timestamp, end: Timestamp):
    combined = signals.get_values_between(start, end)
    cycles = len(combined[0][1])
    last_print_cycle = 0
    figures = []
    if signals.delimiter:
        delimiter_label = signals.delimiter.get_label()
        for (label, values) in combined:
            if label == delimiter_label:
                delimiter_values = signals.delimiter.get_last_n_values(cycles)
    else:
        delimiter_values = ['0'] * cycles
    delimited = True
    for i in range(cycles):
        if (delimiter_values[i] == '1' and delimiter_values[i-1] == '1' and not delimited):
            figures.append(figure(combined, cycles, last_print_cycle, i + 1))
            last_print_cycle = i + 1
            delimited = True
        else:
            delimited = False
    if last_print_cycle != cycles:
        figures.append(figure(combined, cycles, last_print_cycle, cycles))
    return figures
