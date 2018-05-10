#!/usr/bin/python
# -*- coding:Utf-8 -*- 
# utils for handymenu

import os
from os.path import dirname, join, expanduser, isfile
import yaml
import io
import gettext

onglet_width = 12
maxonglets = 9
iconsize = 64

class Utils():
    def __init__(self, appname):
        self.appname = appname
        self.handymenu_path = dirname(dirname(__file__))
        self.app_path = join(self.handymenu_path, "handymenu-{}".format(appname))
        local_path = '/usr/share/locale'
        # options for handymenu
        self.menuname="HandyMenu session {}".format(appname)
        self.defaultconfigfile=expanduser('/etc/handymenu-{}.default.yaml'.format(appname))
        if not isfile(self.defaultconfigfile):
            # On est dans un cadre de DEBUG
            self.defaultconfigfile=expanduser(join(self.app_path, 'handymenu-{}.default.yaml').format(appname))
            local_path = join(self.handymenu_path, 'locale')
        self.configfile=expanduser('/etc/handymenu-{}.yaml'.format(appname))
        if not isfile(self.configfile):
            # On est dans un cadre de DEBUG
            self.configfile=os.path.expanduser(join(self.app_path, 'handymenu-{}.yaml'.format(appname)))
        self.noclose = expanduser('/etc/handymenu-{}-noclose.conf'.format(appname))
        hmdir="/usr/share/handymenu"
        self.primtux_icons = join(hmdir, "icons")
        if not isfile(hmdir):
            # On est dans un cadre de DEBUG
            hmdir=self.app_path
            self.primtux_icons = join(self.handymenu_path, "icons")
        self.configcmd="python {0} {1} &".format(join(self.handymenu_path, "handymenu-configuration.py"), appname)
        self.primtuxmenuicon=join(self.primtux_icons, "primtuxmenu_icon-{}.png".format(appname))
        gettext.bindtextdomain('handymenu', local_path)
        gettext.textdomain('handymenu')
        self._ = gettext.gettext

    def load_default_config(self):
        with io.open(self.defaultconfigfile, 'r') as stream:
            try:
                self.defaultconfig = yaml.load(stream)
            except:
                raise "!!!!"
            return(self.defaultconfig)
    
    def load_config(self):
        with io.open(self.configfile, 'r') as stream:
            try:
                config = yaml.load(stream)
            except:
                return load_default_config()
            for s in config:
                n = len(s['apps'])
                if n > 0:
                    try:
                        for a in s['apps']:
                            appname, icon, cmd, generic = a['name'], a['icon'], a['cmd'], a['generic']
                    except:
                        config = load_default_config()
            return(config)
    
    def save_config(self, conf):
        with io.open(self.configfile, 'w', encoding='utf8') as outfile:
            yaml.dump(conf, outfile, default_flow_style=False, allow_unicode=True)
    
    def add_section(self, config, section):
        config.append(section)
        save_config(config)
        
    def move_section(self, config, section, index):
        """move section of +1 or -1
        index = +1  or -1
        """
        toreload=False
        for s in config:
            if s == section:
                idx = config.index(s)
                if index == -1 : # on recule l'application
                    if idx > 0 :
                        config[idx], config[idx-1] = config[idx-1], config[idx]
                elif index == 1 : # on avance l'application
                    if idx < len(config) - 1:
                        config[idx], config[idx+1] = config[idx+1], config[idx]
                save_config(config)
                toreload=True
                break
        return(toreload)
    
    def add_app(self, config, section, app):
        for s in config:
            if s == section:
                s['apps'].append(app)
                save_config(config)
    
    def del_app(self, config, section, app):
        for s in config:
            if s == section:
                s['apps'].remove(app)
                save_config(config)
    
    def mod_app(self, config, section, app, new):
        for s in config:
            if s == section:
                for a in s['apps']:
                    if a == app:
                        a['name'] = new
                        save_config(config)
    
    def mod_app_icon(self, config, section, app, newicon):
        for s in config:
            if s == section:
                for a in s['apps']:
                    if a == app:
                        a['icon'] = newicon
                        save_config(config)
    
    def move_app(self, config, section, app, index):
        """move app of +1 or -1
        index = +1  or -1
        """
        for s in config:
            if s == section:
                for a in s['apps']:
                    if a == app:
                        idx = s['apps'].index(a)
        
                        if index == -1 : # on recule l'application
                            if idx > 0 :
                                s['apps'][idx -1], s['apps'][idx] = s['apps'][idx], s['apps'][idx-1]
                        elif index == 1 : # on avance l'application
                            if idx < len(s['apps']) - 1:
                                s['apps'][idx], s['apps'][idx+1] = s['apps'][idx+1], s['apps'][idx]
                        save_config(config)
                        break
