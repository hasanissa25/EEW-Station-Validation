from typing import Any, List
import warnings
warnings.filterwarnings("ignore")


class Attachments(dict):
    @property
    def failed_latencies(self) -> List[Any]:
        return self["failed_latencies"]

    @property
    def latency_line_plot(self) -> List[Any]:
        return self["latency_line_plot"]

    @property
    def latency_log_plot(self) -> List[Any]:
        return self["latency_log_plot"]

    @property
    def timely_availability_plot(self) -> List[Any]:
        return self["timely_availability_plot"]

    @property
    def timing_error(self) -> List[Any]:
        return self["timing_error"]

    @property
    def timing_quality(self) -> List[Any]:
        return self["timing_quality"]

    @property
    def validation_results(self) -> List[Any]:
        return self["validation_results"]

    @property
    def adc_count(self) -> List[Any]:
        return self["adc_count"]

    @property
    def max_gap(self) -> List[Any]:
        return self["max_gap"]

    @property
    def num_gaps(self) -> List[Any]:
        return self["num_gaps"]

    @property
    def num_overlaps(self) -> List[Any]:
        return self["num_overlaps"]

    @property
    def pct_above_nhnm(self) -> List[Any]:
        return self["pct_above_nhnm"]

    @property
    def pct_below_nlnm(self) -> List[Any]:
        return self["pct_below_nlnm"]

    @property
    def percent_availability(self) -> List[Any]:
        return self["percent_availability"]

    @property
    def spikes(self) -> List[Any]:
        return self["spikes"]

    @property
    def pdf(self) -> List[Any]:
        return self["pdf"]

    @property
    def clock_offset_line_plot(self) -> List[Any]:
        return self["clock_offset_line_plot"]

    @property
    def clock_offset_log_plot(self) -> List[Any]:
        return self["clock_offset_log_plot"]


class GitLabAttachments(dict):
    '''
    Gitlab handler

    Params:
        list_of_attachments: List of dictionaries containing \
            GitLab attachment information
    '''

    def __init__(
        self,
        list_of_attachments: List[Any]
    ):
        self.list_of_attachments: List[Any] = list_of_attachments

    def get_attachments(self) -> Attachments:
        attachments: dict = {
            "failed_latencies": [],
            "latency_line_plot": [],
            "latency_log_plot": [],
            "timely_availability_plot": [],
            "timing_error": [],
            "timing_quality": [],
            "validation_results": [],
            "adc_count": [],
            "max_gap": [],
            "num_gaps": [],
            "num_overlaps": [],
            "pct_above_nhnm": [],
            "pct_below_nlnm": [],
            "percent_availability": [],
            "spikes": [],
            "pdf": [],
            "clock_offset_line_plot": [],
            "clock_offset_log_plot": []}
        for attachment in self.list_of_attachments:
            if "failed_latencies" in attachment["file_name"]:
                attachments["failed_latencies"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "latency_line_plot" in attachment["file_name"]:
                attachments["latency_line_plot"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "latency_log_plot" in attachment["file_name"]:
                attachments["latency_log_plot"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "timely_availability_plot" in attachment["file_name"]:
                attachments["timely_availability_plot"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "timing_error" in attachment["file_name"]:
                attachments["timing_error"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "timing_quality" in attachment["file_name"]:
                attachments["timing_quality"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "validation_results" in attachment["file_name"]:
                attachments["validation_results"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "adc_count" in attachment["file_name"]:
                attachments["adc_count"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "max_gap" in attachment["file_name"]:
                attachments["max_gap"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "num_gaps" in attachment["file_name"]:
                attachments["num_gaps"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "num_overlaps" in attachment["file_name"]:
                attachments["num_overlaps"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "pct_above_nhnm" in attachment["file_name"]:
                attachments["pct_above_nhnm"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "pct_below_nlnm" in attachment["file_name"]:
                attachments["pct_below_nlnm"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "percent_availability" in attachment["file_name"]:
                attachments["percent_availability"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "spikes" in attachment["file_name"]:
                attachments["spikes"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "pdf" in attachment["file_name"]:
                attachments["pdf"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "clock_offset_line_plot" in attachment["file_name"]:
                attachments["clock_offset_line_plot"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
            elif "clock_offset_log_plot" in attachment["file_name"]:
                attachments["clock_offset_log_plot"].append(
                    {"name": attachment["file_name"],
                     "link": attachment["link"]["markdown"]})
        return Attachments(attachments)
