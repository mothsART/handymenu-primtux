#!/usr/bin/python
# -*- coding:Utf-8 -*- 
# utils for handymenu

import os
from os.path import dirname, join
import yaml
import io
import gettext

# options for handymenu
menuname = "HandyMenu"
configfile=os.path.expanduser('/usr/share/handyconfig-primtux/handymenu.yaml')
if not os.path.isfile(configfile):
    # On est dans un cadre de DEBUG
    configfile=os.path.expanduser(join(dirname(__file__), 'handymenu.yaml'))
noclose=os.path.expanduser('/home/administrateur/.handymenu-noclose.conf')
hmdir="/usr/share/handymenu"
if not os.path.isfile(hmdir):
    # On est dans un cadre de DEBUG
    hmdir=dirname(__file__)
pixmaps="/usr/share/pixmaps"
configcmd="python {} &".format(os.path.join(hmdir,"handymenu-configuration.py")) 
primtux_icons=os.path.join(pixmaps,hmdir,"icons")
primtuxmenuicon=os.path.join(primtux_icons,"primtuxmenu_icon.png")

onglet_width = 12
maxonglets = 9
iconsize = 64

gettext.bindtextdomain('handymenu', '/usr/share/locale')
gettext.textdomain('handymenu')
_ = gettext.gettext

def set_default_config():
    print("reset configuration")
    with io.open(configfile, 'w', encoding='utf8') as pkl:
        yaml.dump(hm_default_sections, pkl, default_flow_style=False, allow_unicode=True)

def load_config():
    with io.open(configfile, 'r') as stream:
        try:
            config = yaml.load(stream)
        except: #ancienne configuration ou config erronée?
            set_default_config()
            config = load_config()
        return(config)

def save_config(conf):
    with io.open(configfile, 'w', encoding='utf8') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False, allow_unicode=True)

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
    {'name' : _("Écriture"),\
    'id': 9,\
    'apps': [\
            {'name' : _("Dictionnaire"),\
        'generic': _("Dictionnaire"),\
        'icon' : "dicorime",\
        'cmd' : "dicorime"\
        },\
        {'name' : _("Multi-Dictionnaire"),\
        'generic': _("Multi-Dictionnaire"),\
        'icon' : "goldendict",\
        'cmd' : "goldendict"\
        },\
        {'name' : _("Conjugaison"),\
        'generic': _("Conjugaison"),\
        'icon' : "Le_Conjugueur2",\
        'cmd' : "/usr/bin/leconjugueur"\
        },\
        {'name' : _("LibreOffice"),\
        'generic': _("LibreOffice"),\
        'icon' : "libreoffice-startcenter",\
        'cmd' : "libreoffice"\
        },\
        {'name' : _("Écrire"),\
        'generic': _("Écrire"),\
        'icon' : "libreoffice-writer",\
        'cmd' : "libreoffice --writer"\
        },\
        {'name' : _("Tableaux"),\
        'generic': _("Tableaux"),\
        'icon' : "libreoffice-calc",\
        'cmd' : "libreoffice --calc"\
        },\
        {'name' : _("Composition"),\
        'generic': _("Composition"),\
        'icon' : "libreoffice-draw",\
        'cmd' : "libreoffice --draw"\
        },\
      {'name' : _("Diaporamas"),\
        'generic': _("Diaporamas"),\
        'icon' : "libreoffice-impress",\
        'cmd' : "libreoffice --impress"\
        },\
        {'name' : _("Math"),\
        'generic': _("Math"),\
        'icon' : "libreoffice-math",\
        'cmd' : "libreoffice --math"\
        },\
                {'name' : _("LibreOffice Base"),\
        'generic': _("LibreOffice Base"),\
        'icon' : "libreoffice-base",\
        'cmd' : "libreoffice --base"\
        },\
        {'name' : _("Agenda"),\
        'generic': _("Agenda Personnel"),\
        'icon' : "osmo",\
        'cmd' : "osmo"\
        },\
		{'name' : _("Journal"),\
        'generic': _("Prise de notes manuscrites"),\
        'icon' : "xournal",\
        'cmd' : "xournal"\
        },\
	{'name' : _("Calculatrice"),\
        'generic': _("Calculatrice"),\
        'icon' : "qalculate",\
        'cmd' : "qalculate-gtk"\
        },\
	{'name' : _("TBO"),\
        'generic': _("TBO"),\
        'icon' : "tbo",\
        'cmd' : "tbo"\
        },\
    ]\
    },\

    {'name' : _("Audio-Vidéo"),\
    'id': 0,\
    'apps': [\
            {'name' : _("Audacity"),\
        'generic': _("Audacity"),\
        'icon' : "audacity",\
        'cmd' : "audacity"\
         },\
                    {'name' : _("Convertisseur audio"),\
        'generic': _("Convertisseur audio"),\
        'icon' : "soundconverter",\
        'cmd' : "soundconverter"\
        },\
           {'name' : _("VLC"),\
        'generic': _("VLC"),\
        'icon' : "vlc",\
        'cmd' : "vlc"\
        },\
           {'name' : _("Éditeur vidéo"),\
        'generic': _("Éditeur vidéo"),\
        'icon' : "openshot",\
        'cmd' : "openshot"\
        },\
           {'name' : _("Gravure"),\
        'generic': _("Gravure"),\
        'icon' : "media-cdrom",\
        'cmd' : "xfburn"\
        },\
    ]\
    },\

    {'name' : _("Images"),\
    'id': 1,\
    'apps': [\
                        {'name' : _("Scanner"),\
        'generic': _("Scanner"),\
        'icon' : "xsane",\
        'cmd' : "xsane"\
        },\
          {'name' : _("Capture d'écran"),\
        'generic': _("Capture d'écran"),\
        'icon' : "shutter",\
        'cmd' : "shutter"\
        },\
        {'name' : _("Gimp"),\
        'generic': _("Éditeur d'images"),\
        'icon' : "gimp",\
        'cmd' : "gimp"\
        },\
        {'name' : _("Pinta"),\
        'generic': _("Éditeur d'images"),\
        'icon' : "pinta",\
        'cmd' : "pinta"\
        },\
          ]\
    },\

    {'name' : _("Système"),\
    'id': 5,\
    'apps': [\
         {'name' : _("Écrans"),\
        'generic': _("Écrans"),\
        'icon' : "display",\
        'cmd' : "arandr"\
        },\
        {'name' : _("Impression"),\
        'generic': _("Impression"),\
        'icon' : "printer",\
        'cmd' : "system-config-printer"\
        },\
        {'name' : _("Éditeur de menu"),\
        'generic': _("Éditeur de menu"),\
        'icon' : "menulibre",\
        'cmd' : "/usr/bin/menulibre"\
        },\
        {'name' : _("Terminal"),\
        'generic': _("Terminal"),\
        'icon' : "utilities-terminal",\
        'cmd' : "roxterm"\
        },\
        {'name' : _("Éditeur de partitions"),\
        'generic': _("Éditeur de partitions"),\
        'icon' : "gparted",\
        'cmd' : "gparted-pkexec"\
        },\
{'name' : _("Clavier"),\
        'generic': _("Clavier"),\
        'icon' : "preferences-desktop-keyboard",\
        'cmd' : "fskbsetting"\
        },\
{'name' : _("Apparence"),\
        'generic': _("Apparence"),\
        'icon' : "preferences-desktop-theme",\
        'cmd' : "lxappearance"\
        },\
 {'name' : _("Logiciels"),\
        'generic': _("Gestionnaire de logiciels"),\
        'icon' : "solydxk-softwaremanager",\
        'cmd' : "gksudo solydxk-softwaremanager"\
          },\
 {'name' : _("Synaptic"),\
        'generic': _("Gestionnaire de paquets"),\
        'icon' : "synaptic",\
        'cmd' : "/usr/local/bin/primtux/synupdate"\
          },\
 {'name' : _("Freeware-Nc"),\
        'generic': _("Logiciels supplémentaires"),\
        'icon' : "freeware-64",\
        'cmd' : "gksudo /usr/local/bin/primtux/non-free/check"\
          },\
 {'name' : _("Samba"),\
        'generic': _("Partager des fichiers"),\
        'icon' : "system-config-samba",\
        'cmd' : "gksu system-config-samba"\
          },\
 {'name' : _("Gigolo"),\
        'generic': _("Visionneur de fichiers distants"),\
        'icon' : "gtk-network",\
        'cmd' : "gigolo"\
          },\
        {'name' : _("Open-Sankore"),\
        'generic': _("Open-Sankore"),\
        'icon' : "sankore",\
        'cmd' : "/usr/local/Open-Sankore-2.5.1/run.sh"\
        },\
           
    ]\
}\
]
