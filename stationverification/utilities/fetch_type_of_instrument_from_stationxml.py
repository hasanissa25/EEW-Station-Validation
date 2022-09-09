import obspy

'''
Returns the type of instrument used on the specific network
station combination

Parameters:

network: str = The code of the network. Ex: QW
station: str = The code of the station. Ex: QCC02

returns:

The type of instrument used. Ex fortimus, or titansma
'''


def fetch_type_of_instrument_from_stationxml(network: str,
                                             station: str,
                                             station_xml: str) \
        -> str:
    inventory = obspy.read_inventory(
        station_xml)
    qw = inventory.select(
        network=network.upper(), station=station.upper())
    # Since the Network and Station are already provided,
    # they will always be at index 0.
    # We give the channel an index of 0 as HNN, HNE, and HNZ will
    # have the same type of instrument.
    qw_channel = qw[0][0][0]
    type_of_instrument = qw_channel.sensor.model.lower()
    return type_of_instrument
