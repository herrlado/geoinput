# import sys
# sys.path.append("C:\\Data\\geoinput")
from geoinputslider import geoinputslider
g = geoinputslider()
try:
    g.run()
except:
    g.printStackTrace()
    raise
