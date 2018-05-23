'''
This is an example of how to programmatically retrieve coordinates using geopy
for cities in the WebSDR thing.
'''
from geopy.geocoders import Nominatim

def main():
    example_city = 'Rome, Italy' #Location of "ROMA2"
    
    geolocator = Nominatim()
    location = geolocator.geocode(example_city)

    print location.latitude, location.longitude

if __name__ == '__main__':
    main()
