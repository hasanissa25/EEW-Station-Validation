'''
This package is used to prepare the environment to use ISPAQ

Functions:
----------

prepare_ispaq_local:
    Prepare an ispaq config file so that it can use local metadata

prepare_ispaq:
    Prepare the environment to be used by ISPAQ

stationxml_from_fdsn:
    Generate station metadata from the CNSN FDSN to be used by ISPAQ when
    using local miniseed files

metadata_from_conf:
    Generate station metadata from a configuration file

link_miniseed_files:
    Creates simlinks to miniseedfiles, using the correct naming scheme for
    ISPAQ

cleanup:
    Remove any temporary files and package the results of the station
    verification

update_station_xml:
    This function will query the apollo server's api and update a stationxml
    file with any new networks or stations it can find in the results

'''
import subprocess
import requests  # type: ignore
import logging
import json

from datetime import date

from obspy.core.inventory.inventory import read_inventory
from obspy.io.xseed import Parser
from obspy.clients.fdsn import Client
from obspy.core import UTCDateTime
from obspy.clients.nrl import NRL
from obspy.core.inventory import Inventory, Network, Station
from obspy.core.inventory import Channel, Equipment
from configparser import ConfigParser

from stationverification import XML_CONVERTER


class InvalidConfigFile(Exception):
    '''
    Exception to be raised if station in missing from file
    '''

    def __init__(self, msg):
        super().__init__(msg)


def prepare_ispaq_local(
    stationconf: ConfigParser,
    tempfolder: str,
    pfile: str,
    miniseed: str,
):
    '''
    Prepare ISPAQ config file so that it can run for a single station with
    local files.

    Parameters
    ----------
    stationconf: ConfigParser
        ConfigParser object containing station information to be used in the
        generation of station metadata and response

    tempfolder: str
        The folder in which to store generated metadata

    pfile: str
        The path to thebase preference file to be modified with local
          variables

    miniseed: str
        The path to the miniseed archive to use with ISPAQ
    '''
    # Generate stationXML files for station
    metadata_from_conf(stationconf, tempfolder)

    station = stationconf.get('metadata', 'station')
    network = stationconf.get('metadata', 'network')
    # Read in the preference file as a template
    with open(pfile, "r") as preffile:
        contents = preffile.readlines()

    # Insert the station's alias right after the line "SNCL:"
    linenum = contents.index('SNCLs:\n') + 1
    contents.insert(linenum, f'  {station}: {network}.{station}.*.H??')

    # Configure ispaq to use local files.
    linenum = contents.index('Data_Access:\n') + 2
    contents[linenum] = f'  dataselect_url:  {miniseed}\n'
    contents[linenum+1] = f'  station_url:  {tempfolder}/station.xml\n'

    contents[linenum+2] = '  event_url:  IRIS\n'
    contents[linenum+3] = f'  resp_dir:  {tempfolder}\n'

    # Write preferenced to a temporary file
    with open(f'{tempfolder}/pref.txt', 'w+') as temppref:
        preference_text = "".join(contents)
        temppref.write(preference_text)

    return f'{tempfolder}/pref.txt'


# def prepare_ispaq(
#     network: str,
#     station: str,
#     temppref: tempfile,  # type: ignore
#     pfile: str,
#     fdsnws: str
# ) -> str:
#     '''
#     The function that handles setting up the environment to work with ISPAQ

#     Parameters
#     ----------
#     network: str
#         The network code for the station

#     station: str
#         The station code for the station to be tested with ISPAQ

#     temppref: tempfile
#         The temporary file to use for ispaq

#     pfile: str
#         The location of the default ISPAQ preference file

#     fdsnws: str
#         The base URL for the FDSN Web service to use for Ispaq

#     Returns
#     -------
#     String
#         The string returned is the path to the temporary preference file

#     '''
#     # Check if the fdsnws url is valid and if not, throw an exception
#     try:
#         Client(base_url=fdsnws)
#     except FDSNException as e:
#         logging.error(e)
#         logging.warning(f'FDSNWS unreachable at {fdsnws},\
# using IRIS instead.')
#         fdsnws = 'IRIS'
#     except ValueError as e:
#         logging.error(e)
#         logging.warning(
#             f'{fdsnws} not a valid URL, using IRIS FDSNWS instead.')
#         fdsnws = 'IRIS'

#     # Read in the preference file as a template
#     with open(pfile, "r") as preffile:
#         contents = preffile.readlines()

#     # Insert the station's alias right after the line "SNCL:"
#     linenum = contents.index('SNCLs:\n') + 1
#     contents.insert(linenum, f'  {station}: {network}.{station}.*.H??')

#     # Set the fdsnws as the dataselect and station metadata target for ISPAQ
#     linenum = contents.index('Data_Access:\n') + 2
#     contents[linenum] = f'  dataselect_url:  {fdsnws}\n'
#     contents[linenum+1] = f'  station_url:  {fdsnws}\n'
#     contents[linenum+2] = '  event_url:  IRIS\n'
#     contents[linenum+3] = '  resp_dir:  \n'

#     # Write to the temporary preference file
#     contents = "".join(contents)
#     temppref.write(contents.encode())
#     temppref.seek(0, os.SEEK_CUR)

#     # Return the name of the tempfile
#     return temppref.name


# Function to pull inventory information from our FDSN using obspy
# This function is deprecated, but still exists for possible future use
def stationxml_from_fdsn(
    network: str,
    station: str,
    start: date,
    stop: date,
    fdsn: str
) -> Inventory:
    '''
    Function to generate stationxml files using information from an fdsn server

    Parameters
    ----------
    network: str
        The network code for the station
    station: str
        The station code of the station to pull metadate from the FDSN for
    start: date
        Datetime date object containing the date to be used as the startdate
        when querying the FDSN server
    stop: date
        Datetime date object containing the date to be used as te endtime when
        querying the FDSN server
    fdsn: str
        The URL for the FDSN server to use

    Returns
    -------
    Inventory:
        Obspy Inventory object containing the metadata retrieved from the FDSN
        server. This is returned for the purpose of unittesting.
    '''
    # Point the obspy Client object at our FDSN server.
    client = Client(fdsn)

    # Populate an obspy inventory object with the metadata for the selected
    # station, from the start date to the end date, to the response level.
    inv = client.get_stations(
        network=network,
        station=station,
        level="response",
        starttime=UTCDateTime(
            start.isoformat()), endtime=UTCDateTime(stop.isoformat()))

    # For some reason if I use a local stationXML file that goes deeper than
    # the station level, ISPAQ tells me that there are no matching channels.
    # Write only station information to a stationxml that ISPAQ can use
    inv.write(
        "tmp/station.xml", format="stationxml", level="station", validate=True)

    # When using local files, ISPAQ requires response information in the form
    # of a RESP file. Generate a stationxml with response information so that
    # it can be converted to a RESP file.
    # Second version of stationXML is used to generate response information

    return inv


def metadata_from_conf(
    conf: ConfigParser,
    tempfolder: str
):
    '''
    Assemble metadata to be used by ispaq using information from a config file.

    Parameters
    ----------

    conf: ConfigParser
        ConfigParser object containing station configuration information

    tempfolder: string
        Path to the folder that will contain all temporary metadata
    '''
    network = conf.get('metadata', 'network')
    station = conf.get('metadata', 'station')
    nrl = NRL()
    # Create an Inventory to be converted to a station xml
    inv = Inventory(
        networks=[],
        source="")

    if conf.get('metadata', 'network') is None:
        raise InvalidConfigFile('No network found in stationconfig file.')
    location = conf.get('metadata', 'location', fallback="")

    # Assemble Network object
    net = Network(
        code=network,
        stations=[],
    )

    # Assemble Station object
    sta = Station(
        code=station,
        latitude=conf.get('metadata', 'latitude', fallback='0'),

        longitude=conf.get('metadata', 'longitude', fallback='0'),
        elevation=conf.get('metadata', 'elevation', fallback='0'),
        start_date=UTCDateTime(conf.get(
            'metadata', 'installdate', fallback=UTCDateTime(0)))
    )

    # Get list of sensors from config file
    channels = list(conf.get('metadata', 'channels').split(','))
    for channel in channels:
        channels[channels.index(channel)] = channel.strip(' ')

    # Loop through each sensor in the list, configuring the channels for each
    # sensor
    respfiles = {}

    for channel in channels:

        # If a REPS file is provided, flag it to be copied
        if 'response_path' in dict(conf.items(channel)):
            respfiles[conf.get(channel, 'response_path')] = f'{tempfolder}RESP.{network}.\
{station}.{location}.{channel}'

        # If a RESP File is not provided for the channel, build the channel's
        # metadata so that it can be converted to a RESP file
        elif 'sensor_keys' in dict(conf.items(channel)) and 'datalogger_keys' \
                in dict(conf.items(channel)):
            # Load datalogger and sensor keys from config file
            sensor_keys = json.loads(conf.get(channel, 'sensor_keys'))
            datalogger_keys = json.loads(conf.get(channel, 'datalogger_keys'))

            # Get the response for a titansma from the NRL
            response = nrl.get_response(
                sensor_keys=sensor_keys,
                datalogger_keys=datalogger_keys)

            # Build the channel object
            cha = Channel(
                code=channel,
                location_code=conf.get('metadata', 'location', fallback=''),
                sample_rate=conf.get(channel, 'sample_rate', fallback='100'),
                latitude=conf.get('metadata', 'latitude', fallback='0'),
                longitude=conf.get('metadata', 'longitude', fallback='0'),
                elevation=conf.get('metadata', 'elevation', fallback='0'),
                depth=conf.get('metadata', 'depth', fallback='0'),
                start_date=UTCDateTime(conf.get(
                    'metadata', 'installdate', fallback=UTCDateTime(0))),
                sensor=Equipment(description=''))

            # Add the response to the channel
            cha.response = response

            # Add the channel to the station
            sta.channels.append(cha)

        else:
            logging.warning(f'No response for {network}.{station}.{channel}, \
PSD-derived metrics and PDF plots will be skipped.')

    # Add the station to the network
    net.stations.append(sta)
    # Add the network to the inventory
    inv.networks.append(net)
    # Write a stationxml file to be used by ISPAQ
    inv.write(
        f"{tempfolder}/station.xml", format="stationxml", level="station",
        validate=True)
    # Write a stationxml file that can be converted to RESP files
    inv.write(
        f"{tempfolder}/{station}resp.xml", format="stationxml", validate=True)

    # Use IRIS's stationxml-seed-converter java porgram to convert stationxml
    # to dataless seed, and then use the obspy parser object to convert to
    # RESP file.
    subprocess.getoutput(f'java -jar {XML_CONVERTER} --input \
{tempfolder}/{station}resp.xml --output {tempfolder}/{station}.dataless')
    pars = Parser(f"{tempfolder}/{station}.dataless")
    pars.write_resp(folder=tempfolder, zipped=False)

    if len(respfiles) > 0:
        for key in respfiles.keys():
            subprocess.getoutput(f'cp {key} {respfiles[key]}')


def update_station_xml(
    stationxml: str,
    apollo: str = None,
):
    '''
    This function downloads and reads station names from an Apollo Server's
    availability API and updates a stationxml file with the bare minimum
    needed to run Ispaq on those stations

    Parameters
    ----------
    stationxml: str
        The path to the stationxml file to update

    apollo: str
        The url of the apollo server to retrieve data from
    '''

    # Read the stationxml file into an inventory object
    inv = read_inventory(stationxml)

    # If an apollo server is specified, download an availability json of all
    # the timeseries data channels
    if apollo is not None:
        url = f'{apollo}/api/v1/channels/availability?type=timeseries'
        # Download the availability data directly into a dictionary object
        availability = json.loads(
            requests.get(url, allow_redirects=True).content)

        # Loop through each entry in the availabiltiy data
        for entry in availability['availability']:
            id = entry['id'].split('.')
            network = id[0]
            station = f'{id[0]}.{id[1]}'

            # If the network doesn't exist in the inventory, create it
            if network not in inv.get_contents()['networks']:
                net = Network(code=network, stations=[])

            # If the network does exist, remove it to be modified
            else:
                net = inv.networks[inv.get_contents()['networks'].index(
                    network)]
                inv = inv.remove(network=network)

            # If the channel isn't in the network object, creat and insert it
            if f'{station} ()' not in net.get_contents()['stations']:
                sta = Station(
                    code=station, latitude=0, longitude=0, elevation=0)
                net.stations.append(sta)

            # Insert the network into the inventory
            inv.networks.append(net)

    # Write the inventory to stationxml file
    inv.write("tmp/stationresp.xml", format="stationxml", validate=True)
