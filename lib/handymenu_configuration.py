#!/usr/bin/python
# -*- coding:Utf-8 -*- 


"""
Description :
    Configuration du handymenu
"""

import sys
import os
import pygtk
pygtk.require('2.0')
import gtk
import gettext
import locale

from hm_utils import *

def get_info_desktop(desktopfile):
    """return infos from a .desktop file"""
    name, cmd, icon, generic= "", "", "", ""
    nameloc = False
    geneloc = False
    lang = locale.setlocale(locale.LC_ALL, "")[0:2]
    with open(desktopfile,'r') as d:
        df = d.readlines()
        for l in df:
            if generic == "" or geneloc == False:
                if l.startswith('GenericName[{0}]='.format(lang)):
                    generic = l.replace('GenericName[{0}]='.format(lang),'').strip()
                    geneloc = True
                elif l.startswith('GenericName='.format(lang)):
                    generic = l.replace('GenericName='.format(lang),'').strip()
            if name == "" or nameloc == False:
                if l.startswith('Name[{0}]='.format(lang)):
                    name = l.replace('Name[{0}]='.format(lang),'').strip()
                    nameloc = True
                elif l.startswith('Name='):
                    name = l.replace('Name=', '').strip()
            if cmd == "":
                if l.startswith('Exec='):
                    cmd = l.replace('Exec=', '').strip()
                    cmd = cmd.split('%')[0].strip()
            if icon == "":
                if l.startswith('Icon='):
                    icon = os.path.splitext(l.replace('Icon=', '').strip())[0]
    return(name, cmd, icon, generic)

class HandymenuConfig():
    def close_application(self, widget, event, data=None):
        os.system("{} --force &".format(join(self.utils.app_path, "handymenu-" + self.utils.appname)))
        gtk.main_quit()
        return False

    def appfinder(self, widget=None, event=None):
        os.system('rox /usr/share/applications &')

    def restart(self, widget=None, event=None):
        page = self.section_list.get_current_page()
        try:
            self.config = load_config()
        except Exception as err:
            print(err)
            self.config = load_default_config()
        self.window.destroy()
        self.make_menu()
        if page > len(self.config):
            page = 0
        self.section_list.set_current_page(page)

    def back_to_default(self, widget):
        set_default_config()
        self.restart()

    def add_new_section(self, widget):
        name = widget.get_text().strip()
        if len(name) != 0:
            newsec =  {'name' : name, 'id': "", 'apps': [] }
            add_section(self.config, newsec)
            self.restart()

    def del_section(self, section):
        self.config.remove(section)
        save_config(self.config)
        self.restart()
    
    def move_sec(self, section, index):
        reload = move_section(self.config, section, index)
        if reload:
            self.restart()

    def add_item_to_section(self, name, cmd, icon, generic, section):
        app = {'name' : name, 'icon' : icon, 'cmd' : cmd, 'generic' : generic}
        add_app(self.config, section, app)
        self.restart()

    def del_item_from_section(self, section, app):
        del_app(self.config, section, app)
        self.restart()

    def mod_app_name(self, widget, event, dialog, section, app):
        newname = widget.get_text().strip()
        if len(newname) != 0:
            mod_app(self.config, section, app, newname)
            self.restart()
        dialog.destroy()

    def mod_app_icon_dialog(self, widget, event, dialog, section, app):
        chooser = gtk.FileChooserDialog(title=self.utils._("Choose an icon"),action=gtk.FILE_CHOOSER_ACTION_OPEN,\
                buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        chooser.set_current_folder(pixmaps)
        filter = gtk.FileFilter()
        filter.set_name(self.utils._("Images"))
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        chooser.add_filter(filter)

        response = chooser.run()

        if response == gtk.RESPONSE_CANCEL:
            print(self.utils._('Closed, no files selected'))
            chooser.destroy()
        elif response == gtk.RESPONSE_OK:
            i = chooser.get_filename()
            chooser.destroy()
            mod_app_icon(self.config, section, app, i)
            self.restart()

        dialog.destroy()

    def move_app_up(self, widget, dialog, section, app):
            move_app(self.config, section, app, -1)
            dialog.destroy() 
            self.restart()

    def move_app_down(self, widget, dialog, section, app):
            move_app(self.config, section, app, 1)
            dialog.destroy() 
            self.restart()

    def on_drag_data_received(self, widget, context, x, y, selection, target_type, timestamp, section):
        data = selection.data.strip().replace('%20', ' ') # On retire le retour à la ligne et le code des espaces
        if data.startswith('file://'):
            f = data.replace("file://", "").strip()
            if os.path.isdir(f): # parse directories
                name = os.path.basename(f)
                cmd = 'exo-open --launch FileManager "{}"'.format(f)
                icon = "folder"
                self.add_item_to_section(name, cmd, icon, None, section)
            elif os.path.isfile(f): # is it file?
                if data.endswith('.desktop'):
                    name, cmd, icon, generic = get_info_desktop(f)
                    self.add_item_to_section(name, cmd, icon, generic, section)
                else:
                    name = os.path.basename(f)
                    cmd = 'exo-open "{}"'.format(f)
                    self.add_item_to_section(name, cmd, "empty", None, section) #raccourci pour fichier sans icone
        elif data.startswith("http://") or \
                data.startswith("https://") or \
                data.startswith("ftp://"):  # cas d'une url
            name = data.split('/')[2]
            cmd = "exo-open --launch WebBrowser {}".format(data)
            self.add_item_to_section(name, cmd, "text-html", "Lien vers une url", section) 

        widget.destroy()

    def add_appli(self, section):
        w = gtk.Dialog(parent=self.window)
        w.connect("delete_event", self.restart)
        w.set_size_request(360, 150)
        TARGET_TYPE_URI_LIST = 80
        dnd_list = [ ( 'text/uri-list', 0, TARGET_TYPE_URI_LIST ) ]
        w.drag_dest_set( gtk.DEST_DEFAULT_MOTION |
                  gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP,
                  dnd_list, gtk.gdk.ACTION_COPY)

        w.connect("drag_data_received", self.on_drag_data_received, section)
        l = gtk.Label(self.utils._("Drag an icon here to create a launcher"))
        w.vbox.pack_start(l, True, True, 10)

        appfinderbtn = gtk.Button(label=self.utils._("Search for applications"))
        appfinderbtn.connect("button_press_event", self.appfinder)
        w.action_area.pack_start(appfinderbtn, True, True, 0)
        appfinderbtn.show()
        l.show()
        
        ret = w.run()
        if ret == gtk.RESPONSE_DELETE_EVENT:
            w.destroy()
    
    def del_appli(self, widget, dialog, section, app):
        self.del_item_from_section(section, app)
        dialog.destroy() # delete parent

    def edit_appli(self, widget, event, section, app):
        d = gtk.Dialog(title=self.utils._("Edit the launcher"))
        # Edition du nom de l'appli
        entry = gtk.Entry()
        entry.connect("activate", self.mod_app_name, entry, d, section, app) # entrée valide
        entry.show()

        namebtn = gtk.Button(label = self.utils._("Change"))
        namebtn.connect_object("clicked", self.mod_app_name, entry, None, d, section, app )
        namebtn.show()

        # on met ça dans une boîte
        box = gtk.HBox(False,2)
        box.pack_start(entry, True, True, 3)
        box.pack_start(namebtn, False, False, 0)
        box.show()
        
        # et le tout dans un étiquette
        nameframe = gtk.Frame(self.utils._("Change the label"))
        nameframe.add(box)
        nameframe.show()

        icon = app["icon"]
        iconpreview = gtk.Image()
        if icon.endswith('.png') or icon.endswith('.jpg'):
            iconpreview.set_from_file(icon)
        else:
            iconpreview.set_from_icon_name(icon, iconsize)
            iconpreview.set_pixel_size(iconsize)
        iconpreview.show()

        # Changement de l'icône
        iconbtn = gtk.Button(label = self.utils._("Change icon"))
        iconbtn.connect_object("clicked", self.mod_app_icon_dialog, entry, None, d, section, app )
        iconbtn.show()

        # on met ça dans une boîte
        
        # et le tout dans un étiquette
        iconframe = gtk.Frame(self.utils._("Change the application icon"))
        iconframe.add(iconbtn)
        iconframe.show()

        # déplacement de l'application
        upbtn = gtk.Button(label=self.utils._("Move up"))
        downbtn = gtk.Button(label=self.utils._("Move down"))

        upi = gtk.Image()
        upi.set_from_stock(gtk.STOCK_GO_UP, gtk.ICON_SIZE_MENU)
        upbtn.set_image(upi)
        downi = gtk.Image()
        downi.set_from_stock(gtk.STOCK_GO_DOWN, gtk.ICON_SIZE_MENU)
        downbtn.set_image(downi)

        upbtn.connect_object("clicked", self.move_app_up, None, d, section, app)
        downbtn.connect_object("clicked", self.move_app_down, None, d, section, app)

        upbtn.show()
        downbtn.show()
        # on met ça dans une boîte
        box = gtk.HBox(False,2)
        box.pack_start(upbtn, True, True, 3)
        box.pack_start(downbtn, False, False, 0)
        box.show()
        
        # et le tout dans un étiquette
        moveframe = gtk.Frame(self.utils._("Move this app"))
        moveframe.add(box)
        moveframe.show()

        # Nécessaire pour la suppression
        delbtn = gtk.Button(label = self.utils._("Delete"), stock=gtk.STOCK_DELETE)
        delbtn.connect("clicked", self.del_appli, d, section, app)
        delbtn.show()
        delframe = gtk.Frame(self.utils._("Delete this launcher"))
        delframe.add(delbtn)
        delframe.show()

        # ajout des objets au dialogue
        d.vbox.pack_start(nameframe)
        hbox = gtk.HBox(False, 2)
        hbox.pack_start(iconpreview)
        hbox.pack_start(iconframe)
        hbox.show();
        d.vbox.pack_start(hbox, True, True, 0)

        d.vbox.pack_start(moveframe)
        d.vbox.pack_start(delframe)
        d.run()

    def make_entrylist(self):
        self.section_list = gtk.Notebook()
        self.section_list.set_tab_pos(gtk.POS_LEFT)   
        self.section_list.set_scrollable(True)

        for s in self.config:
            label = gtk.Label(s['name'])
            applist = gtk.VBox()

            scrolled_window = gtk.ScrolledWindow()
            scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            scrolled_window.set_size_request(620,-1)
            self.section_list.append_page(scrolled_window, label)

            # boutons de config
            hb = gtk.HBox(False, 10)

            delbtn = gtk.Button(label = self.utils._("Delete this section"))
            delbtn.connect_object("clicked", self.del_section, s)

            addbtn = gtk.Button(label = self.utils._("Add an application"))
            addbtn.connect_object("clicked", self.add_appli, s)
            
            hb.pack_start(addbtn)
            hb.pack_start(delbtn)
            
            if self.config.index(s) > 0:
                upbtn = gtk.Button(label = self.utils._("Move section up"))
                upbtn.connect_object("clicked", self.move_sec, s, -1)
                hb.pack_start(upbtn)
            if self.config.index(s) < len(self.config)-1:
                downbtn = gtk.Button(label = self.utils._("Move section down"))
                downbtn.connect_object("clicked", self.move_sec, s, +1)
                hb.pack_start(downbtn)



            applist.pack_start(hb, False,False, 10)

            for a in s['apps']:
                appname, icon, cmd= a['name'], a['icon'], a['cmd']
                image = gtk.Image()
                if icon.endswith('.png') or icon.endswith('.jpg'):
                    image.set_from_file(icon)
                else:
                    image.set_from_icon_name(icon, iconsize)
                    image.set_pixel_size(iconsize)
                # nom de l'appli
                bapp = gtk.Button(label=appname)
                bapp.set_image(image)
                #l'image est au dessus du texte
                bapp.set_image_position(gtk.POS_TOP)
                # apparence du bouton
                bapp.set_relief(gtk.RELIEF_NONE)
                bapp.connect("button_release_event", self.edit_appli, s, a)
                applist.pack_start(bapp)


            scrolled_window.add_with_viewport(applist)

        # ajout de la possibilité d'ajouter des sections
        addbox = gtk.VBox()
        instruction = gtk.Label(self.utils._("Name of the new section: "))
        entry = gtk.Entry()
        entry.connect("activate", self.add_new_section) # entrée valide
        addbox.pack_start(instruction, False, True, 3)
        addbox.pack_start(entry, False, False, 20)

        addbtn = gtk.Button(label = self.utils._("More"), stock=gtk.STOCK_ADD)
        addbtn.connect_object("clicked", self.add_new_section, entry )
        addbox.pack_start(addbtn, False, False, 10)

        addlabel = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join(self.utils.primtux_icons,"add_section.png"))
        scaled_buf = pixbuf.scale_simple(24,24,gtk.gdk.INTERP_BILINEAR)
        addlabel.set_from_pixbuf(scaled_buf)
        bulledesc = gtk.Tooltips()
        bulledesc.set_tip(addlabel, self.utils._("Add a section"))
        self.section_list.append_page(addbox, addlabel)

        self.mainbox.pack_start(self.section_list)
    
    def make_menu(self):
        """build the menu"""
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.close_application)

        self.window.set_title("Handymenu configuration")
        self.window.set_border_width(0)

        # Conteneur principal
        self.mainbox = gtk.VBox(False, 10)
        self.mainbox.set_border_width(10)

        # configuration principale
        self.make_entrylist()

        # conteneur pour les boutons
        btnbox = gtk.HBox(True, 2)
        self.mainbox.pack_start(btnbox, False, False, 0)

        defaultbtn = gtk.Button(label = self.utils._("Reset"))
        resetimg = gtk.Image()
        resetimg.set_from_stock(gtk.STOCK_REDO, gtk.ICON_SIZE_BUTTON)
        defaultbtn.set_image(resetimg)
        defaultbtn.connect_object("clicked", self.back_to_default, self.window )
        btnbox.pack_start(defaultbtn, fill= False)

        savebtn = gtk.Button(label = self.utils._("Quit"), stock=gtk.STOCK_CLOSE)
        savebtn.connect_object("clicked", self.close_application, self.window, None )
        btnbox.pack_start(savebtn, fill= False)

        self.window.add(self.mainbox)
        self.window.set_default_size(620, 560)
        self.window.show_all()

    def __init__(self, appname):
        self.appname = appname
        self.utils = Utils(appname)
        try:
            self.config = self.utils.load_config()
        except Exception as err:
            print(err)
            self.config = self.utils.load_default_config()
        self.make_menu()

def main(appname):
    menu = HandymenuConfig(appname)
    gtk.main()
    return 0        

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
