class StreamError(Exception):
    """
        Exception raised for errors relating to the stream in sohmetrics.
    """


class MetricHandlerError(Exception):
    """
        Exception raised for errors in the metric handler.
    """


class GeneratePlotError(Exception):
    """
        Exception raised for errors in the generate plot.

    """


class LatencyFileError(Exception):
    """
        Exception raised for errors in the generate plot.

    """


class TimeSeriesError(Exception):
    '''
    Error to be raised if the enddate specified is before or the same as the
    startdate
    '''


class MissingConfigOrStationxml(Exception):
    '''
    Exception to be raised if either the stationXML or stationconfig file
    are not included
    '''
