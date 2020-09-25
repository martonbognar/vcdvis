from signal import SignalStore
from timestamp import Timestamp


def draw_line(arr: [str]) -> str:
    buf = ""
    for value in arr:
        buf += ' ' if value == '0' else '█'
    return buf


def draw(signals: SignalStore, start: Timestamp, end: Timestamp):
    max_label_len = max(len(signal.get_label()) for signal in signals.combined()) + 4
    for (label, values) in signals.get_values_between(start, end):
        print("{}{}".format(label.ljust(max_label_len),
                            draw_line(values)))
