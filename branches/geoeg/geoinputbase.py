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
# thanks to Dixtosa for timer idea
# based on idea of k60mm
#
from keypress import *
import appuifw, e32
import keycapture
import appswitch
import globalui
import applist
from key_codes import EKeyBackspace, EKey0, EKey1, EKey2, EKey3, EKey4, EKey5, EKey6, EKey7, EKey8, EKey9, EKeyHash,  EKeyBackspace, EScancodeBackspace, EModifierCtrl, EScancodeHash
import time
import sys
import os
from utils import *
from versions import *

UID = "20027ad1"

APPVERSION = u'1.1.5'

APPNAME = u"geoinput"


###
class geoinputbase(object):

    __CLOCK_OFFSET = int(round(time.time())) - int(round(time.clock()))

    __CONFIG_FILE = u"C:\\Data\\geoinput\\config.cfg"

    __BASE_CONFIG  = { 'hidden' : 0,'kaonstart' : 0,'noteSwitch' : 1, 'simplemenu' : 0, 'exceptions' : [] }



    # # #
    def __init__(self):
        self.backspaceCapturer = None

        self.lastKey = 0
        self.mod = 0
        self.lastClickAt = 0
        self.currentLang = u'ru'



        self.exceptions = []

        self.init()

        self.config = self.getDefaultConfig()

        self.initConfig()

        self.initCapturers()

        self.initEnvy()
        # END __init__

    def init(self):
        pass

    # # #
    def getDefaultConfig(self):
        return self.__BASE_CONFIG

    # # #
    def loadConfig(self):
        try:
            f = open(self.__CONFIG_FILE,'r+')
            for line in f:
                key, value = line.split("=", 1)
                self.config[key.strip()] = eval(value.strip())
            f.close()
        except :
            self.printStackTrace()
            self.config = self.getDefaultConfig()
        self.configLoaded()


    # # #
    def configLoaded(self):
        try:
            if self.config['exceptions'] is not None:
                d = []
                for ex in self.config['exceptions']:
                    d.append(ex)
                self.exceptions = d
        except:
            self.printStackTrace()

    # # #
    def checkConfigPath(self):
        try:
            if os.path.exists("C:\\Data\\geoinput"):
                return
            if not os.path.exists("C:\\Data"):
                os.makedirs("C:\\Data")
            os.makedirs("C:\\Data\\geoinput")
        except:
            self.printStackTrace()
            return False
    # # #
    def initConfig(self):
        try:
            self.checkConfigPath()
            if not os.path.exists(self.__CONFIG_FILE):
                self.saveConfig(self.getDefaultConfig())
            self.loadConfig()
        except:#FALLBACK
            self.printStackTrace()
            self.config = self.getDefaultConfig()
            self.configLoaded()

    # # #
    def saveConfig(self, cfg):
        try:
            self.checkConfigPath()
            f = open(self.__CONFIG_FILE,'w')
            for key, value in cfg.items():
                print >> f, "%s = %s" % (key, repr(value))
            f.close()
            return True
        except:
            self.printStackTrace()
            return False

    # # #
    def form2config(self, form):
        self.config['kaonstart'] =  int(form[0][2][1])
        self.config['hidden'] =     int(form[1][2][1])
        self.config['noteSwitch'] = int(form[2][2][1])
        self.config['simplemenu'] = int(form[3][2][1])


    # # #
    def save_hook_menu(self,form):
        self.form2config(form)
        self.saveConfig(self.config)
        return True


    def getConfigMenuFormList(self):
        INDICATOR = [u('არა'),u('კი')]
        kaonstart = self.c('kaonstart')
        hidden = self.c('hidden')
        noteSwitch = self.c('noteSwitch')
        simplemenu = self.c('simplemenu')
        return [(u("ავტო ენა"), "combo", (INDICATOR, kaonstart)),
            (u("დამალვა"), "combo", (INDICATOR, hidden)),
            (u("ინდიკატორი"), "combo", (INDICATOR, noteSwitch)),
            (u("მარტივი მენუ"),"combo", (INDICATOR, simplemenu))
                ]

    # # #
    def getConfigMenuForm(self):
        form = appuifw.Form(self.getConfigMenuFormList(),appuifw.FFormEditModeOnly)
        return form

    # # #
    def showConfigMenu(self):
        form = self.getConfigMenuForm()
        form.menu = []
        form.save_hook = self.save_hook_menu
        form.execute()

    # # #
    def initMainCapturer(self):
        pass

    # # #
    def stopMainCapturer(self):
        pass

    def startMainCapturer(self):
        pass

    # # #
    def initBackspaceCapturer(self):
        self.backspaceCapturer = keycapture.KeyCapturer(self.backspaceCallBack)
        self.backspaceCapturer.keys = (EKeyBackspace,)
        self.backspaceCapturer.forwarding = 1
        self.backspaceCapturer.start()

    # # #
    def initCapturers(self):
        self.initMainCapturer()
        self.initBackspaceCapturer()
        if not self.c('kaonstart') == 1:
            self.currentLang = u'default'
            self.stop()
    # # #
    def removeExceptions(self, apps):
        for app in apps:
            if app in self.exceptions :
                self.exceptions.remove(app)
        self.config['exceptions'] = self.exceptions
        self.saveConfig(self.config)
        return True
    # # #
    def removeException(self, app):
        apps = []
        apps.append(app)
        return self.removeExceptions(apps)
    # # #
    def addExceptions(self, apps):
        for app in apps:
            if app not in self.exceptions:
                self.exceptions.append(app)
        self.config['exceptions'] = self.exceptions
        self.saveConfig(self.config)
        return True
    # # #
    def addException(self, app):
        apps  = []
        apps.append(app)
        return apps

    # # #
    def removeExceptionMenu(self):
        if len(self.exceptions) == 0 :
            info(u("გამონაკლისები არ არის!"))
            return
        items = appuifw.multi_selection_list(self.exceptions, style='checkbox', search_field=1)
        if len(items) == 0:
            return
        apps_to_remove = []
        for i in items:
            apps_to_remove.append(self.exceptions[i])
        self.removeExceptions(apps_to_remove)
        info(u("წაიშალა"))
    # # #
    def captureExceptionMenu(self):
        import applist
        a = applist.applist()
        if len(a) == 0:
            return
        apps = []
        for i in a:
            apps.append(i[1])
        for ex in self.exceptions:
            if ex in apps:
                apps.remove(ex)
        self.stopMainCapturer()

        items = appuifw.multi_selection_list(apps, style='checkbox', search_field =  1)

        if len(items) == 0:
            return
        apps_to_add = []
        for i in items:
            apps_to_add.append(apps[i])
        self.addExceptions(apps_to_add)
        info(u("დაემატა"))

    # # #
    def initEnvy(self):
        try:
            import envy
            envy.set_app_system(1)
            if self.c('hidden') == 1:
                envy.set_app_hidden(1)
        except:
            self.printStackTrace()

    # # # get 0 or 1 #
    def c(self, key):
        if key not in self.config:
            return self.getDefaultConfig()[key]
        value = 0
        if self.config[key] > 0:
            return 1
        return value

    # # #
    def now(self):
        return time.clock() + self.__CLOCK_OFFSET

    # # #
    def needToggle(self):
        pass

    # # #
    def checkTime(self):
        now = self.now()
        timeDiff =  now - self.lastClickAt
        if timeDiff > 0.75 :
            self.mod = 0
            self.lastKey= 0
        self.lastClickAt = now

    # # #
    def isExceptionInFg(self):
        return len(self.exceptions) > 0 and appswitch.fg_appname() in self.exceptions


    # # #
    def backspaceCallBack(self, key):
        self.lastKey = 0
        self.lastClickAt = 0
        self.backspaceCapturer.stop()

    # # #
    def toggle(self):
        if self.currentLang == u'ka':
            self.currentLang = u'default'
            self.stop()
            if  self.c('noteSwitch') == 0:
                return True
            conf(u("default"))
            e32.ao_sleep(0.2)
        else:
            self.start()
            self.currentLang = u'ka'
            if  self.c('noteSwitch') == 0:
                return True
            conf(u('ქართული'))
            e32.ao_sleep(0.2)
            return True



    # # #
    def start(self):
        try:
            self.startMainCapturer()
        except:
            self.printStackTrace()
    # # #
    def stop(self):
        self.stopMainCapturer()
        self.backspaceCapturer.stop()
        self.currentLang = u'default'

    # # #
    def shutdown(self):
        self.backspaceCapturer.stop()
        del self.backspaceCapturer

    # # #
    def aboutDlg(self):
        info(unicode("geoinput\n") + u("ვერსია ") + unicode(APPVERSION) + u"\n\xa9 2009" + u("ლადო ქუმსიაშვილი"))
    # # #
    def showUID(self):
        appuifw.query(appuifw.app.uid(), 'query')

    # # #
    def helpDlg(self):
        progpath = os.path.split(sys.argv[0])[0]
        if appuifw.app.uid() != UID: # running as a script
            progpath = progpath[:2] + '/Python'
        manpage = os.path.join(progpath, 'manual.html').replace('/', '\\')
        appuifw.note(u(manpage))
        appuifw.Content_handler().open(u(manpage))


    # # #
    def printStackTrace(self, note=True):
        errorString = self.getException()
        if note:
            error(u("შეცდომა! დამატებითი ინფორმაცია") + unicode(" log ") +u("ფაილში"))
        self.log(errorString)

    # # #
    def getException(self):
        import sys
        import traceback
        cla, exc, trbk = sys.exc_info()
        excName = cla.__name__
        try:
            excArgs = exc.__dict__["args"]
        except KeyError:
            excArgs = "<no args>"
        excTb = traceback.format_tb(trbk, 5)
        errorString = repr(excName) + '-' + repr(excArgs) + '-' + repr(excTb) + '\n'
        return errorString


    # # #
    def log(self, message):
        self.checkConfigPath()
        #appuifw.app.body.add(u(message)+"\n")
        f = open(u"C:\\Data\\geoinput\\log.txt","a")
        f.write(message + "\n")
        f.close()



    # # #
    def quit(self):
        self.shutdown()
        self.app_lock.signal()
        if appuifw.app.uid() == UID:
            appuifw.app.set_exit() # running as app

    # # #
    def toggleMenu(self):
        l = []
        if self.currentLang == u'ka':
            l.append(u('რუსული *'))
            l.append(u'default')
        else:
            l.append(u('რუსული'))
            l.append(u'default *')
        items = appuifw.popup_menu(l)

        if items == None:
            return
        if items == 0: #ქარ
            if self.currentLang == u'ru':
                return
            self.toggle()
        else:
            if self.currentLang == u'default':
                return
            self.toggle()

    # # #
    def createMenu(self):
        if self.c("simplemenu") == 1:
            return [ (u("ენა"), self.toggleMenu),
                     (u("გასვლა"), self.quit)]


        return [ (u("ენა"), self.toggleMenu),
                 (u("გამონაკლისები"), ((u("დამატება"), self.captureExceptionMenu),(u("წაშლა"), self.removeExceptionMenu))),
                 (u("კონფიგურაცია"), self.showConfigMenu),
                 (u("დახმარება"), ((u("დახმარება"), self.helpDlg),
                (u("შესახებ"), self.aboutDlg),)),
                 (u("გასვლა"), self.quit)]


    # # #
    def run(self):
        self.app_lock = e32.Ao_lock()

        appuifw.app.title = APPNAME

        appswitch.switch_to_bg(APPNAME)

        appuifw.app.body = appuifw.Text()

        appuifw.app.menu = self.createMenu()

        appuifw.app.exit_key_handler=self.quit

        self.app_lock.wait()
