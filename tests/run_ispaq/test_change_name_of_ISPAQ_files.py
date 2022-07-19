from stationverification.utilities.change_name_of_ISPAQ_files \
    import change_name_of_ISPAQ_files


def test_change_name_of_ISPAQ_files():
    change_name_of_ISPAQ_files(network="QW", station="QCC02")
