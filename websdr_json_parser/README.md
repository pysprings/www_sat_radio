# Testing
Run the following command:

    coverage run -m py.test && coverage report -m --skip-covered

# Usage
`websdr_json_parser.py` contains classes to interact with the JSON data
**already retreived** from [websdr.org](http://websdr.org/) (that topic is
not covered here).

Assuming you already have some kind of file named `websdr.json`:

```python
import json
from websdr_json_parser import SDRS

with open('websdr.json') as fh:
    json_data = fh.read()

sdrs = SDRS(json_data)
print sdrs.closest_to(0, 0)
print sdrs.filter_frequency(21.5)
print sdrs.search(frequency=21.5, closest_to=(0, 0))
```
