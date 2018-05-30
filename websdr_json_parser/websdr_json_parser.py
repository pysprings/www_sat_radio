#!/usr/bin/env python2
'''
This script contains classes used to interact with the pre-downloaded
"websdr.json" file.  You are responsible for obtaining this file!
'''
import sys
import json

from geopy import distance
from geopy.geocoders import Nominatim


class SDRBand(object):
    def __init__(self, sdr_band_dictionary):
        '''
        Representation of a single band provided by a web radio.

        :param dict sdr_band_dictionary: The dictionary of bands provided by
            the web radio.
        '''
        if set(sdr_band_dictionary.keys()) != {'a', 'h', 'c', 'l'}:
            raise ValueError('Wrong set of keys')

        self.data = sdr_band_dictionary

    def __str__(self):
        return "%s-%s" % (self.data['l'], self.data['h'])

    def contains_frequency(self, frequency):
        '''
        Returns `True` if the provided frequency falls in our range.

        :param frequency float: The frequency, in MHz
        '''
        return self.data["l"] <= frequency <= self.data["h"]


class SDR(object):
    def __init__(self, sdr_dictionary):
        '''
        A Representation of a single web radio and its associated data.

        :param dict sdr_dictionary: The JSON dictionary that describes a
            single web radio station in the JSON.
        '''
        self.user_id = sdr_dictionary['users']
        self.url = sdr_dictionary['url']
        self.bands = [SDRBand(x) for x in sdr_dictionary['bands']]
        self.longitude = sdr_dictionary['lon']
        self.latitude = sdr_dictionary['lat']
        self.qth = sdr_dictionary['qth']
        self.description = sdr_dictionary['desc']

        self._location = None

    def __str__(self):
        return "%s:%s / %s" % (self.longitude, self.latitude, self.description)

    def get_location(self):
        '''
        Return the result of `Nominatim().reverse(lat, lon)`.
        '''
        if self._location is not None:
            return self._location

        self._location = Nominatim().reverse("%s, %s" % (self.latitude, self.longitude))
        return self._location

    def contains_frequency(self, frequency):
        '''
        Returns `True` if the provided frequency falls in our range.

        :param frequency float: The frequency, in MHz
        '''
        return bool(next((x for x in self.bands if x.contains_frequency(frequency)), None))

    def distance_from(self, latitude, longitude):
        return distance.distance((self.latitude, self.longitude), (latitude, longitude))


class SDRS(object):
    def __init__(self, sdr_json):
        '''
        Create a list of SDR objects from the JSON object.

        :param list sdr_json: The list of WebSDR radios.
        '''
        self.users = {x['users']: SDR(x) for x in sdr_json}

    def filter_frequency(self, frequency, users=None):
        '''
        Returns a list of SDR objects that have one band containing the
        frequency.

        :param float frequency: The frequency to filter, in MHz
        '''
        users = users or self.users.values()
        return [
            x for x in users if x.contains_frequency(frequency)
        ]

    def closest_to(self, latitude, longitude, users=None):
        '''
        Returns the single SDR clostest to the provided latitude and longitude.
        '''
        result = (None, 1E99)
        users = users or self.users.values()

        for user in users:
            if not result[0]:
                result = (user, user.distance_from(latitude, longitude))
                continue

            distance = user.distance_from(latitude, longitude)
            if distance < result[1]:
                result = (user, distance)

        return result

    def search(self, frequency=None, closest_to=None):
        '''
        Search through all of the SDRs for one or more matching the filter
        criteria.

        :param float frequency: The frequency, in MHz, to filter on.  If set,
            only SDRs that contain the frequency will be returned.
        :param tuple(lat,long) closest_to: A tuple containing the latitude and
            longitude of the location to search for.
            NOTE: This will always return a list of one item!
        '''
        result = self.users.values()

        # We should always filter frequency first, since this returns a list.
        if frequency is not None:
            result = self.filter_frequency(frequency, result)

        if closest_to is not None:
            result = [self.closest_to(*closest_to, users=result)[0]]

        return result


def main():
    if len(sys.argv) < 2:
        print "USAGE: websdr_json_parser.py <path to websdr.json>"
        return -1

    with open(sys.argv[1]) as fh:
        text = fh.read()

    json_data = json.loads(text)
    sdrs = SDRS(json_data)

    print [str(x) for x in sdrs.filter_frequency(12.0)]

    closest_sdr, distance = sdrs.closest_to(41.6042, -112.292)
    print "SDR closest to 51,7: %s" % closest_sdr
    print "... which is %.2fkm" % distance.km

    print sdrs.search(3333.0, (41.6042, -112.292))


if __name__ == '__main__':
    main()
