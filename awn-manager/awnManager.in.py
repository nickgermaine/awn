#!/usr/bin/env python
#
#  Copyright (C) 2007 Neil Jagdish Patel <njpatel@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.
#
#  Author: Ryan Rushton <ryan@rrdesign.ca>
#
#  Notes: Avant Window Navigator Manager

import sys, os, os.path, time

PKGDATA = os.path.join("@DATADIR@", "avant-window-navigator", "awn-manager")
sys.path.append (PKGDATA)

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
    import gtk.gdk as gdk
except Exception, e:
    sys.stderr.write(str(e) + '\n')
    sys.exit(1)

from awnTheme import AwnThemeManager
from awnPreferences import awnPreferences
from awnApplet import awnApplet
from awnLauncher import awnLauncher
import awnDefs as defs

defs.i18nize(globals())

class AwnManager:

    def __init__(self):

        if not os.path.exists(defs.HOME_CONFIG_DIR):
            os.makedirs(defs.HOME_CONFIG_DIR)
        self.GLADE_PATH = os.path.join(PKGDATA, "window.glade")
        gtk.glade.bindtextdomain(defs.I18N_DOMAIN, defs.LOCALEDIR)
        gtk.glade.textdomain(defs.I18N_DOMAIN)

        self.wTree = gtk.glade.XML(self.GLADE_PATH, domain=defs.I18N_DOMAIN)

        self.window = self.wTree.get_widget("main_window")
        self.window.connect("delete-event", gtk.main_quit)

        refresh = self.wTree.get_widget("refreshbutton")
        refresh.connect("clicked", self.refresh)

        about = self.wTree.get_widget("aboutbutton")
        about.connect("clicked", self.about)

        close = self.wTree.get_widget("closebutton")
        close.connect("clicked", gtk.main_quit)

        #menu
        self.treeview =  self.wTree.get_widget("view_menu")
        self.treeview.get_selection().connect("changed", self.menu_row_clicked)
        self.make_menu_model()

        #theme
        self.themeManager = AwnThemeManager(self.wTree)

        #applet
        self.appletManager = awnApplet(self.wTree)

        #launcher
        self.launchManager = awnLauncher(self.wTree)

        #preferences
        self.prefManager = awnPreferences(self.wTree)

    def menu_row_clicked(self, data=None):
        selection = self.treeview.get_selection()
        (model, iterator) = selection.get_selected()
        if iterator is not None:
            self.show_panel(model.get_path(iterator)[0])

    def show_panel(self, index):
        panels = ['panel_preferences','panel_applets','panel_launchers','panel_themes']
        [self.wTree.get_widget(panel).hide() for panel in panels]
        self.wTree.get_widget(panels[index]).show()

    def make_menu_model (self):
        self.model = model = gtk.ListStore(gdk.Pixbuf, str, str, str)
        self.treeview.set_model (model)

        ren = gtk.CellRendererPixbuf()
        col = gtk.TreeViewColumn ("Pixbuf", ren, pixbuf=0)
        self.treeview.append_column (col)

        ren = gtk.CellRendererText()
        col = gtk.TreeViewColumn ("Name", ren, markup=1)
        self.treeview.append_column (col)

        theme = gtk.icon_theme_get_default()

        row = self.model.append ()
        self.model.set_value (row, 0, theme.load_icon (gtk.STOCK_PREFERENCES, 32, 0))
        self.model.set_value (row, 1, "General")

        row = self.model.append ()
        self.model.set_value (row, 0, theme.load_icon (gtk.STOCK_SORT_ASCENDING, 32, 0))
        self.model.set_value (row, 1, "Applets")

        row = self.model.append ()
        self.model.set_value (row, 0, theme.load_icon (gtk.STOCK_FULLSCREEN, 32, 0))
        self.model.set_value (row, 1, "Launchers")

        row = self.model.append ()
        self.model.set_value (row, 0, theme.load_icon (gtk.STOCK_HOME, 32, 0))
        self.model.set_value (row, 1, "Themes")

        path = self.model.get_path(self.model.get_iter_first())
        self.treeview.set_cursor(path, focus_column=None, start_editing=False)

    def refresh(self, button):
        w = gtk.Window()
        i = gtk.IconTheme()
        w.set_icon(i.load_icon("gtk-refresh", 48, gtk.ICON_LOOKUP_FORCE_SVG))
        v = gtk.VBox()
        l = gtk.Label("Refreshed")
        b = gtk.Button(stock="gtk-close")
        b.connect("clicked", self.win_destroy, w)
        v.pack_start(l, True, True, 2)
        v.pack_start(b)
        w.add(v)
        w.resize(200, 100)
        w.show_all()

    def about(self, button):
        self.about = gtk.AboutDialog()
        self.about.set_name("Avant Window Navigator")
        #self.about.set_version("bzr17")
        self.about.set_copyright("Copyright (C) 2007 Neil Jagdish Patel <njpatel@gmail.com>")
        self.about.set_authors(["Neil Jagdish Patel	<njpatel@gmail.com>", "haytjes <hv1989@gmail.com>", "Miika-Petteri Matikainen <miikapetteri@gmail.com>", "Anthony Arobone  <aarobone@gmail.com>", "Ryan Rushton <ryan@rrdesign.ca>", "Michal Hruby  <michal.mhr@gmail.com>", "Julien Lavergne <julien.lavergne@gmail.com>"])
        self.about.set_comments("Fully customisable dock-like window navigator for GNOME.")
        self.about.set_license('''
This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.''')
        self.about.set_wrap_license(True)
        self.about.set_website("http://www.planetblur.org/hosted/awnforum/")
        #self.about.set_logo_icon_name(gtk.STOCK_ABOUT)
        self.about.set_documenters(["More to come..."])
        self.about.set_artists(["More to come..."])
        #self.about.set_translator_credits()
        self.about.run()
        self.about.destroy()

    def win_destroy(self, button, w):
        w.destroy()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    awnmanager = AwnManager()
    awnmanager.main()
