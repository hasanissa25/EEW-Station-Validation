import os
import warnings

from typing import Optional

import numpy as np
from datetime import date, timedelta

import matplotlib.pyplot as plt
import matplotlib
from pandas.core.frame import DataFrame


warnings.filterwarnings("ignore")


def latency_log_plot(
    latencies: DataFrame,
    station: str,
    startdate: date,
    enddate: date,
    typeofinstrument: str,
    network: str,
    timely_threshold: float,
    location: Optional[str] = None,
    total_availability: Optional[float] = None
):
    '''
    Generates a log plot of latency values for a station

    Parameters
    ----------
    latencies: Pandas dataframe
         Contains 'network', 'station', 'channel', 'startTime', 'data_latency'
    station: str
        The station code. For the title and name of file
    network: str
        The network code. For the title and name of file
    channel: str
        The channel code. For the title and name of file
    startdate: date
        The start date of the validation period
    enddate: date
        The end date of the validation period
    typeofinstrument: str
        Used to annotate the plot
    timely_threshold: float
        Maximum latency for a packet to be considered timely

    return
    -------
    No returned values, but will plot the latency log graph for the given
    validation period

    '''

    # Setting up the file name and plot name based on whether its a one day \
    # validation period or not to know if we include end date or not
    filename = ""
    if location is None:
        snlc = f'{network}.{station}..'
    else:
        snlc = f'{network}.{station}.{location}.'
    if startdate == enddate - timedelta(days=1):
        filename = f'{snlc}.{startdate}.latency_log_plot.png'
        plottitle = f'Latencies for {network}.{station} \n {startdate}'
    else:
        filename = f'{snlc}.{startdate}_\
{enddate - timedelta(days=1)}.latency_log_plot.png'
        plottitle = f'Latencies for {network}.{station} \n {startdate} to\
 {enddate - timedelta(days=1)}'

    # Setting up the figure
    font = {'size': 13}

    matplotlib.rc('font', **font)
    fig = plt.figure()
    fig.set_size_inches(18.5, 10.5)

    ax1 = fig.add_subplot(111)
    ax1.set_title(plottitle)  # Add a title to the axes.
    ax1.set_xlabel('Latency (seconds)', fontsize=13)
    ax1.set_ylabel('Occurrences', fontsize=13)  # Add a y-label to the axes.
    ax1.set_yscale('log')
    if typeofinstrument == "APOLLO":
        note_content = f'Type of Instrument: TitanSMA\n\
Data availability: {total_availability}%\n\
Average latency:{round(latencies.data_latency.mean(),2)} seconds\n\
Standard deviation: {round(np.std(latencies.data_latency),1)}'
    elif typeofinstrument == "GURALP":
        note_content = f'Type of Instrument: Fortimus\n\
Average latency:{round(latencies.data_latency.mean(),2)} seconds\n\
Standard deviation: {round(np.std(latencies.data_latency),1)}'

    ax1.text(0.9, 0.8, note_content, style='italic', fontsize=12,
             transform=ax1.transAxes,
             bbox={'facecolor': 'grey', 'alpha': 0.5, 'pad': 6})
    ax1.set_axisbelow(True)
    plt.grid(visible=True, which='both', axis='both', linewidth=0.5)

    ax1.hist(
        latencies.data_latency,
        bins=[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5,
              5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10],
        ec='black',
    )

    # Adding the threshold line
    threshold = timely_threshold
    plt.axvline(threshold, color='r', linestyle='--', linewidth=1,
                label=f"Data Timeliness threshold: \
{timely_threshold} seconds")
    legend = ax1.legend(bbox_to_anchor=(1.1, 1),
                        loc='upper right', fontsize="13")
    plt.show()

    fig.tight_layout()  # Important for the plot labels to not overlap
    if not os.path.isdir('./stationvalidation_output/'):
        os.mkdir('./stationvalidation_output/')
    plt.savefig(
        f'./stationvalidation_output/{filename}',
        bbox_extra_artists=(legend,),
        bbox_inches='tight')
    plt.close()
