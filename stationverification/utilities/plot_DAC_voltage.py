import os
import re
from typing import List

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import obspy


def plot_DAC_voltage(list_of_streams: List):

    for stream in list_of_streams:
        create_line_plot(stream=stream)


def create_line_plot(stream: obspy.Stream):
    trace = stream[0]
    # Setting up name of plot
    network = trace.stats.network
    station = trace.stats.station
    location = trace.stats.location
    startingdate = re.findall("([^T]*)", f'{trace.stats.starttime}')[0]
    if location is None:
        snlc = f'{network}.{station}..'
    else:
        snlc = f'{network}.{station}.{location}.'
    filename = f'{snlc}.{startingdate}'

    # Setting up the figure
    fig = plt.figure(figsize=(18.5, 10.5))
    axes = fig.add_subplot(1, 1, 1)
    axes.plot(trace.times("matplotlib"), trace, "b-")
    plt.title(
        f'DAC Voltage\n\
    {filename}')
    # Formatting the X axis
    formatter = mdates.DateFormatter("%Y-%m-%d:%H:%M")
    axes.xaxis.set_major_formatter(formatter)
    locator = mdates.HourLocator()
    axes.xaxis.set_major_locator(locator)
    axes.tick_params(axis='x', labelrotation=90)

    # Formatting the Y axis
    axes.set_ylabel('Counts')
    # Adding a grid
    # axes.set_axisbelow(True)
    axes.grid(visible=True, which='both',
              axis='both', linewidth=0.5)

    # Adding a legend
    legend = axes.legend(bbox_to_anchor=(1, 1),
                         loc='upper right', fontsize="9")
    if not os.path.isdir("./stationvalidation_output"):
        os.mkdir('./stationvalidation_output')
    plt.savefig(
        f'stationvalidation_output/{filename}.dac_voltage_plot.png',
        dpi=300, bbox_extra_artists=(legend,), bbox_inches='tight')
    plt.close()
