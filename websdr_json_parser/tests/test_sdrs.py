import pytest

from ..websdr_json_parser import SDRS

SDRS_GOOD_DATA = [
    {"users": "103", "url": "http://websdr.ewi.utwente.nl:8901/", "bands": [{"a": "Mini-Whip", "h": 29.1596, "c": "g10", "l": 0}], "lon": 6.875, "mobile": "m.html", "logourl": "http://websdr.ewi.utwente.nl:8901/utlogo48.gif", "lat": 52.2292, "qth": "JO32KF", "desc": "WebSDR at the University of Twente, Enschede, NL"},
    {"users": "36", "url": "http://hackgreensdr.org:8901/", "bands": [{"a": "204 foot long double size G5RV", "h": 1.996, "c": "m160", "l": 1.804}, {"a": "", "h": 3.792, "c": "m80", "l": 3.6}, {"a": "", "h": 5.4285, "c": "m0", "l": 5.2365}, {"a": "", "h": 7.2, "c": "m40", "l": 7.008}, {"a": "", "h": 14.322, "c": "m20", "l": 14.13}, {"a": "", "h": 18.211, "c": "m17", "l": 18.019}], "lon": -2.54167, "mobile": "m.html", "logourl": "http://hackgreensdr.org:8901/nuclear.gif", "lat": 53.0208, "qth": "IO83RA", "desc": "160m, 60m, 80m, 40m and 17m SDR&#39;s from Nantwich in Cheshire"},
    {"users": "60", "url": "http://69.27.184.62:8901/", "bands": [{"a": "&#34;Omni&#34; (TCI 530 LP, 6 dB gain) with preamp", "h": 1.996, "c": "m160", "l": 1.804}, {"a": "&#34;Omni&#34; (TCI 530 LP, 6 dB gain)", "h": 3.642, "c": "m80", "l": 3.45}, {"a": "&#34;Omni&#34; (TCI 530 LP, 6 dB gain)", "h": 3.812, "c": "m80", "l": 3.62}, {"a": "&#34;Omni&#34; (TCI 530 LP, 6 dB gain)", "h": 4.002, "c": "m80", "l": 3.81}, {"a": "&#34;Omni&#34; (TCI 530 LP, 6 dB gain)", "h": 7.135, "c": "m40", "l": 6.943}, {"a": "Switched: &#34;Omni&#34; (TCI 530) or &#34;SE Sector&#34; (TCI 527B @ 135 deg.)", "h": 7.317, "c": "m40", "l": 7.125}, {"a": "&#34;Omni&#34; (TCI 530 LP, 6 dB gain)", "h": 14.182, "c": "m20", "l": 13.99}, {"a": "&#34;Omni&#34; (TCI 530 LP, 6 dB gain)", "h": 14.357, "c": "m20", "l": 14.165}], "lon": -122.375, "mobile": "m.html", "logourl": "http://69.27.184.62:8901/logo.png", "lat": 37.3958, "qth": "CM87tj", "desc": "KFS WebSDR HF receiver system on the Pacific coast south of San Francisco, CA"}
]


@pytest.fixture
def good_sdrs():
    return SDRS(SDRS_GOOD_DATA)


def test_create():
    assert(SDRS(SDRS_GOOD_DATA))


def test_filter_frequency(good_sdrs):
    assert(len(good_sdrs.filter_frequency(7.1)) == 3)
    assert(len(good_sdrs.filter_frequency(14.1)) == 2)
    assert(len(good_sdrs.filter_frequency(-10)) == 0)
    assert(len(good_sdrs.filter_frequency(100)) == 0)


def test_closest_to(good_sdrs):
    result = good_sdrs.closest_to(53.0200, -2.54167)
    assert(result[0] == good_sdrs.users["36"])

    result = good_sdrs.closest_to(53.0200, -2.54167)
    assert(result[0] == good_sdrs.users["36"])

    result = good_sdrs.closest_to(37.3958, -122.375)
    assert(result[0] == good_sdrs.users["60"])
    assert(not result[1])


def test_search(good_sdrs):
    result = good_sdrs.search(frequency=1.9)  # They're all here
    assert(len(result) == len(good_sdrs.users))

    result = good_sdrs.search(frequency=20)  # They're all here
    assert(len(result) == 1)

    result = good_sdrs.search(frequency=20, closest_to=(52.2292, 6.875))  # They're all here
    assert(result[0] == good_sdrs.users["103"])
    assert(len(result) == 1)
