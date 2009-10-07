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
from utils import u, conf
from key_codes import EKeyBackspace, EScancodeBackspace, EModifierCtrl
import e32

class geoinpute71(geoinputbase):
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
        self.keymapkbdhs  = {}
        self.switcherFirsKeyLastClickAt = 0
        self.switcherKey =  ord(' ')
        self.needctrl = ["z","y"]
        t = []
        for i in self.needctrl:
            t.append(ord(i))
        self.needctrl = t
        t = None

        for i in range(0,len("abgdevzTiklmnopJrstufqRySCcZwWxjh")):
            self.keymapkbd[ord("abgdevzTiklmnopJrstufqRySCcZwWxjh"[i])] = tuple([i + 4304])
        self.number_keys = {
                 'r':'1', 'R':'1', 't':'2','T':'2', 'y':'3',
                 'u':'*','f':'4','g':'5','h':'6','j':'#',
                 'v':'7', 'b':'8','n':'9','m':'0'
         }
        number_keys2 = {}
        for key,value in self.number_keys.items():
            number_keys2[ord(key)] = ord(value.decode('utf-8'))
        self.number_keys = number_keys2
        number_keys2 = None
        self.extend('s','შ')
        self.extend('w','ჭ')
        self.extend('r',['ღ','1'])
        self.extend('t',['თ','2'])
        self.extend('y','3')
        self.extend('u','*')
        self.extend('f','4')
        self.extend('g','5')
        self.extend('h','6')
        self.extend('j', ['ჟ','#'])
        self.extend('v','7')
        self.extend('b','8')
        self.extend('n','9')
        self.extend('m','0')
        self.extend('z','ძ')
        self.extend('c',['ჩ'])

    # # #
    def getDefaultConfig(self):
        cfg = geoinputbase.getDefaultConfig(self)
        cfg['keymapKbdExt'] = {}
        return cfg
    # # #
    def initKeymapkbdhs(self):
        for k, v in self.number_keys.items():
            values = list(self.keymapkbd[k])
            if v in values:
                values.remove(v)
            values.insert(0, v)
            self.keymapkbdhs[k] = tuple(values)
    # # #
    def configLoaded(self):
        geoinputbase.configLoaded(self)
        try:
            keymapKbdExt = self.c('keymapKbdExt')
            if keymapKbdExt is not None and type(keymapKbdExt) is dict:
                for key, value in self.config['keymapKbdExt'].items():
                    self.extend(key, value)
        except:
            self.printStackTrace()

        # # # init keys for home screen
        self.initKeymapkbdhs()


    def getKeymapkbd(self, key):
        if key not in self.keymapkbdhs:
            return self.keymapkbd
        if self.isExceptionInFg():
            return self.keymapkbdhs
        return self.keymapkbd
    ###
    def getSimKey(self, key):
        keymapkbd = self.getKeymapkbd(key)
        key_tuple = keymapkbd[key]
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

    def initMainCapturer(self):
        geoinputbase.initMainCapturer(self)
        self.mainCapturer = KeyCapturer(self.mainCallBack)
        self.mainCapturer.keys = tuple(self.keymapkbd.keys())
        self.mainCapturer.start()
        self.initSwitcherCapturers()

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


    def switcherCallBack(self, key):
        if key == self.switcherKey:
            now = self.now()
            timeDiff =  now - self.switcherFirsKeyLastClickAt
            self.switcherFirsKeyLastClickAt = now
            if timeDiff > 0.33:
                return
            self.switcherFirsKeyLastClickAt =  0
            self.toggle()

    def initSwitcherCapturers(self):#####
        self.switcherCapturer = KeyCapturer(self.switcherCallBack)
        self.switcherCapturer.keys = tuple([self.switcherKey])
        self.switcherCapturer.forwarding = 1
        self.switcherCapturer.start()

    def toggle(self):
        simulate_key(8,8)
        if self.currentLang == u'ka':
            self.currentLang = u'default'
            self.stop()
            if  self.c('noteSwitch') == 0:
                return True
            conf(u("default"))
            e32.ao_sleep(0.2)
            #simulate_key(EKeyHash, EScancodeHash)
        else:
            self.start()
            self.currentLang = u'ka'
            if  self.c('noteSwitch') == 0:
                return True
            conf(u('ქართული'))
            e32.ao_sleep(0.2)
            #simulate_key(EKeyHash, EScancodeHash)
            return True
