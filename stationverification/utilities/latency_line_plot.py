'''
A module that contains utilities to extract latency values from HDF5 format
files and report on them
'''
import os
from typing import Optional
import arrow
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from pandas.plotting import register_matplotlib_converters
from datetime import timedelta


def latency_line_plot(
    latencies: list,
    network: str,
    station: str,
    timely_threshold: float,
    location: Optional[str] = None
):
    '''
    Generates a line plot of latency values for each channel of a station

    Parameters
    ----------
    latencies: list of Pandas dataframes
         Each dataframe contains 'network', 'station', 'channel', 'startTime',
         'data_latency'
    station: str
        The station code. For the title and name of file
    network: str
        The network code. For the title and name of file
    channel: str
        The channel code. For the title and name of file
    startdate: date
        The start date of the validation period
    timely_threshold: float
        Maximum latency for a packet to be considered timely
    return
    -------
    No returned values, but will plot the latency line charts for the given
    validation period

    '''
    # The converter was registered by pandas on import. \
    # Future versions of pandas will require you to explicitly register \
    # matplotlib converters.
    register_matplotlib_converters()
    for index, latency_dataframe in enumerate(latencies):
        if not latency_dataframe.empty:
            # Fetch the current date from the dataframe
            startdate = arrow.get(
                latency_dataframe.iloc[0].startTime).format('YYYY-MM-DD')
            startdate_dateobject = arrow.get(startdate, 'YYYY-MM-DD').date()
            if location is None:
                snlc = f'{network}.{station}..'
            else:
                snlc = f'{network}.{station}.{location}.'

            filename = f'{snlc}.{startdate_dateobject}\
.latency_line_plot.png'
            HNN_latencies = \
                latency_dataframe[latency_dataframe
                                  ['channel'] == "HNN"]
            HNE_latencies = \
                latency_dataframe[latency_dataframe
                                  ['channel'] == "HNE"]
            HNZ_latencies = \
                latency_dataframe[latency_dataframe
                                  ['channel'] == "HNZ"]
            # Setting up the figure
            fig, axes = plt.subplots(
                3, 1, sharex=True, sharey=True, figsize=(18.5, 10.5))
            # add a big axis, hide frame
            fig.add_subplot(111, frameon=False)
            # hide tick and tick label of the big axis
            plt.tick_params(labelcolor='none', which='both', top=False,
                            bottom=False, left=False, right=False)
            plt.title(
                f'Latencies for {network}.{station} \n \
    {startdate_dateobject}')
            plt.ylabel("Latency (seconds)")
            threshold = timely_threshold
            if not HNN_latencies.empty:
                axes[0].set_ylim([0, 10])
                # Setting up our data
                x_axis = HNN_latencies.startTime
                x_axis_as_dates = [arrow.get(x).datetime for x in x_axis]
                axes[0].set_xlim(
                    [x_axis_as_dates[0],
                        x_axis_as_dates[0]+timedelta(hours=24)])
                y_axis = HNN_latencies.data_latency

                # Format the dates on the x-axis
                formatter = mdates.DateFormatter("%Y-%m-%d:%H:%M")
                axes[0].xaxis.set_major_formatter(formatter)
                locator = mdates.HourLocator()
                axes[0].xaxis.set_major_locator(locator)
                axes[0].tick_params(axis='x', labelrotation=90)

                # Plotting the data

                axes[0].plot(
                    x_axis_as_dates, y_axis,
                    marker='o', label='HNN Latency values', linewidth=1,
                    markeredgewidth=1,
                    markersize=1, markevery=100000, c="green")
                # Show the grid
                axes[0].set_axisbelow(True)
                axes[0].grid(visible=True, which='both',
                             axis='both', linewidth=0.5)
                # Adding the threshold line
                axes[0].axhline(threshold, color='r', linewidth="1",
                                linestyle='--',
                                label=f"Data Timeliness threshold: \
    {timely_threshold} seconds")

                legend = axes[0].legend(bbox_to_anchor=(1, 1),
                                        loc='upper right', fontsize="9")
            if not HNE_latencies.empty:
                # Setting up the second plot for channel HNE

                axes[1].set_ylim([0, 10])

                # Setting up our data
                x_axis = HNE_latencies.startTime
                x_axis_as_dates = [arrow.get(x).datetime for x in x_axis]
                y_axis = HNE_latencies.data_latency

                # Format the dates on the x-axis
                formatter = mdates.DateFormatter("%Y-%m-%d:%H:%M")
                axes[1].xaxis.set_major_formatter(formatter)
                locator = mdates.HourLocator()
                axes[1].xaxis.set_major_locator(locator)
                axes[1].tick_params(axis='x', labelrotation=90)

                # Plotting the data
                axes[1].plot(
                    x_axis_as_dates, y_axis,
                    marker='o', label='HNE Latency values', linewidth=1,
                    markeredgewidth=1,
                    markersize=1, markevery=100000, c="green")
                # Show the grid
                axes[1].set_axisbelow(True)
                axes[1].grid(visible=True, which='both',
                             axis='both', linewidth=0.5)
                # Adding the threshold line
                axes[1].axhline(threshold, color='r', linewidth="1",
                                linestyle='--',
                                label=f"Data Timeliness threshold: \
    {timely_threshold} seconds")

                legend = axes[1].legend(bbox_to_anchor=(1, 1),
                                        loc='upper right', fontsize="9")
            if not HNZ_latencies.empty:
                # Setting up the third plot for channel HNZ
                axes[2].set_ylim([0, 10])

                # Setting up our data
                x_axis = HNZ_latencies.startTime
                x_axis_as_dates = [arrow.get(x).datetime for x in x_axis]
                y_axis = HNZ_latencies.data_latency

                # Format the dates on the x-axis
                formatter = mdates.DateFormatter("%Y-%m-%d:%H:%M")
                axes[2].xaxis.set_major_formatter(formatter)
                locator = mdates.HourLocator()
                axes[2].xaxis.set_major_locator(locator)
                axes[2].tick_params(axis='x', labelrotation=90)

                # Plotting the data
                axes[2].plot(
                    x_axis_as_dates, y_axis,
                    marker='o', label='HNZ Latency values', linewidth=1,
                    markeredgewidth=1,
                    markersize=1, markevery=100000, c="green")
                # Show the grid
                axes[2].set_axisbelow(True)
                axes[2].grid(visible=True, which='both',
                             axis='both', linewidth=0.5)
                # Adding the threshold line
                axes[2].axhline(threshold, color='r', linewidth="1",
                                linestyle='--',
                                label=f"Data Timeliness threshold: \
    {timely_threshold} seconds")

                legend = axes[2].legend(bbox_to_anchor=(1, 1),
                                        loc='upper right', fontsize="9")
            fig.tight_layout()  # Important for the plot labels to not overlap
            if not os.path.isdir('./stationvalidation_output/'):
                os.mkdir('./stationvalidation_output/')
            plt.savefig(
                f'./stationvalidation_output/{filename}',
                bbox_extra_artists=(legend,),
                bbox_inches='tight')
            plt.close()
