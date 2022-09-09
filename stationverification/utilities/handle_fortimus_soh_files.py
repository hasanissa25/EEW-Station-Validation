import re
import tempfile
from typing import Any, List


def handle_fortimus_soh_files(fortimus_soh_files: List[str],
                              station: str,
                              location: str) -> List[Any]:
    fortimus_soh_metrics_results_for_validation_period = []
    for file in fortimus_soh_files:
        final_formatted_response = fortimus_soh_file_to_string_format(
            path_of_file=file,
            station=station,
            location=location)

        fortimus_soh_metrics_result_for_current_day \
            = get_fortimus_soh_metrics_results_for_current_day(
                data=final_formatted_response,
                file=file)
        fortimus_soh_metrics_results_for_validation_period.append(
            fortimus_soh_metrics_result_for_current_day)
    return fortimus_soh_metrics_results_for_validation_period


def fortimus_soh_file_to_string_format(
        path_of_file: str,
        station: str,
        location: str) -> str:
    with open(path_of_file, 'rb') as fp:
        content = fp.read()

    response = []
    split_by = f'{station.upper()}{location.upper()}SOH'.encode()

    for line in content.split(split_by):
        response.append((line[46:-8]))

    final_formatted_response = b''.join(response).decode('utf-8')

    return final_formatted_response


def get_fortimus_soh_metrics_results_for_current_day(data: str, file: str):
    start = 'GNSS status'
    end = 'PTP status'
    name_of_file = re.findall("([^\/]+$)", file)[0]  # noqa
    result = re.findall('%s((.|\n)*?)(?=%s)' %
                        (start, end), data)

    temp = tempfile.TemporaryFile(mode='w+t')
    list_of_daily_number_of_satellites_used = []
    list_of_daily_timing_quality = []
    list_of_daily_clock_locked_status = []

    try:
        for index, iteration in enumerate(result):
            temp.writelines(result[index][0])
        temp.seek(0)
        lines = temp.readlines()

        list_of_daily_number_of_satellites_used = get_number_of_satelites_used(
            data=lines)
        list_of_daily_timing_quality = get_timing_quality(
            data=lines)
        list_of_daily_clock_locked_status = get_clock_locked_status(
            data=lines
        )
    finally:
        temp.close()
    return {"number_of_satellites_used":
            list_of_daily_number_of_satellites_used,
            "timing_quality": list_of_daily_timing_quality,
            "clock_locked_status": list_of_daily_clock_locked_status,
            "file": name_of_file}


def get_number_of_satelites_used(data: List[str]) -> List[int]:
    list_of_satellites_used = []
    for line in data:
        if("Satellites used" in line):
            line = line.strip()
            number_of_satellites_used = re.search(  # type: ignore
                '((?<=%s).*)' % ("Satellites used:"), line).group()
            list_of_satellites_used.append(int(number_of_satellites_used))
    return list_of_satellites_used


def get_timing_quality(data: List[str]) -> List[str]:
    list_of_timing_quality = []
    for line in data:
        if("Clock quality" in line):
            line = line.strip()
            timing_quality = re.search(  # type: ignore
                '((?<=%s).*)' % ("Clock quality:"), line).group()
            list_of_timing_quality.append(timing_quality.strip())
    return list_of_timing_quality


def get_clock_locked_status(data: List[str]) -> List[str]:
    list_of_clock_locked_status = []
    for line in data:
        if("Status" in line):
            line = line.strip()
            clock_locked_status = re.search(  # type: ignore
                '((?<=%s).*)' % ("Status:"), line).group()
            list_of_clock_locked_status.append(clock_locked_status.strip())
    return list_of_clock_locked_status
