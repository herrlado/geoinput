# import sys
# sys.path.append("C:\\Data\\geoinput")
from versions import *

g = None
try:
    fw = getFW()
    print fw
    if fw in KBD_E61_V:
        from geoinpute61 import geoinpute61
        g = geoinpute61()
    elif fw in KBD_V:
        from geoinputkbd import geoinputkbd
        g = geoinputkbd()
    elif fw in DBL_KBD_V:
        from geoinpute90 import geoinpute90
        g = geoinpute90()
    elif fw in N97_V:
        from geoinputslider import geoinputslider
        g = geoinputslider()
    else:
        from geoinput import geoinput
        g = geoinput()
except:

    from geoinput import geoinput
    g = geoinput()
try:
    g.run()
except:
    g.printStackTrace()
    raise
