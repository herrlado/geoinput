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
from key_codes import EKeyHash, EScancodeHash, EKeyBackspace, EScancodeBackspace,EModifierCtrl
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
        self.switcherKey  = ord(' ')
        for i in range(0,len("abgd3vzT8klmn90J4s57f1R6SCcZ2Wx*#")):
            self.keymapkbd[ord("abgd3vzT8klmn90J4s57f1R6SCcZ2Wx*#"[i])] = tuple([i + 4304])


        self.extend('1','1')
        self.extend('2','ჭ')
        self.extend('2','2')
        self.extend('3','3')
        self.extend('4','ღ')
        self.extend('4','4')
        self.extend('5','თ')
        self.extend('5','5')
        self.extend('6','6')
        self.extend('7','7')
        self.extend('8','8')
        self.extend('9','9')
        self.extend('0','0')

        self.extend('*','*')
        self.extend('#','ჟ')
        self.extend('#','#')
        self.extend('s','შ')
        self.extend('z','ძ')
        self.extend('c','ჩ')

    def extend(self, a, b):
        tmp = list(self.keymapkbd[ord(a)])
        tmp.append(ord(u(b)))
        #print str(tmp)
        self.keymapkbd[ord(a)] = tuple(tmp)

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
                    #for key, value in d.items():
                        #if key not in self.number_keys:
                            #self.number_keys[key] = value
        except:
            self.printStackTrace()

    def getSimKeyKbd(self, key):
        key_tuple = self.keymapkbd[key]
        sim_key = key_tuple[self.mod]
        key_tuple_len = len(key_tuple)
        if self.mod + 1 == key_tuple_len or key_tuple_len == 1:
            self.lastKey = 0
            self.mod = 0
        else:
            self.lastKey = key
            self.mod = (self.mod + 1)  % key_tuple_len
        return sim_key


    def mainCallBackKbd(self, key):
        if key not in self.keymapkbd:
            return
        if self.isExceptionInFg():
            self.mainCapturerKbd.stop()
            simulate_key(key, key)
            self.mainCapturerKbd.start()
            return
        self.checkTime()
        if self.lastKey == key :
            self.backspaceCapturer.stop() # we must stop backspace, because the next call is a "dummy backSpace" to remove a digit in-place
            sim_key = self.getSimKeyKbd(key) #self.keymap[key][mod]
            if sim_key == key : # got number, we need special handling
                self.mainCapturerKbd.stop()  # commonCapturer must not capture next fired keyKode.
                simulate_key(EKeyBackspace, EScancodeBackspace)
                simulate_key(key, 0, EModifierCtrl) # send number code
                self.mainCapturerKbd.start()
            else : # usuall handling
                simulate_key(EKeyBackspace, EScancodeBackspace)
                simulate_key(sim_key, sim_key)
            self.backspaceCapturer.start() # enable backspace forwarding
        else:
            self.mod = 0
            sim_key = self.getSimKeyKbd(key)
            simulate_key(sim_key, sim_key)


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
        self.lastKey = 0
        self.mod = 0


    def startKbd(self):
        geoinput.stop(self)
        self.mainCapturerKbd.start()
        self.currentLangKbd = u"ka"
        self.lastKey = 0
        self.mod = 0

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
