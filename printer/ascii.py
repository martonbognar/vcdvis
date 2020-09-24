import signal


def draw_line(arr: [(int, str)]) -> str:
    buf = ""
    for (timestamp, value) in arr:
        buf += ' ' if value == '0' else '█'
    return buf


def draw(cycles: int, signals: signal.SignalStore):
    max_label_len = max(len(signal.get_label()) for signal in signals.combined()) + 4
    clk_values = signals.clk.get_last_n_values(cycles)
    start = clk_values[0][0]
    end = clk_values[-1][0]
    for signal in signals.combined():
        print("{}{}".format(signal.get_label().ljust(max_label_len),
                            draw_line(signal.get_values_between(start, end))))
