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
    sys.path.append("C:\\Data\\geoinput") #for ped
from geoinputbase import geoinputbase
import keycapture
from keypress import simulate_key
from keycapture import KeyCapturer


class geoinputkbd(geoinputbase):
    def __init__(self):
        geoinputbase.__init__(self)

    def init(self):
        geoinputbase.init(self)
        self.mainCapturer = None
        self.switcherCapturer = None
        self.inputmode = 0
        self.keymapkbd = {}
        self.switcherFirsKeyLastClickAt = 0
        self.switcherKey = 17
        for i in range(0,len("a85de73Tikl90opJrs2*fqRySCcZwWx#6")):
            self.keymapkbd[ord("a85de73Tikl90opJrs2*fqRySCcZwWx#6"[i])] = i + 4304
        # for i in range(0,len("abgdevzTiklmnopJrstufqRySCcZwWxjh")):
        #     self.keymapkbd[ord("abgdevzTiklmnopJrstufqRySCcZwWxjh"[i])] = i + 4304
        self.number_keys = {
                'r':'1', 'R':'1', 't':'2','T':'2', 'y':'3',
                'u':'*','f':'4','g':'5','h':'6','j':'#',
                'v':'7', 'b':'8','n':'9','m':'0'
        }

        number_keys2 = {}
        for key,value in self.number_keys.items():
            number_keys2[ord(key)] = ord(value.decode('utf-8'))
        self.number_keys = number_keys2
        self.number_keys2 = None
        self.number_keys_home_ignore =  self.number_keys.keys()
        #self.number_keys_home_ignore = [ord('r'), ord('R'), ord('t'), ord('T'), ord('y'), ord('u'), ord('f'), ord('g'), ord('h'), ord('j'), ord('v'), ord('b'), ord('n'), ord('m')]
        #self.number_keys_home_ignore = [ord('2'), ord('R'), ord('t'), ord('T'), ord('y'), ord('u'), ord('f'), ord('g'), ord('h'), ord('j'), ord('v'), ord('b'), ord('n'), ord('m')]


    # # #
    def getDefaultConfig(self):
        cfg = geoinputbase.getDefaultConfig(self)
        cfg['keymapKbdExt'] = {}
        cfg['inputmode'] =  0
        cfg['switcherkey'] = chr(17 + 96) #q
        return cfg

    # # #
    def configLoaded(self):
        geoinputbase.configLoaded(self)
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
        try:
            char = self.config['switcherkey']
            if char is None:
                char = 'q'
            self.switcherKey = ord(char.decode('utf-8')) - 96
        except:
            self.switcherKey = 17 #q
            self.printStackTrace()

    def mainCallBack(self, key):
        if self.isExceptionInFg():
            self.mainCapturer.stop()
            simulate_key(key,key)
            self.mainCapturer.start()

        if key not in self.number_keys:
            if key not in self.keymapkbd:
                return
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


    def initMainCapturer(self):
        geoinputbase.initMainCapturer(self)
        self.mainCapturer = KeyCapturer(self.mainCallBack)
        self.mainCapturer.keys = tuple(self.keymapkbd.keys())
        self.mainCapturer.start()
        self.initSwitcherCapturers()

    # def getSwitcherSecondKey(self):
    #     return tuple([ord('.')])

    # def getSwitchetFirstKey(self):
    #     return tuple([ord(',')])


    # def switcherSecondKeyInMainCapturer(self):
    #     return False #while , . are not captured in main callback

    def stopMainCapturer(self):
        self.mainCapturer.stop()

    def startMainCapturer(self):
        self.mainCapturer.start()


    def shutdown(self):
        geoinputbase.shutdown(self)
        self.mainCapturer.stop()
        self.switcherCapturer.stop()#####
        del self.mainCapturer
        del self.switcherCapturer #####
    # def shutdown(self):
    #     geoinputbase.shutdown(self)
    #     del self.mainCapturer
    #     del self.switcherCapturer

    def switcherCallBack(self,key):#####
        now = self.now()
        timeDiff =  now - self.switcherFirsKeyLastClickAt
        self.switcherFirsKeyLastClickAt = now
        if timeDiff > 0.33:
            return
        self.toggle()


    def initSwitcherCapturers(self):#####
        self.switcherCapturer = KeyCapturer(self.switcherCallBack)
        self.switcherCapturer.keys = tuple([self.switcherKey])
        self.switcherCapturer.forwarding = 1
        self.switcherCapturer.start()
