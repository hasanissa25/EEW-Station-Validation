import os
from typing import Optional
import arrow

from datetime import date, timedelta
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.dates as mdates


def plot_clock_offset(network: str,
                      station: str,
                      startdate: date,
                      enddate: date,
                      results: tuple,
                      threshold: float,
                      location: Optional[str] = None):

    number_of_expected_samples = 1440
    x_axis = list(range(0, number_of_expected_samples))

    clock_locked_data, clock_offset_data = results
    font = {'size': 13}
    matplotlib.rc('font', **font)
    if len(clock_locked_data) == len(clock_offset_data):
        for index, clock_offset_data in enumerate(clock_offset_data):
            if(len(clock_offset_data) == number_of_expected_samples):
                # Setting up the figure
                fig, axes = plt.subplots(
                    2, 1, sharex=True, sharey=False, figsize=(18.5, 10.5))
                loc = plticker.MultipleLocator(base=0.5)
                axes[0].yaxis.set_major_locator(loc)

                # add a big axis, hide frame
                fig.add_subplot(111, frameon=False)

                # hide tick and tick label of the big axis
                plt.tick_params(labelcolor='none', which='both', top=False,
                                bottom=False, left=False, right=False)

                # Setting up the current plot
                if location is None:
                    snlc = f'{network}.{station}..'
                else:
                    snlc = f'{network}.{station}.{location}.'
                filename = f'{snlc}.{startdate + timedelta(days=index)}'
                plt.title(
                    f'Timing Error (+/- 0.5 microseconds rounded to 0)\n\
{filename}')
                # Generatre x-axis values as days since startdate
                x_axis_as_dates = [
                    arrow.get(arrow.get(startdate +
                              timedelta(days=index)).datetime +
                              timedelta(minutes=x)).datetime
                    for x in x_axis]

                # First Plot
                axes[0].plot(
                    x_axis_as_dates, clock_offset_data,
                    marker='o', label='Clock offset', linewidth=1,
                    markeredgewidth=1,
                    markersize=1, markevery=60, c="green")
                axes[0].set_ylabel('Timing Error (microseconds)')
                # Format the axis values
                formatter = mdates.DateFormatter("%Y-%m-%d:%H:%M")
                axes[0].xaxis.set_major_formatter(formatter)
                locator = mdates.HourLocator()
                axes[0].xaxis.set_major_locator(locator)
                axes[0].tick_params(axis='x', labelrotation=90)
                axes[0].set_ylim(ymin=-2, ymax=2)

                # Add a grid to the plot to make the symmetry more obvious
                axes[0].set_axisbelow(True)
                axes[0].grid(visible=True, which='both',
                             axis='both', linewidth=0.5)

                # Adding the threshold line
                axes[0].axhline(threshold, color='r', linewidth="1",
                                linestyle='--',
                                label=f'Timing Error Thresholds: \
+/- {threshold} microseconds')
                axes[0].axhline(-threshold, color='r',
                                linewidth="1", linestyle='--')
                # Adding the legend
                legend = axes[0].legend(bbox_to_anchor=(1, 1),
                                        loc='upper right')

                # Second Plot
                axes[1].plot(
                    x_axis_as_dates, clock_locked_data[index],
                    marker='o',  label='0 = Clock is Off, 1 = Clock is Unlocked, 2\
= Clock is Locked', linewidth=1,
                    markeredgewidth=1,
                    markersize=1, markevery=60, c="green")
                # Add a y-label to the axes.
                axes[1].set_ylabel('Clock Status')
                axes[1].tick_params(axis='x', labelrotation=90)

            # labelpad=20
                axes[1].set_ylim(ymin=-1, ymax=3)

                # Add a grid to the plot to make the symmetry more obvious
                axes[1].set_axisbelow(True)
                axes[1].grid(visible=True, which='both',
                             axis='both', linewidth=0.5)
                # this locator puts ticks at regular intervals in steps of\
                #  "base"
                loc = plticker.MultipleLocator(base=1)
                axes[1].yaxis.set_major_locator(loc)
                # Adding the legend
                legend = axes[1].legend(bbox_to_anchor=(1, 1),
                                        loc='upper right')
                # Save the plot to file and then close it so the next \
                # channel's metrics aren't plotted on the same plot
                # Write the plot to the output directory
                if not os.path.isdir("./stationvalidation_output"):
                    os.mkdir('./stationvalidation_output')
                plt.savefig(
                    f'stationvalidation_output/{filename}.timing_error.png',
                    dpi=300, bbox_extra_artists=(legend,), bbox_inches='tight')
                plt.close()
