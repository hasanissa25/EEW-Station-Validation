import os
import warnings
import logging
import matplotlib
import numpy as np

from typing import List, Optional

from datetime import date, timedelta

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.ticker as plticker
import matplotlib.dates as mdates

from pandas.plotting import register_matplotlib_converters
from stationverification.utilities.generate_report import StationMetricData

from stationverification.utilities.get_timely_availability_arrays\
    import get_timely_availability_arrays


warnings.filterwarnings("ignore")


def timely_availability_plot(
    latencies: List,
    station: str,
    startdate: date,
    enddate: date,
    network: str,
    timely_threshold: float,
    stationMetricData: StationMetricData,
    location: Optional[str] = None
):
    font = {'size': 13}
    matplotlib.rc('font', **font)
    percent_availability_array_HNN = (stationMetricData.get_values(
        'percent_availability', network, station, "HNN"))
    percent_availability_array_HNN_rounded = list(
        map(lambda value: float(round(value, 2)),
            percent_availability_array_HNN))
    percent_availability_array_HNE = (stationMetricData.get_values(
        'percent_availability', network, station, "HNZ"))
    percent_availability_array_HNE_rounded = list(
        map(lambda value: float(round(value, 2)),
            percent_availability_array_HNE))
    percent_availability_array_HNZ = (stationMetricData.get_values(
        'percent_availability', network, station, "HNE"))
    percent_availability_array_HNZ_rounded = list(
        map(lambda value: float(round(value, 2)),
            percent_availability_array_HNZ))
    register_matplotlib_converters()
    HNN_timely_availability_percentage_array, \
        HNE_timely_availability_percentage_array,\
        HNZ_timely_availability_percentage_array,\
        timely_availability_percentage_array_days_axis = \
        get_timely_availability_arrays(
            latencies=latencies, threshold=timely_threshold)
    # Setting up the figure
    filename = ""
    if location is None:
        snlc = f'{network}.{station}..'
    else:
        snlc = f'{network}.{station}.{location}.'
    if startdate == enddate - timedelta(days=1):
        filename = f'{snlc}.{startdate}\
.timely_availability_plot.png'
    else:
        filename = f'{snlc}.{startdate}_\
{enddate - timedelta(days=1)}.timely_availability_plot.png'

    fig, axes = plt.subplots(
        3, 1, sharex=True, sharey=True, figsize=(18.5, 10.5))

    # add a big axis, hide frame
    fig.add_subplot(111, frameon=False)

    # hide tick and tick label of the big axis
    plt.tick_params(labelcolor='none', which='both', top=False,
                    bottom=False, left=False, right=False)
    plt.title(
        f'Timely Availability [%]\n{network}.{station} {startdate}_{enddate}',
        pad=20)

    axes[1].set_ylabel("Timely availability [%]", fontsize=20)

    # Setting up our X-axis data
    x_axis = timely_availability_percentage_array_days_axis
    number_of_days = len(x_axis)
    number_of_days_as_array = np.arange(number_of_days)
    width_between_ticks = 0.4
    bar_width = 0.4

    if len(HNN_timely_availability_percentage_array) == len(x_axis) and\
        len(HNE_timely_availability_percentage_array) == len(x_axis) and\
            len(HNE_timely_availability_percentage_array) == len(x_axis) and \
            len(x_axis) != 0:
        # Format the dates on the x-axis
        def timeTicks(x, pos):
            date = startdate + timedelta(days=x)
            return str(date.isoformat())
        formatter = matplotlib.ticker.FuncFormatter(timeTicks)
        axes[0].xaxis.set_major_formatter(formatter)
        # Format the x axis values to be dates and rotate them 90 degrees
        # formatter = mdates.DateFormatter("%Y-%m-%d")
        # axes[0].xaxis.set_major_formatter(formatter)
        locator = mdates.DayLocator()
        axes[0].xaxis.set_major_locator(locator)
        axes[0].tick_params(axis='x', labelrotation=90)
        axes[0].set_xticks(number_of_days_as_array+(width_between_ticks/2))

        # Format the Y-axis values to be percentages
        axes[0].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
        loc = plticker.MultipleLocator(base=10)
        axes[0].yaxis.set_major_locator(loc)

        # Plotting the data
        y_axis = [float(round(a*(b/100), 2)) for a, b in
                  zip(HNN_timely_availability_percentage_array,
                      percent_availability_array_HNN_rounded)]

        # axes[0].bar(x_axis, [100], color="red")
        # axes[0].bar(x_axis, y_axis,
        #             label='HNN Timely Availability [%]')
        if len(number_of_days_as_array) == len(y_axis) and \
                len(number_of_days_as_array) == len(
                    percent_availability_array_HNN_rounded):
            axes[0].bar(number_of_days_as_array, y_axis,
                        bar_width, label='HNN Timely Availability [%]',
                        color="blue")
            axes[0].bar(number_of_days_as_array + width_between_ticks,
                        percent_availability_array_HNN_rounded,
                        bar_width, label='HNN Percent Availability [%]',
                        color="green")
            for bars in axes[0].containers:
                axes[0].bar_label(bars)
            # Show the grid
            axes[0].set_axisbelow(True)
            axes[0].grid(visible=True, which='both',
                         axis='both', linewidth=0.5)
            axes[0].set_ylim(ymin=0, ymax=100)

        # # Second plot
        # Setting up our data
        # Format the Y-axis values to be percentages
        axes[1].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
        loc = plticker.MultipleLocator(base=10)
        axes[1].yaxis.set_major_locator(loc)
        y_axis = [float(round(a*(b/100), 2)) for a, b in
                  zip(HNE_timely_availability_percentage_array,
                      percent_availability_array_HNE_rounded)]
        if len(number_of_days_as_array) == len(y_axis) and \
                len(number_of_days_as_array) == len(
                    percent_availability_array_HNE_rounded):
            axes[1].bar(number_of_days_as_array, y_axis,
                        bar_width, label='HNE Timely Availability [%]',
                        color="blue")
            axes[1].bar(number_of_days_as_array + width_between_ticks,
                        percent_availability_array_HNE_rounded,
                        bar_width, label='HNE Percent Availability [%]',
                        color="green")
            for bars in axes[1].containers:
                axes[1].bar_label(bars)
            # Show the grid
            axes[1].set_axisbelow(True)
            axes[1].grid(visible=True, which='both',
                         axis='both', linewidth=0.5)
            axes[1].set_ylim(ymin=0, ymax=100)

        # # Third plot
        # Setting up our data
        axes[2].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
        loc = plticker.MultipleLocator(base=10)
        axes[2].yaxis.set_major_locator(loc)
        y_axis = [float(round(a*(b/100), 2)) for a, b in
                  zip(HNZ_timely_availability_percentage_array,
                      percent_availability_array_HNZ_rounded)]
        if len(number_of_days_as_array) == len(y_axis) and \
                len(number_of_days_as_array) == len(
                    percent_availability_array_HNZ_rounded):
            axes[2].bar(number_of_days_as_array, y_axis,
                        bar_width, label='HNZ Timely Availability [%]',
                        color="blue")
            axes[2].bar(number_of_days_as_array + width_between_ticks,
                        percent_availability_array_HNZ_rounded,
                        bar_width, label='HNZ Percent Availability [%]',
                        color="green")
            for bars in axes[2].containers:
                axes[2].bar_label(bars)

            # Show the grid
            axes[2].set_axisbelow(True)
            axes[2].grid(visible=True, which='both',
                         axis='both', linewidth=0.5)
            axes[2].set_ylim(ymin=0, ymax=100)

        legend = axes[0].legend(bbox_to_anchor=(1.1, 1),
                                loc='upper right', fontsize="10")
        legend = axes[1].legend(bbox_to_anchor=(1.1, 1),
                                loc='upper right')
        legend = axes[2].legend(bbox_to_anchor=(1.1, 1),
                                loc='upper right')
        fig.tight_layout()  # Important for the plot labels to not overlap
        if not os.path.isdir('./stationvalidation_output/'):
            os.mkdir('./stationvalidation_output/')
        plt.savefig(
            f'./stationvalidation_output/{filename}',
            bbox_extra_artists=(legend,),
            bbox_inches='tight')
        plt.close()
    else:
        logging.warning(
            "Skipping Timely Availability. Please double check the latency\
 files")
