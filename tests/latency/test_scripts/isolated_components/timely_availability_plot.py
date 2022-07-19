from datetime import date, timedelta

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import matplotlib.ticker as plticker

startdate = date(2022, 3, 20)
enddate = date(2022, 3, 30)
HNN_timely_availability_percentage_array = [
    99, 95, 95, 95, 95, 99, 95, 95, 95, 95]
HNE_timely_availability_percentage_array = [
    99, 95, 95, 95, 95, 99, 95, 95, 95, 95]
HNZ_timely_availability_percentage_array = [
    99, 95, 95, 95, 95, 99, 95, 95, 95, 95]
filename = 'timely_availability_plot_test.png'
# Setting up the figure
fig, axes = plt.subplots(
    3, 1, sharex=True, sharey=True, figsize=(18.5, 10.5))
# add a big axis, hide frame
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', which='both', top=False,
                bottom=False, left=False, right=False)
plt.title(
    'Timely availability [%]')
plt.ylabel("Timely availability")

# Setting up our X-axis data
difference = enddate - startdate
x_axis = np.arange(0, difference.days, 1)
if len(HNN_timely_availability_percentage_array) == x_axis.size:
    # Function for formatting the x values to actually be dates

    def timeTicks(x, pos):
        date = startdate + timedelta(days=x)
        return str(date.isoformat())

    # Format the x axis values to be dates and rotate them 90 degrees
    formatter = matplotlib.ticker.FuncFormatter(timeTicks)
    axes[0].xaxis.set_major_formatter(formatter)
    axes[0].tick_params(axis='x', labelrotation=90)
    # Format the Y-axis values to be percentages
    axes[0].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
    loc = plticker.MultipleLocator(base=10.0)
    axes[0].yaxis.set_major_locator(loc)
    # Plotting the data
    y_axis = HNN_timely_availability_percentage_array
    axes[0].bar(x_axis, y_axis, label='HNN Latency values')
    legend = axes[0].legend(bbox_to_anchor=(1.1, 1),
                            loc='upper right', fontsize="9")
    # Show the grid
    axes[0].set_axisbelow(True)
    axes[0].grid(visible=True, which='both', axis='both', linewidth=0.5)

    # Second plot
    # Setting up our data
    y_axis = HNE_timely_availability_percentage_array
    # Format the Y-axis values to be percentages
    axes[0].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
    # Plotting the data
    axes[1].bar(x_axis, y_axis)
    # Show the grid
    axes[1].set_axisbelow(True)
    axes[1].grid(visible=True, which='both', axis='both', linewidth=0.5)

    # Third plot
    # Setting up our data
    y_axis = HNZ_timely_availability_percentage_array
    # Format the Y-axis values to be percentages
    axes[0].yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100))
    # Plotting the data
    axes[2].bar(x_axis, y_axis)
    # Show the grid
    axes[2].set_axisbelow(True)
    axes[2].grid(visible=True, which='both', axis='both', linewidth=0.5)

    fig.tight_layout()  # Important for the plot labels to not overlap
    plt.savefig(
        f'tests/latency/test_scripts/isolated_components/{filename}',
        bbox_extra_artists=(legend,),
        bbox_inches='tight')
    plt.close()
