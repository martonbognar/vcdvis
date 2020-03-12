import signal


def print_arr(arr, offset, color):
    # int_val = int(signals["inst_full"]["values"][-num:][index], 2)
    # instr = bytearray.fromhex(hex(int_val)[2:]).decode().replace(
    #     '&', '\\&').replace('#', '\\#')
    x = 0
    output = ""
    for elem in arr:
        y = offset + 1 if elem == '1' else offset
        output += "\\draw [{3},ultra thick] ({0},{2}) rectangle ({1},{2});\n".format(
            x, x + 1, y, color)
        x += 1
    return output


def figure(signals, total_cycles, start_cycle, end_cycle):
    cycle_delta = end_cycle - start_cycle
    output = ""
    output += "\\begin{figure}[h]\n"
    # output += "\\caption{{{0}}}".format(instr)
    output += "\\begin{tikzpicture}[yscale=0.5]\n"
    for i in range(len(signals)):
        output += "\\draw [help lines,lightgray,line width=0.01mm] (0,{}) grid ({},{});\n".format(
            i * 2,
            cycle_delta,
            i * 2 + 1)
        output += print_arr(signals[i].get_last_n_values(total_cycles)
                            [start_cycle:end_cycle], i * 2, signals[i].get_color())
        output += "\\node [left] at (0,{}) {{{}}};\n".format(i * 2 + 0.5, signals[i].get_label().replace('_', '\\_'))
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
