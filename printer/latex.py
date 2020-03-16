import signal


def print_ascii(arr, offset, color) -> str:
    period_start = 0
    output = ""
    for index, elem in enumerate(arr):
        if elem != arr[period_start] or index == len(arr) - 1:
            int_val = int(elem, 2)
            hx = hex(int_val)[2:].ljust(2, '0')
            text = bytearray.fromhex(hx).decode().replace(
                '&', '\\&').replace('#', '\\#')
            output += "\\draw [{},ultra thick] ({},{}) rectangle ({},{});\n".format(
                color, period_start, offset, index + 1, offset + 1)
            output += "\\node at ({},{}) {{{}}};\n".format(
                (period_start + index + 1) / 2, offset + 0.5, text)
            period_start = index
    return output


def print_wire(arr, offset, color) -> str:
    x = 0
    output = ""
    output += "\\draw [help lines,lightgray,line width=0.01mm] (0,{}) grid ({},{});\n".format(
        offset,
        len(arr),
        offset + 1)
    for elem in arr:
        y = offset + 1 if elem == '1' else offset
        output += "\\draw [{3},ultra thick] ({0},{2}) -- ({1},{2});\n".format(
            x, x + 1, y, color)
        x += 1
    return output


def figure(signals, total_cycles, start_cycle, end_cycle) -> str:
    cycle_delta = end_cycle - start_cycle
    output = ""
    output += "\\begin{figure}[h]\n"
    output += "\\begin{tikzpicture}[yscale=0.5]\n"
    for i in range(len(signals)):
        if signals[i].get_type() == signal.SignalType.BOOLEAN:
            output += print_wire(signals[i].get_last_n_values(total_cycles)
                                 [start_cycle:end_cycle], i * 2, signals[i].get_color())
        elif signals[i].get_type() == signal.SignalType.ASCII:
            output += print_ascii(signals[i].get_last_n_values(total_cycles)
                                  [start_cycle:end_cycle], i * 2, signals[i].get_color())
        output += "\\node [left] at (0,{}) {{{}}};\n".format(
            i * 2 + 0.5, signals[i].get_label().replace('_', '\\_'))
    output += "\\end{tikzpicture}\n"
    output += "\\end{figure}\n\n"
    return output


def tikz(cycles: int, delimiter: str, signals: [signal.Signal]) -> [str]:
    last_print_cycle = 0
    figures = []
    delimiter_signal = [
        signal for signal in signals if signal.name_match(delimiter)][0]
    values = delimiter_signal.get_last_n_values(cycles)
    for i in range(cycles):
        if (values[i] == '1' and values[i-1] == '1'):
            figures.append(figure(signals, cycles, last_print_cycle, i + 1))
            last_print_cycle = i + 1
    if last_print_cycle != cycles:
        figures.append(figure(signals, cycles, last_print_cycle, cycles))
    return figures
