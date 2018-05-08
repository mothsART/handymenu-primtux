#!/usr/bin/python
# -*- coding:Utf-8 -*- 
# utils for handymenu

import os
from os.path import dirname, join
import pickle
import gettext

# options for handymenu
menuname = "HandyMenu"
configfile=os.path.expanduser('/home/01-mini/.handymenu.conf')
if not os.path.isfile(configfile):
    # On est dans un cadre de DEBUG
    configfile=os.path.expanduser(join(dirname(__file__), 'handymenu.conf'))
noclose=os.path.expanduser('/home/01-mini/.handymenu-noclose.conf')
hmdir="/usr/share/handymenu-mini"
if not os.path.isfile(hmdir):
    # On est dans un cadre de DEBUG
    hmdir=dirname(__file__)
pixmaps="/usr/share/pixmaps"
configcmd="python {} &".format(os.path.join(hmdir,"handymenu-configuration.py")) 
primtux_icons=os.path.join(pixmaps,hmdir,"icons")
primtuxmenuicon=os.path.join(primtux_icons,"primtuxmenu_icon.png")

onglet_width = 18
maxonglets = 4
iconsize = 64

gettext.bindtextdomain('handymenu', '/usr/share/locale')
gettext.textdomain('handymenu')
_ = gettext.gettext

def set_default_config():
    print("reset configuration")
    with open(configfile, 'wb') as pkl:
        pickle.dump(hm_default_sections, pkl, pickle.HIGHEST_PROTOCOL)

def load_config():
    with open(configfile, 'rb') as pkl:
        try:
            config = pickle.load(pkl)
        except: #ancienne configuration ou config erronée?
            set_default_config()
            config = load_config()
        return(config)

def save_config(conf):
    with open(configfile, 'wb') as pkl:
        pickle.dump(conf, pkl, pickle.HIGHEST_PROTOCOL)

def add_section(config, section):
    config.append(section)
    save_config(config)
    
def move_section(config, section, index):
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

def add_app(config, section, app):
    for s in config:
        if s == section:
            s['apps'].append(app)
            save_config(config)

def del_app(config, section, app):
    for s in config:
        if s == section:
            s['apps'].remove(app)
            save_config(config)

def mod_app(config, section, app, new):
    for s in config:
        if s == section:
            for a in s['apps']:
                if a == app:
                    a['name'] = new
                    save_config(config)

def mod_app_icon(config, section, app, newicon):
    for s in config:
        if s == section:
            for a in s['apps']:
                if a == app:
                    a['icon'] = newicon
                    save_config(config)

def move_app(config, section, app, index):
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

#app = {'name' : "Description l'application",\
#        'generic' : "Nom générique de l'application",\
#        'icon' : "icône de l'application",\
#        'cmd' : "commande"}
#applist = [app1, app2, app3, ...]
#section = {'name': 'Recent', 'apps' : applist , id : ''}
#sections = [section1, section2,...]
hm_default_sections = \
[\
    {'name' : _("Français-Maths"),\
    'id': 9,\
    'apps': [\
           {'name' : _("Écrire"),\
        'generic': _("Ecrire"),\
        'icon' : "libreoffice-writer",\
        'cmd' : "libreoffice --writer"\
        },\
        {'name' : _("A nous les nombres"),\
        'generic': _("AbulEdu A nous les nombres"),\
        'icon' : "abuledu-anouslesnombres",\
        'cmd' : "anous-mini"\
        },\
    {'name' : _("AbulEdu Contour"),\
        'generic': _("AbulEdu A nous les nombres"),\
        'icon' : "abuledu-contourjeu",\
        'cmd' : "contour-mini"\
        },\
        {'name' : _("AbulEdu Suites"),\
        'generic': _("AbulEdu Suites"),\
        'icon' : "abuledu-suites",\
        'cmd' : "suites-mini"\
        },\
        {'name' : _("AbulEdu Chemin"),\
        'generic': _("AbulEdu Chemin"),\
        'icon' : "abuledu-chemin",\
        'cmd' : "chemin-mini"\
         },\
         {'name' : _("AbulEdu Symcolor"),\
        'generic': _("AbulEdu Symcolor"),\
        'icon' : "abuledu-symcolor",\
        'cmd' : "symcolor-mini"\
        },\
             {'name' : _("Tangrams"),\
        'generic': _("Tangrams"),\
        'icon' : "gtans",\
        'cmd' : "gtans"\
        },\
                     {'name' : _("Labyrinthe"),\
        'generic': _("Labyrinthe"),\
        'icon' : "labytux",\
        'cmd' : "/usr/share/Omega/labyrinthe-linux/Labyrinthe"\
        },\
                   {'name' : _("Labyrinthe caché"),\
        'generic': _("Labyrinthe caché"),\
        'icon' : "laby-cache",\
        'cmd' : "/usr/share/Omega/labyrinthe-cache-linux/Labyrinthe-cache"\
        },\
                             {'name' : _("Comparaison"),\
        'generic': _("Comparaison"),\
        'icon' : "comparaison",\
        'cmd' : "/usr/share/Omega/comparaison-linux/comparaison"\
        },\
                   {'name' : _("Piles"),\
        'generic': _("Piles"),\
        'icon' : "/usr/share/icons/Faenza/actions/48/document-properties.png",\
        'cmd' : "/usr/share/Omega/piles-linux/piles"\
        },\
    ]\
    },\
    {'name' : _("Compilations-Jeux"),\
    'id': 7,\
    'apps': [\
       {'name' : _("AbulEdu Mulot"),\
        'generic': _("AbulEdu Mulot"),\
        'icon' : "abuledu-mulot",\
        'cmd' : "mulot-mini"\
        },\
        {'name' : _("KLettres"),\
        'generic': _("KLettres"),\
        'icon' : "klettres",\
        'cmd' : "klettres"\
        },\
        {'name' : _("PySyCache"),\
        'generic': _("PySyCache"),\
        'icon' : "pysycache",\
        'cmd' : "pysycache"\
        },\
                {'name' : _("Tux Paint"),\
        'generic': _("Tux Paint"),\
        'icon' : "tuxpaint",\
        'cmd' : "tuxpaint"\
        },\
         {'name' : _("Childsplay"),\
        'generic': _("Childsplay"),\
        'icon' : "childsplay",\
        'cmd' : "childsplay --language=fr"\
        },\
        {'name' : _("GCompris"),\
        'generic': _("Suite éducative GCompris"),\
        'icon' : "gcompris",\
        'cmd' : "gcompris"\
        },\
        {'name' : _("Omnitux"),\
        'generic': _("Omnitux"),\
        'icon' : "omnitux",\
        'cmd' : "/usr/bin/omnitux"\
        },\
        {'name' : _("Help Hannah's Horse"),\
        'generic': _("Help Hannah's Horse"),\
        'icon' : "hannah",\
        'cmd' : "hannah"\
        },\
        {'name' : _("Monsieur Patate"),\
        'generic': _("Monsieur Patate"),\
        'icon' : "ktuberling",\
        'cmd' : "ktuberling"\
        },\
        {'name' : _("Ri-li"),\
        'generic': _("Ri-li"),\
        'icon' : "ri-li",\
        'cmd' : "ri-li"\
        },\
{'name' : _("SuperTux"),\
        'generic': _("SuperTux"),\
        'icon' : "supertux",\
        'cmd' : "supertux"\
        },\
          {'name' : _("Internet"),\
        'generic': _("Firefox"),\
        'icon' : "firefox",\
        'cmd' : "firefox"\
        },\
 {'name' : _("Arrêter"),\
        'generic': _("Arrêter"),\
        'icon' : "system-shutdown",\
        'cmd' : "/usr/bin/shutdown"\
        },\
    ]\
}\
]
