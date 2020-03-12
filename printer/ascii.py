import signal


def draw_line(arr: [str]):
    buf = ""
    for char in arr:
        buf += ' ' if char == '0' else '█'
    return buf


def draw(cycles: int, signals: [signal.Signal]):
    for signal in signals:
        print("{}{}".format(signal.get_label().ljust(20),
                            draw_line(signal.get_last_n_values(cycles))))
