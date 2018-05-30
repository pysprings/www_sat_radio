import pytest

from ..websdr_json_parser import SDRBand


@pytest.fixture
def good_sdrs():
    return SDRBand({"a": "Mini-Whip", "h": 29.1596, "c": "g10", "l": 0})


def test_create():
    '''
    Ensure we can create the object.
    '''
    SDRBand({"a": "Mini-Whip", "h": 29.1596, "c": "g10", "l": 0})


def test_not_enough_keys():
    '''Ensure it fails if we don't have enough keys'''
    with pytest.raises(ValueError):
        # missing "c"
        SDRBand({"a": "Mini-Whip", "h": 29.1596, "l": 0})


def test_contains_frequency(good_sdrs):
    assert(good_sdrs.contains_frequency(-10) is False)
    assert(good_sdrs.contains_frequency(30) is False)
    assert(good_sdrs.contains_frequency(29.1) is True)


def test_str(good_sdrs):
    assert(str(good_sdrs) == "0-29.1596")
