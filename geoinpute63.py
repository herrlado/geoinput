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
from geoinpute71 import geoinpute71
import keycapture
from keypress import simulate_key
from keycapture import KeyCapturer
from key_codes import EKeyBackspace, EScancodeBackspace, EModifierCtrl
from utils import u

class geoinpute63(geoinpute71):
    def __init__(self):
        geoinpute71.__init__(self)
    def init(self):
        geoinpute71.init(self)
        self.switcherKey = 17
    ###
    def getDefaultConfig(self):
        cfg = geoinpute71.getDefaultConfig(self)
        cfg['inputmode'] =  0
        cfg['switcherkey'] = chr(17 + 96) #q
        return cfg
    ###
    def configLoaded(self):
        geoinpute71.configLoaded(self)
        try:
            char = self.config['switcherkey']
            if char is None:
                char = 'q'
            self.switcherKey = ord(char.decode('utf-8')) - 96
        except:
            self.switcherKey = 17 #q
            self.printStackTrace()
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
