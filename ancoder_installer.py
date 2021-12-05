import requests
import os
import sys

class MissingArgsError(Exception):
    pass
class NotFound(Exception):
    pass

try:
    kw = sys.argv[1]
except IndexError:
    raise MissingArgsError("One or more args has been missing")

r = requests.get("https://static.cdn.ancoder.ml/packager/"+kw)

if r.status_code == 404:
    raise NotFound("Package not found!")
else:
    open("temp.py", 'w').write(r.text)
    import temp
    temp.setup(sys.argv, MissingArgsError)
    os.remove("temp.py")
