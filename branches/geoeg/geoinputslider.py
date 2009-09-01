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
UID = "20027ad2"
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
        self.switcherFirsKeyLastClickKbdAt = 0
        self.inputmode = 0
        self.keymapkbd = {}
        self.switcherKey  = ord(' ')
        self.numbers = range(48, 58)
        self.numbers.append(ord('*'))
        self.numbers.append(ord('#'))
        for i in range(0,len("abgdevzTiklmnopJrstufqRySCcZwWxjh")):
            self.keymapkbd[ord("abgdevzTiklmnopJrstufqRySCcZwWxjh"[i])] = tuple([i + 4304])


        self.extend('q','1')
        self.extend('w','ჭ')
        self.extend('w','2')
        self.extend('e','3')
        self.extend('r','ღ')
        self.extend('r','4')
        self.extend('t','თ')
        self.extend('t','5')
        self.extend('y','6')
        self.extend('u','7')
        self.extend('i','8')
        self.extend('o','9')
        self.extend('p','0')

        self.extend('j','ჟ')
        self.extend('j','*')

        self.extend('h','#')
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
                simulate_key(key, key)
                self.mainCapturerKbd.start()
            elif sim_key in self.numbers:
                simulate_key(EKeyBackspace, EScancodeBackspace)
                simulate_key(sim_key, 0, EModifierCtrl) # send number code
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
            timeDiff =  now - self.switcherFirsKeyLastClickKbdAt
            self.switcherFirsKeyLastClickKbdAt = now
            if timeDiff > 0.33:
                return
            self.switcherFirsKeyLastClickKbdAt =  0
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
