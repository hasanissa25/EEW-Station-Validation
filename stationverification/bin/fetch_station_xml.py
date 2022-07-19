import requests
import argparse
from datetime import timedelta
from dateutil import parser as dateparser  # type: ignore


def main():
    class UserInput(dict):
        @property
        def startdate(self) -> bool:
            return self["startdate"]

        @property
        def network(self) -> str:
            return self["network"]

    def fetch_arguments() -> UserInput:
        argsparser = argparse.ArgumentParser()
        argsparser.add_argument(
            "-s",
            "--start_date",
            help="The starting date on each station",
            type=str,
            default=None
        )
        argsparser.add_argument(
            "-n",
            "--network",
            help="Network to fetch from the FDSN",
            type=str,
            required=True
        )
        args = argsparser.parse_args()
        network = args.network
        startdate = args.start_date
        return UserInput(network=network, startdate=startdate)

    user_input = fetch_arguments()
    start_date = user_input.startdate
    network = user_input.network

    if start_date is None:
        station_url = f"http://fdsn.seismo.nrcan.gc.ca/fdsnws/station/1/query?network={network}&level=response&nodata=404"  # noqa
    else:
        start_date_as_date = (dateparser.parse(
            start_date, yearfirst=True)).date() - timedelta(days=1)
        station_url = f"http://fdsn.seismo.nrcan.gc.ca/fdsnws/station/1/query?startafter={start_date_as_date}&network={network}&nodata=404"  # noqa

    request = requests.get(station_url, allow_redirects=True)
    request.raise_for_status()
    open('stationverification/data/QW.xml', 'wb').write(request.content)
