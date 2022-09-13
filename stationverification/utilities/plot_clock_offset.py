import os
import itertools
import re
import obspy
import numpy as np

from datetime import date, timedelta
from typing import Any, List
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_clock_offset(
        list_of_streams: List,
        clock_offset_threshold_in_microseconds: float,
        network: str,
        station: str,
        startdate: date,
        enddate: date,
        location: Any = None):

    for stream in list_of_streams:
        create_line_plot(
            stream=stream,
            clock_offset_threshold_in_microseconds=clock_offset_threshold_in_microseconds  # noqa
        )
    create_bar_graph(
        list_of_streams=list_of_streams,
        clock_offset_threshold_in_microseconds=clock_offset_threshold_in_microseconds,  # noqa
        network=network,
        station=station,
        startdate=startdate,
        enddate=enddate,
        location=location
    )


def create_line_plot(stream: obspy.Stream,
                     clock_offset_threshold_in_microseconds: float):
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

    # Setting up the data and threshold
    '''
        The raw channel values are in counts and should be multiplied
        by the calibration value of 24.112654 to get a number of
        nanoseconds of offset. The timing quality will remain
        'fine locked' as long as the time offset from the time source
        is within half of a sample period. The system is operating in
        5000 samples per second so as long as the time difference
        is kept within 100000ns (1s / 5000sps / 2) there is no threat
        to the sample timing precision.
        '''
    offsets = (abs((trace.data * 24.112654) / 1000))

    # Setting up the figure
    fig = plt.figure(figsize=(18.5, 10.5))
    axes = fig.add_subplot(1, 1, 1)
    axes.plot(trace.times("matplotlib"), offsets, "b-")
    plt.title(
        f'Clock Offset\n\
    {filename}')
    # Formatting the X axis
    formatter = mdates.DateFormatter("%Y-%m-%d:%H:%M")
    axes.xaxis.set_major_formatter(formatter)
    locator = mdates.HourLocator()
    axes.xaxis.set_major_locator(locator)
    axes.tick_params(axis='x', labelrotation=90)

    # Formatting the Y axis
    axes.set_ylim(ymin=0, ymax=110)
    axes.set_ylabel('Clock Offset (microseconds)')
    # Adding a grid
    # axes.set_axisbelow(True)
    axes.grid(visible=True, which='both',
              axis='both', linewidth=0.5)

    # Adding the threshold line
    axes.axhline(clock_offset_threshold_in_microseconds, color='r',
                 linewidth="1",
                 linestyle='--',
                 label=f'Clock Offset Threshold: \
{clock_offset_threshold_in_microseconds} microseconds')
    # Adding a legend
    legend = axes.legend(bbox_to_anchor=(1, 1),
                         loc='upper right', fontsize="9")
    if not os.path.isdir("./stationvalidation_output"):
        os.mkdir('./stationvalidation_output')
    plt.savefig(
        f'stationvalidation_output/{filename}.clock_offset_line_plot.png',
        dpi=300, bbox_extra_artists=(legend,), bbox_inches='tight')
    plt.close()


def create_bar_graph(list_of_streams: np.ndarray,
                     clock_offset_threshold_in_microseconds: float,
                     network: str,
                     station: str,
                     startdate: date,
                     enddate: date,
                     location: Any = None
                     ):
    # Setting up the data
    list_of_clock_offsets = []
    for stream in list_of_streams:
        list_of_clock_offsets.append(stream[0].data)
    flat_list_of_clock_offsets = list(itertools.chain(*list_of_clock_offsets))

    # Setting up the file name and plot name based on whether its a one day \
    # validation period or not to know if we include end date or not
    filename = ""
    if location is None:
        snlc = f'{network}.{station}..'
    else:
        snlc = f'{network}.{station}.{location}.'
    if startdate == enddate - timedelta(days=1):
        filename = f'{snlc}.{startdate}.clock_offset_log_plot.png'
        plottitle = f'Clock Offset log plot for {network}.{station} \
\n {startdate}'
    else:
        filename = f'{snlc}.{startdate}_\
{enddate - timedelta(days=1)}.clock_offset_log_plot.png'
        plottitle = f'Clock Offset log plot for {network}.{station} \n {startdate} to\
 {enddate - timedelta(days=1)}'

    # Setting up the figure
    fig = plt.figure()
    fig.set_size_inches(18.5, 10.5)

    ax1 = fig.add_subplot(111)
    ax1.set_title(plottitle)  # Add a title to the axes.
    ax1.set_xlabel('Clock Offset (microseconds)', fontsize=13)
    ax1.set_ylabel('Occurrences', fontsize=13)  # Add a y-label to the axes.
    ax1.set_axisbelow(True)
    plt.grid(visible=True, which='both', axis='both', linewidth=0.5)
    ax1.set_yscale('log')

    # Adding the threshold line
    threshold = clock_offset_threshold_in_microseconds
    plt.axvline(threshold, color='r', linestyle='--', linewidth=1,
                label=f"Data Timeliness threshold: \
{clock_offset_threshold_in_microseconds} seconds")
    legend = ax1.legend(bbox_to_anchor=(1.1, 1),
                        loc='upper right', fontsize="13")

    fig.tight_layout()  # Important for the plot labels to not overlap

    # Adding the data
    ax1.hist(flat_list_of_clock_offsets, ec='black')

    if not os.path.isdir('./stationvalidation_output/'):
        os.mkdir('./stationvalidation_output/')
    plt.savefig(
        f'./stationvalidation_output/{filename}',
        bbox_extra_artists=(legend,),
        bbox_inches='tight')
    plt.close()
