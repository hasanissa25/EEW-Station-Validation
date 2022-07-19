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

    # Create plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Plot the min, max and median normalized to the mean. This makes it
    # easier to see how symmetrical it is.
    ax.scatter(
        x_axis, [4000, 2000, 3500, 2000, 1500, 1000, 500, 4500, 5000, 2000],
        marker='o', label='ADC Counts: max deviation from mean')
    ax.scatter(
        x_axis, [-600, -250, -9000, -3500, -
                 4500, -1500, -1000, -6000, -450, -2500],
        marker='o', label='ADC Counts: min deviation from mean')
    ax.scatter(
        x_axis, [-350, -400, -500, -20, -490, -900, -1000, -200, -50, -700],
        marker='o', label='ADC Counts: median deviation from mean')
    ax.scatter(
        x_axis, [100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        marker='o', label='Sample RMS')

    legend = plt.legend(fancybox=True, framealpha=0.2,
                        bbox_to_anchor=(1.4, 1.0),
                        loc='upper right', fontsize="9")

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
    plt.title(
        f'{snlc} - \
ADC Count (range: [0, +/- 8,388,608])')
    plt.ylabel('Amplitude value')
    ax.set_axisbelow(True)
    plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

    # Save the plot to file and then close it so the next channel's metrics
    # aren't plotted on the same plot
    if start == stop - timedelta(days=1):
        plot_filename = f'{snlc}.{start}.adc_count'
    else:
        plot_filename = f'{snlc}.{start}_\
{(stop + timedelta(days=-1))}.adc_count'
    # Write the plot to the output directory
    plt.savefig(f'stationvalidation_output/{plot_filename}.png',
                dpi=300,
                bbox_extra_artists=(legend,),
                bbox_inches='tight')
    plt.close()


test_generate_sample_plot()
