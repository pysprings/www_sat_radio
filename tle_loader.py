import arrow
from skyfield.api import load

tles = load.tle('https://celestrak.com/NORAD/elements/amateur.txt')
t = tles[25544]
ts = load.timescale()
t.at(ts.utc(arrow.now().datetime)).subpoint()
