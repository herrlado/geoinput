# -*- coding: utf-8 -*-
# Copyright (C) 2009 Lado Kumsiashvili <herrlado@arcor.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
import appuifw
UID = "20027ad1"
if appuifw.app.uid() != UID:
    import sys
    sys.path.append("C:\\Data\\geoinput")

from geoinputbase import geoinputbase
from geoinputbase import UID
from utils import u
from key_codes import EKey0, EKey1, EKey2, EKey3, EKey4, EKey5, EKey6, EKey7, EKey8, EKey9, EKeyHash, EModifierCtrl, EKeyBackspace, EScancodeBackspace
from keycapture import KeyCapturer
from keypress import simulate_key


class geoinput(geoinputbase):
    def __init__(self):
        geoinputbase.__init__(self)

    def init(self):
        geoinputbase.init(self)
        self.log("geoinput")
        self.mainCapturer     = None  #main caputurer
        self.switcherCapturer = None
        self.switcherFirstClickCapturer = None

        self.switcherFirsKeyLastClickAt = 0
        self.mod = 0
        self.keymap = {
            EKey0 : [" ", "0", "\r"],

            EKey1 : [".", ",", "?", "!", "@", "'", "-", "1"],
            EKey2 : ["ა", "ბ", "ც", "ჩ", "2"],
            EKey3 : ["დ", "ე", "ფ", "3"],
            EKey4 : ["გ", "ჰ", "ი", "4"],
            EKey5 : ["ჯ", "კ", "ლ", "ჟ", "5"],
            EKey6 : ["მ", "ნ", "ო", "6"],
            EKey7 : ["პ","ქ","რ","ს","ღ","შ","7"],
            EKey8 : ["ტ","უ","ვ","თ","8"],
            EKey9 : ["წ","ხ","ყ","ზ","ჭ","ძ","9"]
            }
        for  value in self.keymap.values():
            for i in range(len(value)):
                value[i]=ord(u(value[i]))

    def initMainCapturer(self):
        self.mainCapturer = KeyCapturer(self.mainCallBack)
        self.mainCapturer.keys = tuple(self.keymap.keys())
        self.mainCapturer.start()
        self.initSwitcherCapturers()


    def mainCallBack(self, key):
        if self.isExceptionInFg():
            self.mainCapturer.stop()
            simulate_key(key, key)
            self.mainCapturer.start()
            return
        if key == EKey0:
            if self.switcherCallBack(key):
                return
        self.checkTime()
        if self.lastKey == key :
            self.backspaceCapturer.stop() # we must stop backspace, because the next call is a "dummy backSpace" to remove a digit in-place
            simulate_key(EKeyBackspace, EScancodeBackspace)
            sim_key = self.getSimKey(key) #self.keymap[key][mod]
            if sim_key == key : # got number, we need special handling
                self.mainCapturer.stop()  # commonCapturer must not capture next fired keyKode.
                simulate_key(key, 0, EModifierCtrl) # send number code
                self.mainCapturer.start()
            else : # usuall handling
                simulate_key(sim_key, sim_key)
            self.backspaceCapturer.start() # enable backspace forwarding
        else:
            sim_key = self.keymap[key][0]
            simulate_key(sim_key, sim_key)
            self.lastKey = key
            self.mod = 1

    ## #
    def getSimKey(self, key):
        key_tuple = self.keymap[key]
        sim_key = key_tuple[self.mod]
        self.mod = (self.mod + 1) % len(key_tuple)
        return sim_key


    def getSwitchetFirstKey(self):
        return [EKeyHash]

    def getSwitcherSecondKey(self):
        return [EKey0]


    def stopMainCapturer(self):
        self.mainCapturer.stop()

    def startMainCapturer(self):
        self.mainCapturer.start()

    def shutdown(self):
        geoinputbase.shutdown(self)
        del self.mainCapturer


    def start(self):
        geoinputbase.start(self)
        if self.switcherSecondKeyInMainCapturer():
            self.switcherCapturer.stop()
        else:
            self.switcherCapturer.start()
            self.currentLang = u'ka'

    def switcherSecondKeyInMainCapturer(self) :
        return True

        # # #
    def initSwitcherCapturers(self):
        self.switcherCapturer = KeyCapturer(self.switcherCallBack)
        self.switcherCapturer.keys = tuple(self.getSwitcherSecondKey())
        self.switcherCapturer.forwarding = 1
        if not self.switcherSecondKeyInMainCapturer() :
            self.switcherCapturer.start()
        self.switcherFirstClickCapturer = KeyCapturer(self.switcherFirstClickCallBack)
        self.switcherFirstClickCapturer.keys = tuple(self.getSwitchetFirstKey())
        self.switcherFirstClickCapturer.forwarding = 1
        self.switcherFirstClickCapturer.start()


    def needToggle(self):
        now = self.now()
        timeDiff =  now - self.switcherFirsKeyLastClickAt
        if timeDiff < 0.33:
            self.switcherFirsKeyLastClickAt =  0
            self.switcherCapturer.forwarding = 0
            return True
        return False


        # # #
    def switcherCallBack(self, key):
        if key in self.getSwitcherSecondKey():
            if self.isExceptionInFg():
                return False
            if not self.needToggle():
                return False
            return self.toggle()

    # # #
    def switcherFirstClickCallBack(self, key):
        if key in self.getSwitchetFirstKey():
            self.switcherFirsKeyLastClickAt = self.now()

    def stop(self):
        geoinputbase.stop(self)
        self.switcherCapturer.forwarding = 1
        if self.switcherSecondKeyInMainCapturer():
            self.switcherCapturer.start()
