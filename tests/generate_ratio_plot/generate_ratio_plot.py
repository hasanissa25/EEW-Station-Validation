# flake8: noqa
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates
import numpy as np

register_matplotlib_converters()

# Getting the Data
first_csv = "ispaq_outputs/PDFs/XX/TOTT/XX.TOTT..HNZ.D.2022-04-01_2022-04-10_PDF.csv"
first_dataframe = pd.read_csv(first_csv)
first_dataframe.sort_values(by='power', ascending=True, inplace=True)
first_dataframe.drop_duplicates(subset=['frequency'], inplace=True)
first_dataframe.sort_values(by='frequency', ascending=True, inplace=True)
second_csv = "ispaq_outputs/PDFs/QW/QCC02/QW.QCC02..HNE.D.2022-03-28_PDF.csv"
second_dataframe = pd.read_csv(second_csv)
second_dataframe.sort_values(by='power', ascending=True, inplace=True)
second_dataframe.drop_duplicates(subset=['frequency'], inplace=True)
second_dataframe.sort_values(by='frequency', ascending=True, inplace=True)


# Setting up the plot
fig = plt.figure()
fig.set_size_inches(18.5, 10.5)
ax1 = fig.add_subplot(111)
ax1 = plt.gca()
# Add a title to the axes.
ax1.set_title("Ratio Plot:\n TOTT vs QCC02 (HNZ)")
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('Ratio of power')  # Add a y-label to the axes.
# Setting up our data
x_axis = second_dataframe.frequency
y_axis_cn = first_dataframe["power"].array
y_axis_qw = second_dataframe["power"].array

y_axis = []
for index, i in enumerate(y_axis_cn):
    y_axis.append(y_axis_qw[index]/y_axis_cn[index])
# Show the grid
ax1.set_axisbelow(True)
plt.grid(visible=True, which='both', axis='both', linewidth=0.5)
# Plotting the data
ax1.plot(
    x_axis, y_axis,
    marker='o', label='Ratio', linewidth=1, markeredgewidth=1,
    markersize=1, markevery=10, c="green")

fig.tight_layout()  # Important for the plot labels to not overlap

plt.savefig(
    './tests/generate_ratio_plot/TOTTvsQCC02')
plt.close()
