# flake8: noqa
from typing import Optional
from jinja2 import Template
from stationverification.utilities.GitLabAttachments import Attachments


def generate_markdown_template_for_full_validation(attachments: Attachments,
                                                   json_report: dict,
                                                   typeofinstrument: str) -> str:
    if typeofinstrument == "titansma":
        full_validation_template = Template('''
<details><summary>JSON Report</summary>
{% for element in validation_results -%}
    {{ element["link"] }}
{% endfor %}
</details>

<details><summary>PDF</summary>
{% for element in pdf -%}
 {{ element["link"] }}
{% endfor %}
</details>

<details><summary>Latency Log Plot</summary>
{% for element in latency_log_plot -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Latency Line Plots</summary>
{% for element in latency_line_plot -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Failed Latencies</summary>
{% for element in failed_latencies -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Timely Availability</summary>
{% for element in timely_availability_plot -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Timing Error</summary>
{% for element in timing_error -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Timing Quality</summary>
{% for element in timing_quality -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>ADC Count</summary>
{% for element in adc_count -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Max Gap {{ max_gap_status }}</summary>
{% for element in max_gap -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Number of Gaps {{ num_gaps_status }}</summary>
{% for element in num_gaps -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Number of Overlaps {{ num_overlaps_status }}</summary>
{% for element in num_overlaps -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Spikes {{ spikes_status }}</summary>
{% for element in spikes -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Percent above New High Noise Model</summary>
{% for element in pct_above_nhnm -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Percent below New Low Noise Model {{pct_below_nlnm_status}}</summary>
{% for element in pct_below_nlnm -%}
 {{ element["link"] }}
{% endfor %}
</details>
''')
    elif typeofinstrument == "fortimus":
        full_validation_template = Template('''
<details><summary>JSON Report</summary>
{% for element in validation_results -%}
    {{ element["link"] }}
{% endfor %}
</details>

<details><summary>PDF</summary>
{% for element in pdf -%}
 {{ element["link"] }}
{% endfor %}
</details>

<details><summary>Latency Log Plot</summary>
{% for element in latency_log_plot -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Latency Line Plots</summary>
{% for element in latency_line_plot -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Failed Latencies</summary>
{% for element in failed_latencies -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Timely Availability</summary>
{% for element in timely_availability_plot -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>ADC Count</summary>
{% for element in adc_count -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Max Gap {{ max_gap_status }}</summary>
{% for element in max_gap -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Number of Gaps {{ num_gaps_status }}</summary>
{% for element in num_gaps -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Number of Overlaps {{ num_overlaps_status }}</summary>
{% for element in num_overlaps -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Spikes {{ spikes_status }}</summary>
{% for element in spikes -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Percent above New High Noise Model</summary>
{% for element in pct_above_nhnm -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Percent below New Low Noise Model {{pct_below_nlnm_status}}</summary>
{% for element in pct_below_nlnm -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Clock offset line plots</summary>
{% for element in clock_offset_line_plot -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Clock offset log plot</summary>
{% for element in clock_offset_log_plot -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>DAC Voltage plot</summary>
{% for element in dac_voltage_plot -%}
 {{ element["link"] }}
{% endfor %}
</details>
''')
    empty_fields_dictionary = get_empty_fields(json_report)
    template_render = full_validation_template.render(
        failed_latencies=attachments.failed_latencies,
        latency_line_plot=attachments.latency_line_plot,
        latency_log_plot=attachments.latency_log_plot,
        timely_availability_plot=attachments.timely_availability_plot,
        timing_error=attachments.timing_error,
        timing_quality=attachments.timing_quality,
        validation_results=attachments.validation_results,
        adc_count=attachments.adc_count,
        max_gap=attachments.max_gap,
        max_gap_status=empty_fields_dictionary["max_gap"],
        num_gaps=attachments.num_gaps,
        num_gaps_status=empty_fields_dictionary["num_gaps"],
        num_overlaps=attachments.num_overlaps,
        num_overlaps_status=empty_fields_dictionary["num_overlaps"],
        pct_above_nhnm=attachments.pct_above_nhnm,
        pct_below_nlnm=attachments.pct_below_nlnm,
        pct_below_nlnm_status=empty_fields_dictionary["pct_below_nlnm"],
        spikes=attachments.spikes,
        spikes_status=empty_fields_dictionary["spikes"],
        pdf=attachments.pdf,

        clock_offset_line_plot=attachments.clock_offset_line_plot,
        clock_offset_log_plot=attachments.clock_offset_log_plot,

        dac_voltage_plot=attachments.dac_voltage_plot,

    )
    return template_render


def generate_markdown_template_for_latency_validation(attachments: Attachments)\
        -> str:
    latency_validation_template = Template('''
<details><summary>Latency Log Plot</summary>
{% for element in latency_log_plot -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Latency Line Plots</summary>
{% for element in latency_line_plot -%}
 {{ element["link"] }}
{% endfor %}
</details>
<details><summary>Failed Latencies</summary>
{% for element in failed_latencies -%}
 {{ element["link"] }}
{% endfor %}
</details>
''')
    template_render = latency_validation_template.render(
        failed_latencies=attachments.failed_latencies,
        latency_line_plot=attachments.latency_line_plot,
        latency_log_plot=attachments.latency_log_plot,
    )
    return template_render


def get_empty_fields(json_report: dict):
    empty_fields_dictionary = {}
    empty_fields_dictionary["max_gap"] = check_if_empty(
        json_report=json_report, name_of_field="max_gap")
    empty_fields_dictionary["num_gaps"] = check_if_empty(
        json_report=json_report, name_of_field="num_gaps")
    empty_fields_dictionary["num_overlaps"] = check_if_empty(
        json_report=json_report, name_of_field="num_overlaps")
    empty_fields_dictionary["pct_below_nlnm"] = check_if_empty(
        json_report=json_report, name_of_field="pct_below_nlnm")
    empty_fields_dictionary["spikes"] = check_if_empty(
        json_report=json_report, name_of_field="spikes")
    return empty_fields_dictionary


def check_if_empty(name_of_field: str,
                   json_report: dict):
    HNE_is_all_zero = check_if_all_values_are_zero(
        list_to_check=json_report["channels"]["HNE"]["metrics"][name_of_field]["values"])
    HNN_is_all_zero = check_if_all_values_are_zero(
        list_to_check=json_report["channels"]["HNN"]["metrics"][name_of_field]["values"])
    HNZ_is_all_zero = check_if_all_values_are_zero(
        list_to_check=json_report["channels"]["HNZ"]["metrics"][name_of_field]["values"])

    if HNE_is_all_zero and HNN_is_all_zero and HNZ_is_all_zero:
        return "(Empty)"
    else:
        return ""


def check_if_all_values_are_zero(list_to_check: list):
    return all(value == 0 for value in list_to_check)
