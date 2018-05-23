# WWW Satellite Receiver

This project is intended to build a system for receiving satellites via a
distributed system of software defined radio (SDR) receivers. These receivers
are already built and available, courtesy of [WebSDR](http://websdr.org/).

## Architecture

While this should be updated by PySprings users, the general idea is this:

* Identify and collect a set of amateur radio satellites, such as
[amsats](https://www.amsat.org/) or other
[OSCARs](https://www.n2yo.com/satellites/?c=18).

* Identify and catalogue the ground stations on the WebSDR site, recording
  their physical locations and frequency ranges
 
* Build an API to communicate with the WebSDRs:
    
    * Reverse engineer the protocol used to talk to the server
    * Determine the tuning commands
    * Determine how to acquire (audio) samples from a site
    * Wrap all of these in a web-based API, potentially using [requests](http://docs.python-requests.org/en/master/)

* Pick an amateur satellite which carries a voice transponder (or any other
  modulation type which is decodable by the radios on WebSDR)

* Get a representation of its [orbital parameters](https://en.wikipedia.org/wiki/Two-line_element_set)

* Determine its present location in space and the projection of such on the ground, using something like [PyEphem](http://rhodesmill.org/pyephem/) or [PyOrbital](https://github.com/pytroll/pyorbital).

* Use [some kind of distance
  algorithm](https://github.com/googlemaps/google-maps-services-python) to
  determine which of the ground stations discovered in step 2 is closest

* Access the WebSDR API to tune the SDR to the appropriate downlink frequency

* Use the API to pull samples for playback

* Listen to SPACE!

### Directory Structure

websdr_api/ - Code/package for controlling a WebSDR instance
space_radio/ - Application code with logic for controlling the system


### Changelog

This should track the progress made to this system and when it happened, for
posterity:

* 22 May 2018: This README created

### Libraries

* [Skyfield](http://rhodesmill.org/skyfield/) 
