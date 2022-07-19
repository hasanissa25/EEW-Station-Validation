# flake8:noqa

import json
import math
from stationverification.utilities import exceptions


def calculate_total_availability_for_nanometrics(files: list) -> float:
    '''
    Calculates the total availability percentage from a list Nanometric
    latency files

    Parameters
    ---------
    files: list
        List of file paths to nanometric latency jsons

    Outputs
    -------
    Total Availability Percentage to two decimal places
    '''
    # The sum of the average percent availability of all files, to be divided by the number of files to get the final average percent availiablity
    total_sum_of_percent_availability_for_all_files = 0.
    # The number of latency files. Used to get the average percent availability
    number_of_latency_files = len(files)
    # final_average_percent_availability_for_all_files = total_sum_of_percent_availability_for_all_files / number_of_latency_files
    final_average_percent_availability_for_all_files = 0.

    for file in files:
        # Getting the average percent availability for each file
        json_latency_file = open(file)
        try:
            latency_dict = json.load(json_latency_file)
        except json.decoder.JSONDecodeError:
            raise exceptions.LatencyFileError(
                f'Problem detected in latency file: {file}')
        array_of_channels_in_current_latency_file = latency_dict["availability"]
        number_of_channels = len(latency_dict["availability"])
        sum_of_percent_availability_for_all_channels = 0.
        # Iterating over each channel, HNN, HNZ, and HNE, and getting the average percent availability
        for current_channel in array_of_channels_in_current_latency_file:
            sum_of_current_channels_percent_availability = 0
            number_of_latency_objects_in_current_channel = \
                len(current_channel["intervals"])
            average_percent_availability_for_current_channel = 0.
            for latency_object in current_channel["intervals"]:
                sum_of_current_channels_percent_availability += \
                    latency_object["percentAvailability"]
            average_percent_availability_for_current_channel = sum_of_current_channels_percent_availability / \
                number_of_latency_objects_in_current_channel
            sum_of_percent_availability_for_all_channels += average_percent_availability_for_current_channel
        if number_of_channels > 0:
            average_percent_availability_for_file = sum_of_percent_availability_for_all_channels / \
                number_of_channels
        else:
            average_percent_availability_for_file = 0
        total_sum_of_percent_availability_for_all_files += average_percent_availability_for_file
    final_average_percent_availability_for_all_files = math.floor(
        total_sum_of_percent_availability_for_all_files
        / number_of_latency_files * 10 ** 2)\
        / 10 ** 2

    return final_average_percent_availability_for_all_files
