from keypress import *
import appuifw, e32, e32dbm, os.path, os
import keycapture
import globalui



def commonLogger(key):
    print(str(key))


commonCapturer = keycapture.KeyCapturer(commonLogger)
commonCapturer.keys = keycapture.all_keys
commonCapturer.forwarding = 0
commonCapturer.start()
