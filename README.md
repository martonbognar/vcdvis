# vcdvis

Convert your value change dumps into TikZ figures or visualize them in ASCII.
The tool is clock cycle based, async signals will not work properly.

vcdvis is still very much a work in progress, feel free to submit issues or pull requests!

## Usage

```bash
$ ./vcdvis.py -h
usage: vcdvis.py [-h] (-cycles CYCLES | -start_tick START) [-end_tick END] [-c CONFIG] [-f FILE] {latex,ascii,both}

Visualize a VCD waveform as ASCII or convert to a tikz figure.

positional arguments:
  {latex,ascii,both}  the output type

optional arguments:
  -h, --help          show this help message and exit
  -cycles CYCLES      the number of clock cycles AT THE END of the simulation to include in the output
  -start_tick START   the starting tick from the simulation to be included, e.g. 120ns
  -end_tick END       the final tick from the simulation to be included, e.g. 180ns
  -c CONFIG           configuration file (default: config.json)
  -f FILE             the VCD file to parse (default: taken from the config file)
```

You can specify the timeframe you want to visualize two different ways:
1. By supplying the `-cycles N` argument. This will plot the final N clock cycles from the simulation.
Tip: if the simulation ends in the middle of a cycle (only one half of a cycle
is included at the end), you can provide a decimal `cycles` argument to offset
this effect so that the visualization doesn't also start in the middle of a
cycle, e.g. `57.5` if you want to visualize 57 cycles but a half extra cycle is
included at the end of the VCD file.
2. By supplying the `-start_tick TICK` and optionally the `-end_tick TICK` arguments.
Running `./vcdvis.py ascii -start_tick 131890ns -end_tick 132234ns` will visualize the selected signals
between the two specified timestamps (you can get these timestamps from GTKWave for example).

## config.json

The following fields can be set in the config file:

- `file_path`: the path to the VCD file (can be overwritten by the command line argument `-f`)
- `clk_signal`: the name of the signal that should be considered the system clock
- `delimiter`: if this signal is set and the output mode is `latex`, the TikZ figures will be split after this signal has been high for a full clock cycle
- `signals`: the array of the signals that should be plotted (in addition to the clock and the delimiter signal). The signals can contain the following fields:
    + `name`: the name of the signal in the VCD file. This can also be an array, in that case for each cycle the output value will be the maximum of the given signals. This can be useful if for example you want to track whether any of a number of flags have been triggered.
    + `color`: a valid TikZ color, if the output is `latex`, this will be the color of the signal on the figure
    + `label`: the pretty name of the signal in the output, defaults to the name[s] of the signal[s]
    + `type`: type of the signal, possible values for now are `wire` (0/1), `hex`, and `ascii` (default is `wire`)

For a complete example, see the [config file](config.json.example) included in this repository.

## Example

Given the following waveform file:

![](https://i.imgur.com/qEUzd5q.png)

We can issue the following command:

```bash
$ ./vcdvis.py -cycles 20 latex -f /tmp/vcd/jmp_single.vcd > output.tex
```

This means that we want to plot the execution during last 20 clock cycles in the simulation.
In this case, the output will look like the following:

![](https://i.imgur.com/8tz2juR.png)

If we omit the delimiter signal from the config file, we will get the following output (watch out, you might run off at the side of the page):

![](https://i.imgur.com/V82va9C.png)

Alternatively, if we want to plot the execution in ASCII to get a quick look, we can do:

```bash
$ ./vcdvis.py -cycles 20 ascii -f /tmp/vcd/jmp_single.vcd
mclk                 █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █
data memory              ██  ██
program memory       ████    ██████  ████    ████████████  █
peripheral           ██                  ██  ██
instruction         SX…SXT &EDE                MOV #N, r15
exec_done            ██      ██      ██      ██  ██  ██  ███
```
