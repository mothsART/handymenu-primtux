#!/usr/bin/python
# -*- coding:Utf-8 -*- 
# utils for handymenu

import os
import pickle
import gettext

# options for handymenu
menuname = "HandyMenu"
configfile=os.path.expanduser('/home/02-super/.handymenu.conf')
noclose=os.path.expanduser('/home/02-super/.handymenu-noclose.conf')
hmdir="/usr/share/handymenu-super"
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
    {'name' : _("Accueil"),\
    'id': 6,\
    'apps': [\
                {'name' : _("Internet"),\
        'generic': _("Firefox"),\
        'icon' : "firefox",\
        'cmd' : "firefox"\
        },\
          {'name' : _("Fichiers"),\
        'generic': _("Pcmanfm"),\
        'icon' : "pcmanfm",\
        'cmd' : "/usr/bin/pcmanfm /home/02-super/Documents"\
        },\
        {'name' : _("Écrire"),\
        'generic': _("Ecrire"),\
        'icon' : "libreoffice-writer",\
        'cmd' : "libreoffice --writer"\
        },\
        {'name' : _("Arrêter"),\
        'generic': _("Arrêter"),\
        'icon' : "system-shutdown",\
        'cmd' : "/usr/bin/shutdown"\
        },\
    ]\
    },\
{'name' : _("Français"),\
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
        {'name' : _("Écrire"),\
        'generic': _("Écrire"),\
        'icon' : "libreoffice-writer",\
        'cmd' : "libreoffice --writer"\
          },\
            {'name' : _("AbulEdu Aller"),\
        'generic': _("AbulEdu Aller"),\
        'icon' : "abuledu-aller",\
        'cmd' : "aller-super"\
         },\
         {'name' : _("AbulEdu - Associations"),\
        'generic': _("AbulEdu - Associations"),\
        'icon' : "abuledu-associations",\
        'cmd' : "/usr/bin/associations-super"\
        },\
                 {'name' : _("AbulEdu Imageo"),\
        'generic': _("AbulEdu Imageo"),\
        'icon' : "abuledu-imageo",\
        'cmd' : "leterrier-imageo"\
        },\
           {'name' : _("TBO"),\
        'generic': _("TBO"),\
        'icon' : "tbo",\
        'cmd' : "tbo"\
        },\
    ]\
    },\

    {'name' : _("Calcul"),\
    'id': 1,\
    'apps': [\
        {'name' : _("A nous les nombres"),\
        'generic': _("AbulEdu A nous les nombres"),\
        'icon' : "abuledu-anouslesnombres",\
        'cmd' : "anous-super"\
        },\
        {'name' : _("Calcul-Mental"),\
        'generic': _("Abuledu Calcul-Mental"),\
        'icon' : "abuledu-calculs",\
        'cmd' : "leterrier-calcul-mental"\
        },\
        {'name' : _("Calcul Reflechi"),\
        'generic': _("AbulEdu Calcul Reflechi"),\
        'icon' : "abuledu-calculreflechi",\
        'cmd' : "mathoeuf-super"\
        },\
        {'name' : _("Calculs"),\
        'generic': _("AbulEdu Calculs"),\
        'icon' : "abuledu-calculs",\
        'cmd' : "calculs-super"\
        },\
        {'name' : _("Operations"),\
        'generic': _("Abuledu Operations"),\
        'icon' : "abuledu-operations",\
        'cmd' : "operations-super"\
        },\
        {'name' : _("SuiteArithmetique"),\
        'generic': _("AbulEdu SuiteArithmetique"),\
        'icon' : "leterrier-suitearithmetique",\
        'cmd' : "leterrier-suitearithmetique"\
        },\
   {'name' : _("AbulEdu Contour"),\
        'generic': _("AbulEdu A nous les nombres"),\
        'icon' : "abuledu-contourjeu",\
        'cmd' : "contour-super"\
        },\
  {'name' : _("AbulEdu Suites"),\
        'generic': _("AbulEdu Suites"),\
        'icon' : "abuledu-suites",\
        'cmd' : "suites-super"\
        },\
     ]\
    },\

    {'name' : _("Calcul 2"),\
    'id': 7,\
    'apps': [\
             {'name' : _("AbulEdu Tierce"),\
        'generic': _("AbulEdu Tierce"),\
        'icon' : "/usr/share/icons/Faenza/apps/48/gnome-sudoku.png",\
        'cmd' : "leterrier-tierce"\
        },\
        {'name' : _("Calculatrice"),\
        'generic': _("Calculatrice"),\
        'icon' : "accessories-calculator",\
        'cmd' : "qalculate-gtk"\
        },\
        {'name' : _("Calculette capricieuse"),\
        'generic': _("Calculette capricieuse"),\
        'icon' : "leterrier-calccap",\
        'cmd' : "leterrier-calculette-capricieuse"\
        },\
        {'name' : _("FreeMaths"),\
        'generic': _("FreeMaths"),\
        'icon' : "/usr/share/icons/Faenza/apps/48/gnome-tetravex.png",\
        'cmd' : "/usr/bin/freemaths"\
        },\
 {'name' : _("Fubuki"),\
        'generic': _("Fubuki"),\
        'icon' : "leterrier-fubuki",\
        'cmd' : "leterrier-fubuki"\
        },\
        {'name' : _("Le Terrier Cible"),\
        'generic': _("Le Terrier Cible"),\
        'icon' : "leterrier-cibler",\
        'cmd' : "leterrier-cibler"\
        },\
        {'name' : _("Problèmes"),\
        'generic': _("Problèmes"),\
        'icon' : "problemes",\
        'cmd' : "problemes-super"\
        },\
        {'name' : _("Tux Math"),\
        'generic': _("Tux Math"),\
        'icon' : "tuxmath",\
        'cmd' : "tuxmath"\
        },\
        {'name' : _("Multiplication"),\
        'generic': _("Multiplication Station"),\
        'icon' : "multiplicationstation-0.8.0",\
        'cmd' : "multiplication-station"\
        },\
           ]\
},\
    {'name' : _("Géométrie"),\
    'id': 4,\
    'apps': [\
          {'name' : _("AbulEdu Chemin"),\
        'generic': _("AbulEdu Chemin"),\
        'icon' : "abuledu-chemin",\
        'cmd' : "chemin-super"\
         },\
         {'name' : _("AbulEdu Symcolor"),\
        'generic': _("AbulEdu Symcolor"),\
        'icon' : "abuledu-symcolor",\
        'cmd' : "symcolor-super"\
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
              {'name' : _("DrGEo"),\
        'generic': _("DrGeo"),\
        'icon' : "drgeo",\
        'cmd' : "drgeo"\
           },\
    ]\
 },\
    {'name' : _("Compilations"),\
    'id': 3,\
    'apps': [\
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
        {'name' : _("pySioGame"),\
        'generic': _("pySioGame"),\
        'icon' : "pysiogame",\
        'cmd' : "/usr/bin/pysiogame"\
        },\
      ]\
    },\
        {'name' : _("Déc. du Monde"),\
    'id': 8,\
    'apps': [\
            {'name' : _("Internet"),\
        'generic': _("Firefox"),\
        'icon' : "firefox",\
        'cmd' : "firefox"\
        },\
                    {'name' : _("Scratch"),\
        'generic': _("Scratch"),\
        'icon' : "scratch",\
        'cmd' : "scratch %f"\
        },\
                            {'name' : _("Stellarium"),\
        'generic': _("Stellarium"),\
        'icon' : "stellarium",\
        'cmd' : "stellarium"\
        },\
                            {'name' : _("Microscope virtuel"),\
        'generic': _("Microscope virtuel"),\
        'icon' : "microscope",\
        'cmd' : "/usr/bin/micro"\
        },\
       ]\
    },\

    {'name' : _("Jeux"),\
    'id': 5,\
    'apps': [\
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
        {'name' : _("Monsterz"),\
        'generic': _("Monsterz"),\
        'icon' : "monsterz",\
        'cmd' : "monsterz"\
        },\
        {'name' : _("Ri-li"),\
        'generic': _("Ri-li"),\
        'icon' : "ri-li",\
        'cmd' : "ri-li"\
        },\
{'name' : _("Seahorse Adventures"),\
        'generic': _("Seahorse Adventures"),\
        'icon' : "seahorse-adventures",\
        'cmd' : "seahorse-adventures"\
        },\
{'name' : _("SuperTux"),\
        'generic': _("SuperTux"),\
        'icon' : "supertux",\
        'cmd' : "supertux"\
        },\
       {'name' : _("AbulEdu Mulot"),\
        'generic': _("AbulEdu Mulot"),\
        'icon' : "abuledu-mulot",\
        'cmd' : "mulot-super"\
        },\
        {'name' : _("Jnavigue"),\
        'generic': _("Jnavigue"),\
        'icon' : "logoJnavigue",\
        'cmd' : "/usr/bin/jnavigue.sh"\
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
    ]\
}\
]
