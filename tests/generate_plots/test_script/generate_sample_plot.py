# flake8:noqa
import subprocess
from configparser import ConfigParser
import logging
import os
from datetime import date, timedelta
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.ticker as plticker
import matplotlib.dates as mdates

from stationverification import CONFIG

from datetime import date


def test_generate_sample_plot():
    subprocess.getoutput(
        "rm -rf 'stationvalidation_output'")
    subprocess.getoutput(
        "mkdir stationvalidation_output")
    thresholds = ConfigParser()
    thresholds.read(CONFIG)
    ########################################################################################
    threshold_value = 10
    ########################################################################################
    network = "QW"
    station = "QCC02"
    channel = "HNE"
    location = None
    start = date(2022, 4, 1)
    stop = date(2022, 4, 11)

    if location is None:
        snlc = f'{network}.{station}..{channel}'
    else:
        snlc = f'{network}.{station}.{location}.{channel}'

    # Generatre x-axis values as days since startdate
    difference = stop - start
    x_axis = np.arange(0, difference.days, 1)
    y_axis = [99.8754, 99.8754, 99.8754, 99.8754, 99.8754,
              99.8754, 99.8754, 99.8754, 99.8754, 99.8754]
    y_axis_rounded = list(map(lambda value: float(round(value, 2)), y_axis))
    # Create plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    loc = plticker.MultipleLocator(base=10.0)
    ax.yaxis.set_major_locator(loc)
    ########################################################################################
    ax.set_ylim([0, 100])
    bars = ax.bar(
        x_axis, y_axis_rounded, 0.1)
    ax.bar_label(bars)
    ########################################################################################

    # Function for formatting the x values to actually be dates

    def timeTicks(x, pos):
        date = start + timedelta(days=x)
        return str(date.isoformat())

    # Format the x axis values to be dates and rotate them 90 degrees
    formatter = matplotlib.ticker.FuncFormatter(timeTicks)
    ax.xaxis.set_major_formatter(formatter)
    locator = mdates.DayLocator()
    ax.xaxis.set_major_locator(locator)
    plt.xticks(rotation=90)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))

    ########################################################################################
    ax.set_title(f'{snlc} - Number of Gaps', pad=20)
    plt.ylabel('Gaps')
    ########################################################################################

    # Add a grid to the plot to make the symmetry more obvious
    ax.set_axisbelow(True)
    plt.grid(visible=True, which='both', axis='both', linewidth=0.5)
    ########################################################################################
    # TODO: New
    ax.axhline(threshold_value, color='r', linewidth="2",
               linestyle='--',
               label=f"Maximum number of gaps threshold: \
{threshold_value} gaps")
    ########################################################################################

    legend = ax.legend(bbox_to_anchor=(1, 1),
                       loc='upper right', fontsize="9")
    # Save the plot to file and then close it so the next channel's metrics
    # aren't plotted on the same plot
    if start == stop - timedelta(days=1):
        plot_filename = f'{snlc}.{start}\
.num_overlaps'
    else:
        plot_filename = f'{snlc}.{start}_\
{(stop + timedelta(days=-1))}.num_overlaps'

    # Write the plot to the output directory
    plt.savefig(f'stationvalidation_output/{plot_filename}.png',
                dpi=300, bbox_extra_artists=(legend,), bbox_inches='tight')
    logging.info(f'{plot_filename} created.')
    plt.close()


test_generate_sample_plot()
