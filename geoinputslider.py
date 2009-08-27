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


class geoinputslider(geoinput):
    def __init__(self):
        geoinput.__init__(self)

    def init(self):
        geoinput.init(self)
        #self.log("geoinputslider")
        self.mainCapturerKbd = None
        self.switcherCapturerKbd = None
        self.currentLangKbd = u"default"
        self.inputmode = 0
        self.keymapkbd = {}
        for i in range(0,len("abgdevzTiklmnopJrstufqRySCcZwWxjh")):
            self.keymapkbd[ord("abgdevzTiklmnopJrstufqRySCcZwWxjh"[i])] = i + 4304
        self.number_keys = {'q':'1', 'Q':'1', 'w':'2','W':'2','e':'3', 'r':'4','R':'4', 't':'5','T':'5','y':'6','Y':'6','u':'7','i':'8','o':'9','p':'0','g':'*','h':'#'}
        number_keys2 = {}
        for key,value in self.number_keys.items():
            number_keys2[ord(key)] = ord(value.decode('utf-8'))
        self.number_keys = number_keys2
        self.number_keys2 = None
        self.number_keys_home_ignore = self.number_keys.keys()
        self.switcherKey  = ord(' ')

    # # #
    def getDefaultConfig(self):
        cfg = geoinput.getDefaultConfig(self)
        cfg['keymapKbdExt'] = {}
        #cfg['inputmode'] =  0
        return cfg

    # # #
    def configLoaded(self):
        geoinput.configLoaded(self)
        try:
            if self.c('keymapKbdExt') is not None:
                d = {}
                for key,value in self.config['keymapKbdExt'].items():
                    d[ord(key)] = ord(value.decode('utf-8'))
                    for key, value in d.items():
                        if key not in self.number_keys:
                            self.number_keys[key] = value
        except:
            self.printStackTrace()


    def mainCallBackKbd(self, key):
        if key not in self.number_keys:
            sim_key = self.keymapkbd[key]
            simulate_key(sim_key, sim_key)
            return
        reverse = self.isExceptionInFg() #False
        if key not in self.number_keys_home_ignore:
            reverse = False
        self.checkTime()
        if self.lastKey == key :
            self.backspaceCapturer.stop() # we must stop backspace, because the next call is a "dummy backSpace" to remove a digit in-place
            simulate_key(8,8)
            if reverse:
                sim_key = self.keymapkbd[key]
            else:
                sim_key = self.number_keys[key]
            simulate_key(sim_key, sim_key)
            self.backspaceCapturer.start() # enable backspace forwarding
            self.lastKey = 0
        else:
            if reverse:
                sim_key = self.number_keys[key]
            else:
                sim_key = self.keymapkbd[key]
            simulate_key(sim_key, sim_key)
            self.lastKey = key


    # def initMainCapturer(self):
    #     geoinputbase.initMainCapturer(self)
    #     self.mainCapturer = KeyCapturer(self.mainCallBack)
    #     self.mainCapturer.keys = tuple(self.keymapkbd.keys())
    #     self.mainCapturer.start()
    #     self.initSwitcherCapturers()

    # def getSwitcherSecondKey(self):
    #     return tuple([ord('.')])

    # def getSwitchetFirstKey(self):
    #     return tuple([ord(',')])


    # def switcherSecondKeyInMainCapturer(self):
    #     return False #while , . are not captured in main callback

    # def stopMainCapturer(self):
    #     self.mainCapturer.stop()

    # def startMainCapturer(self):
    #     self.mainCapturer.start()


    # def shutdown(self):
    #     geoinputbase.shutdown(self)
    #     self.mainCapturerKbd.stop()
    #     del self.mainCapturerKbd
    #     del self.switcherCapturer

    # def switcherCallBack(self,key):
    #     now = self.now()
    #     timeDiff =  now - self.switcherFirsKeyLastClickAt
    #     self.switcherFirsKeyLastClickAt = now
    #     self.log(str(timeDiff))
    #     if timeDiff > 0.33:
    #         return
    #     self.switcherFirsKeyLastClickAt =  0
    #     self.toggle()


    #########################
    def initMainCapturer(self):
        geoinput.initMainCapturer(self)
        self.mainCapturerKbd = KeyCapturer(self.mainCallBackKbd)
        self.mainCapturerKbd.keys = tuple(self.keymapkbd.keys())
        self.switcherCapturerKbd = KeyCapturer(self.switcherCapturerKbdCallBack)
        self.switcherCapturerKbd.keys = tuple([self.switcherKey])
        self.switcherCapturerKbd.forwarding = 1
        self.switcherCapturerKbd.start()

        # # #
    def start(self):
        geoinput.start(self)
        self.mainCapturerKbd.stop()


    def shutdown(self):
        geoinput.shutdown(self)
        self.mainCapturerKbd.stop()
        del self.mainCapturerKbd
        self.switcherCapturerKbd.stop()
        del self.switcherCapturerKbd

    def switcherCapturerKbdCallBack(self, key):
        if key == self.switcherKey:
            now = self.now()
            timeDiff =  now - self.switcherFirsKeyLastClickAt
            self.switcherFirsKeyLastClickAt = now
            if timeDiff > 0.33:
                return
            self.switcherFirsKeyLastClickAt =  0
            self.toggleKbd()

    def stopKbd(self):
        self.mainCapturerKbd.stop()
        self.currentLangKbd = u"default"

    def startKbd(self):
        geoinput.stop(self)
        self.mainCapturerKbd.start()
        self.currentLangKbd = u"ka"

    def toggleKbd(self):
        simulate_key(8,8)
        if self.currentLangKbd == u'ka':
            self.currentLangKbd = u'default'
            self.stopKbd()
            if  self.c('noteSwitch') == 0:
                return True
            conf(u("default"))
            e32.ao_sleep(0.2)
            #simulate_key(EKeyHash, EScancodeHash)
        else:
            self.startKbd()
            self.currentLangKbd = u'ka'
            if  self.c('noteSwitch') == 0:
                return True
            conf(u('ქართული'))
            e32.ao_sleep(0.2)
            #simulate_key(EKeyHash, EScancodeHash)
            return True
