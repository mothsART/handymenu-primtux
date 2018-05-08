#!/usr/bin/python
# -*- coding:Utf-8 -*- 


"""
HandyMenu :     menu principal de la distribution
                HandyLinux <http://handylinux.org>

Auteurs :
            - HandyMenu-v1/2 : aka handy-menu
                arnault perret <arpinux@member.fsf.org>
                Meier Link <lucian.von.ruthven@gmail.com>
                manon crunchiikette <contact@handylinux.org>
                etienne de paris <contact@handylinux.org>
                fibi bestesterever <contact@handylinux.org>

            - HandyMenu v3 : aka handymenu
                Xavier Cartron (thuban@yeuxdelibad.net)
                Modifié par Tomasi pour PrimTux  

licence :       GNU General Public Licence v3
Description :   Handymenu from scratch
Dépendances :   python-gtk2

"""

version = "1.0"
auteur = "thuban modifié par Tomasi"
licence = "GPLv3"
homepage = "http://handylinux.org, http://primtux.fr"

import os
import sys
import pygtk
pygtk.require('2.0')
import gtk
import gettext
from hm_utils import *

gettext.bindtextdomain('handymenu', '/usr/share/locale')
gettext.textdomain('handymenu')
_ = gettext.gettext

class Handymenu():
    def close_application(self, widget, event, data=None):
        # tests nécessaires pour que seul clic-gauche et Entrée soient valables
        if event.type == gtk.gdk.BUTTON_RELEASE and \
                event.state & gtk.gdk.BUTTON1_MASK:
                gtk.main_quit()
        elif event.type == gtk.gdk.KEY_PRESS: 
            if event.keyval == gtk.keysyms.Return:
                gtk.main_quit()

    def configure(self, data=None):
        os.system(configcmd)
        gtk.main_quit()

#   def about(self, wid=None, data=None):
        # fenêtre à propos.
#        m = gtk.MessageDialog(type=gtk.MESSAGE_INFO,\
#           buttons = gtk.BUTTONS_OK)
#        m.set_markup(_('<b>Handymenu-PrimTux</b>\n\n\
#version : {0}\n\
#author : {1}\n\
#licence : {2}\n\
#homepage : {3}').format(version, auteur, licence, homepage))
#        ret = m.run()
#        if ret == gtk.RESPONSE_DELETE_EVENT or ret == gtk.RESPONSE_OK:
#            m.destroy()
    
    def add_recent(self,app):
        """add a recent application
        appname, icon, cmd= app['name'], app['icon'], app['cmd']
        """
        max = 6 # maximum d'applications récentes

        for s in self.config:
            if s['id'] == 'recent': # on prend la bonne section
                # check if app is not already in recents
                if app not in s['apps']:
                    s['apps'].insert(0,app)
                # on vire les vieux éléments
                if len(s['apps']) > max:
                    s['apps'].pop()
        save_config(self.config)

    def exec_app(self, widget, event, data):
        exe = False
        if event.type == gtk.gdk.BUTTON_RELEASE and \
                event.state & gtk.gdk.BUTTON1_MASK:
                exe = True
        elif event.type == gtk.gdk.KEY_PRESS: 
            if event.keyval == gtk.keysyms.Return:
                exe = True
        if exe:
            appname, icon, cmd= data['name'], data['icon'], data['cmd']
            os.system("{} &".format(cmd.strip()))
            self.add_recent(data)
            if self.closeafterrun:
                gtk.main_quit()

    def create_tabs(self):
        self.n_onglets = len(self.config)
        for s in self.config:
            # Description du bouton
            label = gtk.Label(s['name'])
            label.set_width_chars(onglet_width) # pour avoir des onglets uniformes
            # onglet coloré
            label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#41B1FF"))

            n = len(s['apps']) # number of apps to show
            if n <= 4: # si peu d'applications, 1 seule ligne
                r = 1
            else:
                r = 2 # two rows

            if n%2==0:  # nombre d'applis pair ou pas
                c = n/r - 1
            else:
                c = n/r 
            if n > 8 :  # beaucoup d'applications : + de 2 lignes
                c = 4
                r = n/c

            if n == 0 : # empty section
                c = 1

            page = gtk.Table(rows=r, columns=c, homogeneous=True)
            page.grab_focus()
            page.set_row_spacings(10)
            page.set_col_spacings(10)

            cur = [0,0]
            if n > 0:
                for a in s['apps']:
                    appname, icon, cmd, generic = a['name'], a['icon'], a['cmd'], a['generic']
                    # image utilisée dans le bouton
                    image = gtk.Image()
                    if icon.endswith('.png') or icon.endswith('.jpg'):
                        pixbuf = gtk.gdk.pixbuf_new_from_file(icon)
                        scaled_buf = pixbuf.scale_simple(iconsize,iconsize,gtk.gdk.INTERP_BILINEAR)
                        image.set_from_pixbuf(scaled_buf)
                    else:
                        image.set_from_icon_name(icon, gtk.ICON_SIZE_BUTTON)
                        image.set_pixel_size(iconsize)
                    # nom de l'appli
                    bapp = gtk.Button(label=appname)
                    bapp.set_image(image)
                    # l'image est au dessus du texte
                    bapp.set_image_position(gtk.POS_TOP)
                    # apparence du bouton
                    bapp.set_relief(gtk.RELIEF_NONE)
                    bapp.connect("button_release_event", self.exec_app, a)
                    bapp.connect("key_press_event", self.exec_app, a)
                    # Le bouton survolé change de couleur
                    bapp.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse("#41B1FF"))
                    # Description du bouton
                    bulledesc = gtk.Tooltips()
                    bulledesc.set_tip(bapp, generic)

                    page.attach(bapp, cur[0], cur[0]+1, cur[1], cur[1]+1,\
                        xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND|gtk.FILL,\
                        xpadding=5, ypadding=5)
                    if cur[0] < c:
                        cur[0] +=1
                    elif cur[0] == c:
                        cur[0] = 0
                        cur[1] += 1

                # pour centrer
                align = gtk.Alignment(0.5, 0.5, 0, 0)
                align.add(page)
                self.onglets.append_page(align, label)
            else:
                desc = gtk.Label(_("This menu is still empty"))
                align = gtk.Alignment(0.5, 0.5, 0, 0)
                align.add(desc)
                self.onglets.append_page(align, label)

        self.onglets.set_tab_label_packing(align, False, False, gtk.PACK_START)
        if self.n_onglets > maxonglets: # dyp il aime pas :P
            self.onglets.set_scrollable(True)# dyp y veut pas :P

    def close_after(self, widget):
        self.closeafterrun = widget.get_active()
        if not self.closeafterrun: #on enregistre de ne pas fermer
            with open(noclose,'w') as n:
                n.write('Thuban veut un câlin :P')
        elif os.path.isfile(noclose): #on ferme la prochiane fois
            os.remove(noclose)
            
    def make_menu(self):
        """build the menu"""
        # Conteneur principal
        mainbox = gtk.EventBox()
        self.window.add(mainbox)

        vbox = gtk.VBox(False, 2)
        vbox.set_border_width(15)
        mainbox.add(vbox)

        # Logo
        image = gtk.Image()
        image.set_from_file(primtuxmenuicon)
        logo = gtk.EventBox()
        logo.add(image)
#       logo.connect_object("button_release_event", self.about, None)
        bulledesc = gtk.Tooltips()
        bulledesc.set_tip(logo, _("Thuban/HandyLinux-Tomasi/PrimTux"))

        # Titre
        title = gtk.Label()
        title.set_markup('<span size="32000">Handy-PrimTux  </span>')
        title.set_justify(gtk.JUSTIFY_CENTER)
        linkbox = gtk.EventBox()
        linkbox.add(title)
        bulledesc = gtk.Tooltips()
        bulledesc.set_tip(linkbox, "http://primtux.fr")

        # boutons
        # bouton pour fermer
        closebtn = gtk.Button()
        croix = gtk.Image()
        croix.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        closebtn.set_image(croix)
                
        closebtn.set_relief(gtk.RELIEF_NONE)
        closebtn.connect("button_release_event", self.close_application)
        closebtn.connect("key_press_event", self.close_application)
        bulledesc = gtk.Tooltips()
        bulledesc.set_tip(closebtn, _("Close"))

       # fermer ou pas
        closeafterbtn = gtk.CheckButton()
        closeafterbtn.connect("toggled", self.close_after)
        closeafterbtn.set_active(self.closeafterrun)
        bulledesc = gtk.Tooltips()
        bulledesc.set_tip(closeafterbtn, _("Close after execution"))

        # configuration 
       # qbtn = gtk.Button()
       # image = gtk.Image()
       # image.set_from_stock(gtk.STOCK_PREFERENCES, gtk.ICON_SIZE_MENU)
       # qbtn.set_image(image)
       # qbtn.set_relief(gtk.RELIEF_NONE)
       # qbtn.connect_object("clicked", self.configure, None)
       # bulledesc = gtk.Tooltips()
       # bulledesc.set_tip(qbtn, _("Configure"))

        # boite à boutons 
        btnbox = gtk.VBox(False,0)
        btnbox.pack_start(closebtn, True, True, 0)
        # btnbox.pack_start(qbtn, True, True, 0)
        btnbox.pack_start(closeafterbtn, True, True, 0)

        # Boite d'en haut
        topbox = gtk.HBox(False, 0)
        topbox.pack_start(logo, True, True, 0)
        #topbox.pack_start(linkbox, True, True, 0)
        topbox.pack_start(btnbox, False, False, 0)

        vbox.pack_start(topbox, True, True, 0)

        # onglets
        self.onglets = gtk.Notebook()
        self.onglets.set_tab_pos(gtk.POS_TOP)
        self.onglets.set_show_border(False)
        align = gtk.Alignment(0.5, 0.5, 0, 0)
        align.add(self.onglets)
        vbox.pack_start(align, True, True, 0)

	# Boite d'en bas
        bottombox = gtk.HBox(True, 0)
        #bottombox.pack_start(logo, False, False, 0)
        #topbox.pack_start(linkbox, True, True, 0)
        bottombox.pack_start(btnbox, False, False, 0)
        vbox.pack_start(bottombox, False, False, 0)

        # Catégories
        self.create_tabs()

        self.window.show_all()

    def __init__(self):
        if os.path.isfile(noclose):
            self.closeafterrun = False
        else:
            self.closeafterrun = True
        self.n_onglets = 0 # nombre d'onglets
        try:
            self.config = load_config()
        except Exception as err:
            print(err)
            set_default_config()
            self.config = load_config()

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
#	self.window.maximize()
        self.window.connect("delete_event", lambda x,y: gtk.main_quit())

        self.window.set_title(menuname)
        self.window.set_border_width(1) # pour avoir une bordure noire
        self.window.set_icon_from_file(primtuxmenuicon)

        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_resizable(False)
        self.window.set_decorated(False)
        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        
        self.make_menu()
        self.onglets.grab_focus() # pour la gestion au clavier facilitée

def main():
    os.chdir(os.getenv('HOME'))
    menu = Handymenu()
    gtk.main()
    return 0        

if __name__ == "__main__":
    main()


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
