# flake8:noqa
import pytest
from stationverification.utilities.get_latency_files import get_latency_files


def test_get_latency_files(latency_parameters_nanometrics, latency_parameters_nanometrics_no_files, latency_parameters_guralp):
    nanometrics_files = get_latency_files(typeofinstrument=latency_parameters_nanometrics.type_of_instrument,
                                          network=latency_parameters_nanometrics.network,
                                          path=latency_parameters_nanometrics.path,
                                          station=latency_parameters_nanometrics.station,
                                          startdate=latency_parameters_nanometrics.startdate,
                                          enddate=latency_parameters_nanometrics.enddate)
    assert nanometrics_files == ['tests/latency/test_data/apollo/archive/latency/2022/04/01/QW.QCC02.2022.091.json',
                                 'tests/latency/test_data/apollo/archive/latency/2022/04/02/QW.QCC02.2022.092.json',
                                 'tests/latency/test_data/apollo/archive/latency/2022/04/03/QW.QCC02.2022.093.json']
    guralp_files = get_latency_files(typeofinstrument=latency_parameters_guralp.type_of_instrument,
                                     network=latency_parameters_guralp.network,
                                     path=latency_parameters_guralp.path,
                                     station=latency_parameters_guralp.station,
                                     startdate=latency_parameters_guralp.startdate,
                                     enddate=latency_parameters_guralp.enddate)
    assert guralp_files == ['tests/latency/test_data/guralp/archive/latency/2022/03/01/QW_QCN08_0N_HNE_2022_060.csv',
                            'tests/latency/test_data/guralp/archive/latency/2022/03/01/QW_QCN08_0N_HNN_2022_060.csv',
                            'tests/latency/test_data/guralp/archive/latency/2022/03/01/QW_QCN08_0N_HNZ_2022_060.csv',
                            'tests/latency/test_data/guralp/archive/latency/2022/03/02/QW_QCN08_0N_HNE_2022_061.csv',
                            'tests/latency/test_data/guralp/archive/latency/2022/03/02/QW_QCN08_0N_HNN_2022_061.csv',
                            'tests/latency/test_data/guralp/archive/latency/2022/03/02/QW_QCN08_0N_HNZ_2022_061.csv']
    with pytest.raises(FileNotFoundError):
        get_latency_files(typeofinstrument="non_existent",
                          network="non_existent",
                          path="non_existent",
                          station="non_existent",
                          startdate="non_existent",
                          enddate="non_existent")
    nanometrics_files = get_latency_files(typeofinstrument=latency_parameters_nanometrics_no_files.type_of_instrument,
                                          network=latency_parameters_nanometrics_no_files.network,
                                          path=latency_parameters_nanometrics_no_files.path,
                                          station=latency_parameters_nanometrics_no_files.station,
                                          startdate=latency_parameters_nanometrics_no_files.startdate,
                                          enddate=latency_parameters_nanometrics_no_files.enddate)
    assert nanometrics_files == ['tests/latency/test_data/apollo/archive/latency/2022/04/01/QW.QCC02.2022.091.json',
                                 'tests/latency/test_data/apollo/archive/latency/2022/04/02/QW.QCC02.2022.092.json',
                                 'tests/latency/test_data/apollo/archive/latency/2022/04/03/QW.QCC02.2022.093.json']
