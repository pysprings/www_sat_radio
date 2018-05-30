import pytest

from ..websdr_json_parser import SDR


SDR_GOOD_DATA = {"users": "103", "url": "http://websdr.ewi.utwente.nl:8901/", "bands": [{"a": "Mini-Whip", "h": 29.1596, "c": "g10", "l": 0}], "lon": 6.875, "mobile": "m.html", "logourl": "http://websdr.ewi.utwente.nl:8901/utlogo48.gif", "lat": 52.2292, "qth": "JO32KF", "desc": "WebSDR at the University of Twente, Enschede, NL"}
SDR_BAD_DATA = {"users": "103", "url": "http://websdr.ewi.utwente.nl:8901/", "bands": [{"a": "Mini-Whip", "h": 29.1596, "l": 0}], "lon": 6.875, "mobile": "m.html", "logourl": "http://websdr.ewi.utwente.nl:8901/utlogo48.gif", "lat": 52.2292, "qth": "JO32KF", "desc": "WebSDR at the University of Twente, Enschede, NL"}


@pytest.fixture
def good_sdr():
    return SDR(SDR_GOOD_DATA)


def test_create():
    '''
    Ensure we can create the object.
    '''
    sdr = SDR(SDR_GOOD_DATA)
    assert(sdr.user_id == "103")
    assert(sdr.url == "http://websdr.ewi.utwente.nl:8901/")
    assert(sdr.latitude == 52.2292)
    assert(sdr.longitude == 6.875)
    assert(sdr.qth == "JO32KF")
    assert(sdr.description == "WebSDR at the University of Twente, Enschede, NL")

    with pytest.raises(ValueError):
        SDR(SDR_BAD_DATA)


def test_get_location(good_sdr):
    assert(good_sdr._location is None)
    assert('Nederland' in good_sdr.get_location().address)

    assert(good_sdr._location is not None)
    assert('Nederland' in good_sdr.get_location().address)  # This should use cached


def test_contains_frequency(good_sdr):
    assert(good_sdr.contains_frequency(10.0) is True)
    assert(good_sdr.contains_frequency(-1) is False)
    assert(good_sdr.contains_frequency(30) is False)


def test_distance_from(good_sdr):
    assert(good_sdr.distance_from(52.2292, 6.875) == 0)
    assert(good_sdr.distance_from(0, 0) > 0)


def test_str(good_sdr):
    assert(str(good_sdr) == '6.875:52.2292 / WebSDR at the University of Twente, Enschede, NL')
