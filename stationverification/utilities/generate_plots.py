'''
This module generates plots to be used in the station verification process

Functions
---------

plot_psd:
    Plots probabilistic spectral density data against the 2g and 4g noise
    curves

ADC_plot:
    Plots the sample min, max, mean and median so that symetry can be visually
    verified

max_gap_plot:
    Plots the max gap metric returned from ispaq
num_gaps_plot:
    Plots the num_gaps metric returned from ispaq
num_overlaps_plot:
    Plots the num_overlaps metric returned from ispaq
spikes_plot:
    Plots the spikes metric returned from ispaq
percent_availability_plot:
    Plots the percent_availability metric returned from ispaq
pct_above_nhnm_plot:
    Plots the pct_above_nhnm metric returned from ispaq
pct_below_nlnm_plot:
    Plots the pct_below_nlnm metric returned from ispaq
dead_channel_lin_plot:
    Plots the dead_channel_lin metric returned from ispaq
dead_channel_gsn_plot:
    Plots the dead_channel_gsn metric returned from ispaq

'''
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


from .generate_report import StationMetricData
from stationverification import CONFIG


class PlotParameters(dict):
    @property
    def network(self) -> str:
        return self["network"]

    @property
    def station(self) -> str:
        return self["station"]

    @property
    def location(self) -> str:
        return self["location"]

    @property
    def stationMetricData(self) -> StationMetricData:
        return self["stationMetricData"]

    @property
    def start(self) -> date:
        return self["start"]

    @property
    def stop(self) -> date:
        return self["stop"]

    @property
    def channel(self) -> str:
        return self["channel"]

    @property
    def thresholds(self):
        thresholds = ConfigParser()
        thresholds.read(CONFIG)
        return thresholds


def plot_metrics(plotParameters: PlotParameters):
    if not os.path.isdir("./stationvalidation_output"):
        os.mkdir('./stationvalidation_output')
    ADC_plot(plotParameters)
    max_gap_plot(plotParameters)
    num_gaps_plot(plotParameters)
    num_overlaps_plot(plotParameters)

    spikes_plot(plotParameters)
    # percent_availability_plot(plotParameters)
    pct_above_nhnm_plot(plotParameters)
    pct_below_nlnm_plot(plotParameters)

    # dead_channel_lin_plot(plotParameters)
    # dead_channel_gsn_plot(plotParameters)

# Function to graph the ADC plot for visual representation
# Since what values are normal for these metrics seems to differ from one
# channel to the next, it was difficult to come up with thresholds. However,
# according to IRIS documentation, the sample_min and sample_max should be
# roughly symmetrical around sample_mean and sample_median. I thought a good
# way to represent this would be to generate a plot of these values


def ADC_plot(
    plotParameters: PlotParameters
):
    network = plotParameters.network
    station = plotParameters.station
    location = plotParameters.location
    channel = plotParameters.channel
    stationMetricData = plotParameters.stationMetricData
    start = plotParameters.start
    stop = plotParameters.stop

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
    size_of_x_axis = x_axis.size
    size_of_metric_data = len(stationMetricData.get_values(
        'sample_max', network, station, channel))
    if size_of_metric_data == size_of_x_axis:
        ax.scatter(
            x_axis, np.subtract(
                stationMetricData.get_values(
                    'sample_max', network, station, channel),
                stationMetricData.get_values(
                    'sample_mean', network, station, channel)),
            marker='o', label='ADC Counts: max deviation from mean')
        ax.scatter(
            x_axis, np.subtract(
                stationMetricData.get_values(
                    'sample_min', network, station, channel),
                stationMetricData.get_values(
                    'sample_mean', network, station, channel)),
            marker='o', label='ADC Counts: min deviation from mean')
        ax.scatter(
            x_axis, np.subtract(
                stationMetricData.get_values(
                    'sample_median', network, station, channel),
                stationMetricData.get_values(
                    'sample_mean', network, station, channel)),
            marker='o', label='ADC Counts: median deviation from mean')
        ax.scatter(
            x_axis, stationMetricData.get_values(
                'sample_rms', network, station, channel),
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
ADC Count (range: [0, +/- 8,388,608])', pad=20)
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


def num_overlaps_plot(
    plotParameters: PlotParameters
):
    network = plotParameters.network
    station = plotParameters.station
    location = plotParameters.location
    channel = plotParameters.channel
    stationMetricData = plotParameters.stationMetricData
    start = plotParameters.start
    stop = plotParameters.stop
    thresholds = plotParameters.thresholds
    number_overlaps_threshold = thresholds.getint(
        'thresholds', 'num_overlaps', fallback=0)
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
    loc = plticker.MultipleLocator(base=1)
    ax.yaxis.set_major_locator(loc)
    ax.set_ylim([0, 10])
    size_of_x_axis = x_axis.size
    size_of_metric_data = len(stationMetricData.get_values(
        'num_overlaps', network, station, channel))
    if size_of_metric_data == size_of_x_axis:
        bars = ax.bar(
            x_axis, stationMetricData.get_values(
                'num_overlaps', network, station, channel), 0.1)
        ax.bar_label(bars)
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

        ax.set_title(f'{snlc} - Number of overlaps', pad=20)
        plt.ylabel('Overlaps')

        # Add a grid to the plot to make the symmetry more obvious
        ax.set_axisbelow(True)
        plt.grid(visible=True, which='both', axis='both', linewidth=0.5)
        ax.axhline(number_overlaps_threshold, color='r', linewidth="2",
                   linestyle='--',
                   label=f"Maximum number of overlaps threshold: \
{number_overlaps_threshold} overlaps")

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


def num_gaps_plot(
    plotParameters: PlotParameters
):
    network = plotParameters.network
    station = plotParameters.station
    location = plotParameters.location
    channel = plotParameters.channel
    stationMetricData = plotParameters.stationMetricData
    start = plotParameters.start
    stop = plotParameters.stop
    thresholds = plotParameters.thresholds
    num_gaps_threshold = thresholds.getint(
        'thresholds', 'num_gaps', fallback=10)
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
    # this locator puts ticks at regular intervals in setps of "base"
    loc = plticker.MultipleLocator(base=1)
    ax.yaxis.set_major_locator(loc)
    ax.set_ylim([0, 20])

    size_of_x_axis = x_axis.size
    size_of_metric_data = len(stationMetricData.get_values(
        'num_gaps', network, station, channel))
    if size_of_metric_data == size_of_x_axis:
        bars = ax.bar(
            x_axis, stationMetricData.get_values(
                'num_gaps', network, station, channel), 0.1)
        ax.bar_label(bars)

        # Function for formatting the x values to actually be dates

        def timeTicks(x, pos):
            date = start + timedelta(days=x)
            return str(date.isoformat())

        # Format the x axis values to be dates and rotate them 90 degrees
        formatter = matplotlib.ticker.FuncFormatter(timeTicks)
        ax.xaxis.set_major_formatter(formatter)
        plt.xticks(rotation=90)
        locator = mdates.DayLocator()
        ax.xaxis.set_major_locator(locator)
        ax.set_title(f'{snlc} - Number of Gaps', pad=20)
        plt.ylabel('Gaps')

        # Add a grid to the plot to make the symmetry more obvious
        ax.set_axisbelow(True)
        plt.grid(visible=True, which='both', axis='both', linewidth=0.5)
        # Adding the threshold line
        ax.axhline(num_gaps_threshold, color='r', linewidth="1",
                   linestyle='--',
                   label=f"Maximum number of gaps threshold: \
{num_gaps_threshold} gaps")

        legend = ax.legend(bbox_to_anchor=(1, 1),
                           loc='upper right', fontsize="9")
        # Save the plot to file and then close it so the next channel's metrics
        # aren't plotted on the same plot
        if start == stop - timedelta(days=1):
            plot_filename = f'{snlc}.{start}.num_gaps'
        else:
            plot_filename = f'{snlc}.{start}_\
{(stop + timedelta(days=-1))}.num_gaps'
        # Write the plot to the output directory
        plt.savefig(f'stationvalidation_output/{plot_filename}.png',
                    dpi=300, bbox_extra_artists=(legend,), bbox_inches='tight')
        logging.info(f'{plot_filename} created.')
    plt.close()


def max_gap_plot(
    plotParameters: PlotParameters
):
    network = plotParameters.network
    station = plotParameters.station
    location = plotParameters.location
    channel = plotParameters.channel
    stationMetricData = plotParameters.stationMetricData
    start = plotParameters.start
    stop = plotParameters.stop
    thresholds = plotParameters.thresholds
    size_of_gaps_threshold = thresholds.getint(
        'thresholds', 'max_gap', fallback=2)
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
    # this locator puts ticks at regular intervals in setps of "base"
    loc = plticker.MultipleLocator(base=1)
    ax.yaxis.set_major_locator(loc)
    ax.set_ylim([0, 10])

    size_of_x_axis = x_axis.size
    size_of_metric_data = len(stationMetricData.get_values(
        'max_gap', network, station, channel))
    if size_of_metric_data == size_of_x_axis:
        bars = ax.bar(
            x_axis, stationMetricData.get_values(
                'max_gap', network, station, channel), 0.1)
        # Function for formatting the x values to actually be dates
        ax.bar_label(bars)

        def timeTicks(x, pos):
            date = start + timedelta(days=x)
            return str(date.isoformat())

        # Format the x axis values to be dates and rotate them 90 degrees
        formatter = matplotlib.ticker.FuncFormatter(timeTicks)
        ax.xaxis.set_major_formatter(formatter)
        locator = mdates.DayLocator()
        ax.xaxis.set_major_locator(locator)
        plt.xticks(rotation=90)

        ax.set_title(f'{snlc} - Max Gaps', pad=20)
        plt.ylabel('Gap size (Seconds)')

        # Add a grid to the plot to make the symmetry more obvious
        ax.set_axisbelow(True)
        plt.grid(visible=True, which='both', axis='both', linewidth=0.5)
        ax.axhline(size_of_gaps_threshold, color='r', linewidth="1",
                   linestyle='--',
                   label=f"Maximum size of gaps: \
{size_of_gaps_threshold} seconds")

        legend = ax.legend(bbox_to_anchor=(1, 1),
                           loc='upper right', fontsize="9")
        # Save the plot to file and then close it so the next channel's metrics
        # aren't plotted on the same plot
        if start == stop - timedelta(days=1):
            plot_filename = f'{snlc}.{start}.max_gap'
        else:
            plot_filename = f'{snlc}.{start}_\
{(stop + timedelta(days=-1))}.max_gap'
        # Write the plot to the output directory
        plt.savefig(f'stationvalidation_output/{plot_filename}.png',
                    dpi=300, bbox_extra_artists=(legend,), bbox_inches='tight')
        logging.info(f'{plot_filename} created.')
    plt.close()


def spikes_plot(
    plotParameters: PlotParameters
):
    thresholds = ConfigParser()
    thresholds.read(CONFIG)
    spikes_threshold = thresholds.getint(
        'thresholds', 'spikes', fallback=0)
    network = plotParameters.network
    station = plotParameters.station
    location = plotParameters.location
    channel = plotParameters.channel
    stationMetricData = plotParameters.stationMetricData
    start = plotParameters.start
    stop = plotParameters.stop
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
    # this locator puts ticks at regular intervals in setps of "base"
    loc = plticker.MultipleLocator(base=1.0)
    ax.yaxis.set_major_locator(loc)
    ax.set_ylim([0, 10])

    size_of_x_axis = x_axis.size
    size_of_metric_data = len(stationMetricData.get_values(
        'spikes', network, station, channel))
    if size_of_metric_data == size_of_x_axis:
        bars = ax.bar(
            x_axis, stationMetricData.get_values(
                'spikes', network, station, channel), 0.1)
        ax.bar_label(bars)

        ax.axhline(spikes_threshold, color='r', linewidth="2",
                   linestyle='--',
                   label=f"Maximum number of spikes threshold: \
{spikes_threshold} spikes")

        legend = ax.legend(bbox_to_anchor=(1, 1),
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

        ax.set_title(f'{snlc} - Spikes', pad=20)
        plt.ylabel('Spikes')

        # Add a grid to the plot to make the symmetry more obvious
        ax.set_axisbelow(True)
        plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

        # Save the plot to file and then close it so the next channel's metrics
        # aren't plotted on the same plot
        if start == stop - timedelta(days=1):
            plot_filename = f'{snlc}.{start}.spikes'
        else:
            plot_filename = f'{snlc}.{start}_\
{(stop + timedelta(days=-1))}.spikes'
        # Write the plot to the output directory
        plt.savefig(f'stationvalidation_output/{plot_filename}.png',
                    dpi=300, bbox_extra_artists=(legend,), bbox_inches='tight')
        logging.info(f'{plot_filename} created.')
    plt.close()


def pct_above_nhnm_plot(
    plotParameters: PlotParameters
):
    network = plotParameters.network
    station = plotParameters.station
    location = plotParameters.location
    channel = plotParameters.channel
    stationMetricData = plotParameters.stationMetricData
    start = plotParameters.start
    stop = plotParameters.stop
    thresholds = plotParameters.thresholds
    pct_above_nhnm_threshold = thresholds.getint(
        'thresholds', 'pct_above_nhnm', fallback=40)
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
    # this locator puts ticks at regular intervals in setps of "base"
    loc = plticker.MultipleLocator(base=10.0)
    ax.yaxis.set_major_locator(loc)
    ax.set_ylim([0, 100])

    size_of_x_axis = x_axis.size
    size_of_metric_data = len(stationMetricData.get_values(
        'pct_above_nhnm', network, station, channel))
    y_axis = stationMetricData.get_values(
        'pct_above_nhnm', network, station, channel)
    y_axis_rounded = list(map(lambda value: float(round(value, 1)), y_axis))
    if size_of_metric_data == size_of_x_axis:
        bars = ax.bar(
            x_axis, y_axis_rounded, width=0.1)
        ax.bar_label(bars)

        # legend = plt.legend(fancybox=True, framealpha=0.2,
        #                     loc='upper right', fontsize="9")
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

        ax.set_title(
            f'{snlc} - \
Percent above New High Noise Model', pad=20)
        plt.ylabel('Percentage')
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
        # Add a grid to the plot to make the symmetry more obvious
        ax.set_axisbelow(True)
        plt.grid(visible=True, which='both', axis='both', linewidth=0.5)
        ax.axhline(pct_above_nhnm_threshold, color='r', linewidth="1",
                   linestyle='--',
                   label=f"Percent Above New High Noise Modal threshold: \
{pct_above_nhnm_threshold}%")

        legend = ax.legend(bbox_to_anchor=(1, 1),
                           loc='upper right', fontsize="9")
        # Save the plot to file and then close it so the next channel's metrics
        # aren't plotted on the same plot
        if start == stop - timedelta(days=1):
            plot_filename = f'{snlc}.{start}\
.pct_above_nhnm'
        else:
            plot_filename = f'{snlc}.{start}_\
{(stop + timedelta(days=-1))}.pct_above_nhnm'
        # Write the plot to the output directory
        plt.savefig(f'stationvalidation_output/{plot_filename}.png',
                    dpi=300, bbox_extra_artists=(legend,), bbox_inches='tight')
        logging.info(f'{plot_filename} created.')
    plt.close()


def pct_below_nlnm_plot(
    plotParameters: PlotParameters
):
    thresholds = ConfigParser()
    thresholds.read(CONFIG)
    below_nlnm_threshold = thresholds.getint(
        'thresholds', 'pct_below_nlnm', fallback=0)
    network = plotParameters.network
    station = plotParameters.station
    location = plotParameters.location
    channel = plotParameters.channel
    stationMetricData = plotParameters.stationMetricData
    start = plotParameters.start
    stop = plotParameters.stop
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
    # this locator puts ticks at regular intervals in setps of "base"
    loc = plticker.MultipleLocator(base=10.0)
    ax.yaxis.set_major_locator(loc)
    ax.set_ylim([0, 100])

    size_of_x_axis = x_axis.size
    size_of_metric_data = len(stationMetricData.get_values(
        'pct_below_nlnm', network, station, channel))
    y_axis = stationMetricData.get_values(
        'pct_below_nlnm', network, station, channel)
    y_axis_rounded = list(map(lambda value: float(round(value, 1)), y_axis))

    if size_of_metric_data == size_of_x_axis:
        bars = ax.bar(
            x_axis, y_axis_rounded, 0.1)
        ax.bar_label(bars)
        ax.axhline(below_nlnm_threshold, color='r', linewidth="2",
                   linestyle='--',
                   label=f"Percent Below New Low Noise Modal threshold: \
{below_nlnm_threshold}%")

        legend = ax.legend(bbox_to_anchor=(1, 1),
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

        ax.set_title(
            f'{snlc} - \
Percent below New Low Noise Model', pad=20)
        plt.ylabel('Percentage')
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
        # Add a grid to the plot to make the symmetry more obvious
        ax.set_axisbelow(True)
        plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

        # Save the plot to file and then close it so the next channel's metrics
        # aren't plotted on the same plot
        if start == stop - timedelta(days=1):
            plot_filename = f'{snlc}.{start}\
.pct_below_nlnm'
        else:
            plot_filename = f'{snlc}.{start}_\
{(stop + timedelta(days=-1))}.pct_below_nlnm'
        # Write the plot to the output directory
        plt.savefig(f'stationvalidation_output/{plot_filename}.png',
                    dpi=300, bbox_extra_artists=(legend,), bbox_inches='tight')
        logging.info(f'{plot_filename} created.')
    plt.close()
