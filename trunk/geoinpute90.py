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
from geoinput import geoinput
import keycapture
from keypress import simulate_key
from keycapture import KeyCapturer
from utils import *
from key_codes import EKeyHash, EScancodeHash
import e32

class geoinpute90(geoinput):
    def __init__(self):
        geoinput.__init__(self)

    def init(self):
        geoinput.init(self)
        self.log("geoinpute90")
        self.mainCapturerKbd = None
        self.switcherCapturerKbd = None
        self.currentLangKbd = u"default"
        self.switcherKey = 16
        self.keymapkbd = {}
        for i in range(0,len("abgdevzTiklmnopJrstufqRySCcZwWxjh")):
            self.keymapkbd[ord("abgdevzTiklmnopJrstufqRySCcZwWxjh"[i])] = i + 4304
    # #
    def getDefaultConfig(self):
        cfg = geoinput.getDefaultConfig(self)
        cfg['switcherkey'] = chr(16 + 96) #q
        return cfg

    # #
    def configLoaded(self):
        geoinput.configLoaded(self)
        try:
            char = self.config['switcherkey']
            if char is None:
                char = 'q'
            self.switcherKey = ord(char.decode('utf-8')) - 96
        except:
            self.switcherKey = 16 #p
            self.printStackTrace()

    def mainCallBackKbd(self, key):
        if self.isExceptionInFg():
            self.mainCapturerKbd.stop()
            simulate_key(key, key)
            self.mainCapturerKbd.start()
            return

        sim_key = self.keymapkbd[key]
        simulate_key(sim_key, sim_key)

    def initMainCapturer(self):
        geoinput.initMainCapturer(self)
        self.mainCapturerKbd = KeyCapturer(self.mainCallBackKbd)
        self.mainCapturerKbd.keys = tuple(self.keymapkbd.keys())
        self.switcherCapturerKbd = KeyCapturer(self.switcherCapturerKbdCallBack)
        self.switcherCapturerKbd.keys = tuple([self.switcherKey])
        self.switcherCapturerKbd.forwarding = 0
        self.switcherCapturerKbd.start()

        # # #
    def start(self):
        geoinput.start(self)
        self.mainCapturerKbd.stop()


    def shutdown(self):
        geoinput.shutdown(self)
        self.mainCapturerKbd.stop()
        del self.mainCapturerKbd

    def switcherCapturerKbdCallBack(self, key):
        if key == self.switcherKey:
            self.toggleKbd()

    def stopKbd(self):
        self.mainCapturerKbd.stop()
        self.currentLangKbd = u"default"

    def startKbd(self):
        geoinput.stop(self)
        self.mainCapturerKbd.start()
        self.currentLangKbd = u"ka"

    def toggleKbd(self):
        if self.currentLangKbd == u'ka':
            self.currentLangKbd = u'default'
            self.stopKbd()
            if  self.c('noteSwitch') == 0:
                return True
            conf(u("default"))
            e32.ao_sleep(0.2)
            simulate_key(EKeyHash, EScancodeHash)
        else:
            self.startKbd()
            self.currentLangKbd = u'ka'
            if  self.c('noteSwitch') == 0:
                return True
            conf(u('ქართული'))
            e32.ao_sleep(0.2)
            simulate_key(EKeyHash, EScancodeHash)
            return True
