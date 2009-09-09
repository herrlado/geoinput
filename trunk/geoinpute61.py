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
from geoinputbase import geoinputbase
import keycapture
from keypress import simulate_key
from keycapture import KeyCapturer
from key_codes import EKeyBackspace, EScancodeBackspace, EModifierCtrl
from utils import u

class geoinpute61(geoinputbase):
    def __init__(self):
        geoinputbase.__init__(self)

    ### no list. append if not already in list
    def append(self, dest, value):
        intvalue = None
        if type(value) is unicode:
            intvalue = ord(value)
        if type(value) is str:
            intvalue = ord(u(value))
        elif type(value) is int:
            intvalue = value
        else: return

        if intvalue not in dest:
            dest.append(intvalue)
    ###
    def extend(self, key_p, value):
        if type(key_p) is str:
            key = ord(u(key_p))
        elif type(key_p) is int:
            key = key_p
        else:
            return
        if key not in self.keymapkbd:
            self.keymapkbd[key] = tuple([])
        tmp = list(self.keymapkbd[key])
        if type(value) is list:
            for v in value:
                self.append(tmp, v)
        else:
            self.append(tmp, value)
        self.keymapkbd[key] = tuple(tmp)
    ###
    def init(self):
        geoinputbase.init(self)
        self.mainCapturer = None
        self.switcherCapturer = None
        self.inputmode = 0
        self.keymapkbd = {}
        self.switcherFirsKeyLastClickAt = 0
        self.switcherKey = 17
        self.needctrl = ["1","2","3","4","5","6","7","8","9","0","*","#","+","y","z"]
        t = []
        for i in self.needctrl:
            t.append(ord(i))
        self.needctrl = t
        t = None
        for i in range(0,len("a85de7zTikl09opJ1s2*4qR3SCcZwWx#6")):
            self.keymapkbd[ord("a85de7zTikl09opJ1s2*4qR3SCcZwWx#6"[i])] = tuple([i + 4304])
        self.extend('s','შ')
        self.extend('w','ჭ')
        self.extend('1',['ღ','1'])
        self.extend('2',['თ','2'])
        self.extend('3','3')
        self.extend('*','*')
        self.extend('4','4')
        self.extend('5','5')
        self.extend('6','6')
        self.extend('#', ['ჟ','#'])
        self.extend('7','7')
        self.extend('8','8')
        self.extend('9','9')
        self.extend('0','0')
        self.extend('z','ძ')
        self.extend('c',['ჩ','+'])

    ###
    def getDefaultConfig(self):
        cfg = geoinputbase.getDefaultConfig(self)
        cfg['keymapKbdExt'] = {}
        cfg['inputmode'] =  0
        cfg['switcherkey'] = chr(17 + 96) #q
        return cfg
    ###
    def configLoaded(self):
        geoinputbase.configLoaded(self)
        try:
            keymapKbdExt = self.c('keymapKbdExt')
            if keymapKbdExt is not None and type(keymapKbdExt) is dict:
                for key,value in self.config['keymapKbdExt'].items():
                    self.extend(key, value)
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
    ###
    def getSimKey(self, key):
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
    ###
    def mainCallBack(self, key):
        if key not in self.keymapkbd:
            return
        if self.isExceptionInFg():
            self.mainCapturer.stop()
            simulate_key(key, key)
            self.mainCapturer.start()
            return
        self.checkTime()
        if self.lastKey == key :
            self.backspaceCapturer.stop()
            sim_key = self.getSimKey(key)
            if sim_key == key :
                self.mainCapturer.stop()
            simulate_key(EKeyBackspace, EScancodeBackspace)
            if sim_key in self.needctrl:
                simulate_key(sim_key, 0, EModifierCtrl)
            else:
                simulate_key(sim_key, sim_key)
            if sim_key == key:
                self.mainCapturer.start()
            self.backspaceCapturer.start()
        else:
            self.mod = 0
            sim_key = self.getSimKey(key)
            simulate_key(sim_key, sim_key)
    ###
    def initMainCapturer(self):
        geoinputbase.initMainCapturer(self)
        self.mainCapturer = KeyCapturer(self.mainCallBack)
        self.mainCapturer.keys = tuple(self.keymapkbd.keys())
        self.mainCapturer.start()
        self.initSwitcherCapturers()
    ###
    def stopMainCapturer(self):
        self.mainCapturer.stop()
    ###
    def startMainCapturer(self):
        self.mainCapturer.start()
    ###
    def shutdown(self):
        geoinputbase.shutdown(self)
        self.mainCapturer.stop()
        self.switcherCapturer.stop()
        del self.mainCapturer
        del self.switcherCapturer
    ###
    def switcherCallBack(self,key):
        if key == self.switcherKey:
            self.toggle()
    ###
    def initSwitcherCapturers(self):
        self.switcherCapturer = KeyCapturer(self.switcherCallBack)
        self.switcherCapturer.keys = tuple([self.switcherKey])
        self.switcherCapturer.forwarding = 1
        self.switcherCapturer.start()
