import subprocess
import os

from datetime import date, timedelta
from typing import Optional

from stationverification.utilities.change_name_of_ISPAQ_files \
    import change_name_of_ISPAQ_files


def cleanup_directory(
    network: str,
    station: str,
    startdate: date,
    enddate: date,
    outputdir: str,
    instrumentGain: Optional[str] = None
):
    '''
    Function to clean up after the program runs.

    Parameters
    ----------
    network: string
        Network code used for naming the tarball of output files

    station: string
        The station code, used for naming the tarball of output files

    startdate: date
        The start date to use in the name of the tarball of output files

    enddate: date
        The end date to use in the name of the tarball output

    outputdir: string
        Path to the directory to deposit output tarball in. Default = None

    '''
    # Create the final directory that the data will be placed in
    if startdate == enddate - timedelta(days=1):
        validation_output_directory = f'{outputdir}/{network}/{station}/\
{startdate}'
    else:
        validation_output_directory = f'{outputdir}/{network}/{station}/\
{startdate}-{enddate - timedelta(days=1)}'
    # Create the directory if it doesn't already exist
    if not os.path.isdir(validation_output_directory):
        subprocess.getoutput(
            f"mkdir -p '{validation_output_directory}'")

    change_name_of_ISPAQ_files(network=network,
                               station=station,
                               instrumentGain=instrumentGain)
    pdffiles = f'ispaq_outputs/PDFs/{network}/{station}/*.png'
    psdfiles = f'ispaq_outputs/PSDs/{network}/{station}/*.csv'
    subprocess.getoutput(
        f"mv {pdffiles} {validation_output_directory}/")
    subprocess.getoutput(
        f"mv {psdfiles} {validation_output_directory}/")
    subprocess.getoutput(
        f"mv ./stationvalidation_output/* {validation_output_directory}")  # noqa

    subprocess.getoutput(
        "rm -rf stationvalidation_output")

    subprocess.getoutput(
        f"mv ISPAQ_TRANSCRIPT.log {validation_output_directory}")

    subprocess.getoutput(
        "rm -rf ispaq_outputs")


def cleanup_directory_after_latency_call(startdate: date,
                                         enddate: date,
                                         outputdir: str,
                                         network: str,
                                         station: str,
                                         ):
    if startdate == enddate - timedelta(days=1):
        validation_output_directory = f'{outputdir}/{network}/{station}/\
{startdate}'
    else:
        validation_output_directory = f'{outputdir}/{network}/{station}/\
{startdate}-{enddate - timedelta(days=1)}'
    # Create the directory if it doesn't already exist
    if not os.path.isdir(validation_output_directory):
        subprocess.getoutput(
            f"mkdir -p {validation_output_directory}")
    subprocess.getoutput(
        f"mv ./stationvalidation_output/* {validation_output_directory}")  # noqa
    subprocess.getoutput(
        "rm -rf ./stationvalidation_output")
