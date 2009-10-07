from versions import *
g = None
try:
    fw = getFW()
    if fw in KBD_E61_V:
        from geoinpute61 import geoinpute61
        g = geoinpute61()
    if fw in KBD_E71_V:
        from geoinpute71 import geoinpute71
        g = geoinpute71()
    elif fw in KBD_E63_V:
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
    import sys
    import traceback
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, 5)
    errorString = repr(excName) + '-' + repr(excArgs) + '-' + repr(excTb) + '\n'
    print errorString
    from geoinput import geoinput
    g = geoinput()
try:
    g.run()
except:
    g.printStackTrace()
    raise
