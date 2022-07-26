import os

import requests
import logging


def update_station_xml():
    logging.info("Fetching Station XML")
    if not os.path.isfile("stationverification/data/QW.xml"):
        open('stationverification/data/QW.xml', 'wb')

    station_url = "https://earthquakescanada.nrcan.gc.ca/fdsnws/station/1/query?network=QW&level=response&nodata=404"  # noqa
    request = requests.get(station_url, allow_redirects=True)
    request.raise_for_status()
    open('stationverification/data/QW.xml', 'wb').write(request.content)
