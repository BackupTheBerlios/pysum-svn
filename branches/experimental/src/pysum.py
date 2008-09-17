#! /usr/bin/env python
# -*- coding: UTF-8 -*-

# pysum - A pygtk app to create and check md5 and other checksum 
# Copyright (C) 2008 Daniel Fuentes Barría <dbfuentes@gmail.com>
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
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


# Importamos los modulos necesarios
import md5
import gettext
import os.path

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

# directorio con los archivos necesarios

resources_dir = "/usr/share/pysum"

# Algunas cosas para gettext (i18n - traducciones)

_ = gettext.gettext

gettext.textdomain("pysum")
gtk.glade.textdomain("pysum")

# Clase con la informacion del programa (para no escribir tanto)

class Pysum:
    "Store the program information"
    name = "pySum"
    version = "svn rev 8"
    copyright = "Copyright © 2008 Daniel Fuentes B."
    authors = ["Daniel Fuentes Barría <dbfuentes@gmail.com>"]
    website = "http://pysum.berlios.de/"
    description = _("A pygtk application for create and verify md5 and other checksum")
    license = "This program is free software; you can redistribute it and/or modify \
it under the terms of the GNU General Public License as published by \
the Free Software Foundation; either version 2 of the License, or \
(at your option) any later version. \n\n\
This program is distributed in the hope that it will be useful, but \
WITHOUT ANY WARRANTY; without even the implied warranty of \
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. \
See the GNU General Public License for more details. \n\n\
You should have received a copy of the GNU General Public License \
along with this program; if not, write to the Free Software Foundation, Inc., \
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA."


# Definimos una funcion para obtener la suma md5 de los archivos
def getmd5(filename):
    "Calculate MD5 hash for a file without full-load in memory"
    try:
        fichero = open(filename, "rb")
    except:
        pass
        #print _("Can't open the file:"), filename

    suma = md5.new()
    while True:
        data = fichero.read(10240)
        if not data:
            break
        suma.update(data)

    fichero.close()
    return suma.hexdigest()

# Funcion para obtener una lista con los archivos a comprobar de la
# forma [["archivo1","suma1","dir1"], ["archivo2","suma2","dir2"]]
def listasumas(filename):
    "Get a list of files and checksums"
    try:
        fichero = open(filename, "rb")
    except:
        print _("Can't open the file:"), filename

    lista = []
    # tranformar rutas como /home/user/midoc.txt en /home/user/
    ruta_bruta = os.path.split(filename)
    ruta = ruta_bruta[0] 

    for linea in fichero:
        ruta_arch = str(os.path.join(ruta, (linea [34:-1])))
        minilista = [linea [34:-1], linea[0:32], ruta_arch]
        lista.append(minilista)

    fichero.close()
    return lista

# Interfaz grafica (gtk-glade)
# Clase para el Loop principal (de la interfaz grafica)

class Gui:
    "This is the pysum application. This is a pyGTK window"
    def __init__(self):
        # Le indicamos al programa que archivo XML de glade usar.
        # la comprobacion es para que funcione el paquete debian
        if os.path.exists("pysum.glade"):
            self.widgets = gtk.glade.XML("pysum.glade")
        else:
            self.widgets = gtk.glade.XML(os.path.join(resources_dir, "pysum.glade"))

        # Creamos un diccionario con los manejadores definidos en glade
        # y sus respectivas llamadas.
        signals = {
                   "on_buttonopen1_clicked" : self.on_buttonopen1_clicked,
                   "on_button2_clicked" : self.on_button2_clicked,
                   "on_about1_activate" : self.on_about1_activate,
                   "gtk_main_quit" : gtk.main_quit,
                   }

        # Autoconectamos las signals.
        self.widgets.signal_autoconnect(signals)

        # Del archivo glade obtenemos los widgets a usar.
        self.entry1 = self.widgets.get_widget("entry1")

        # widgests de la ventana de comprobacion
        self.checkwindow = self.widgets.get_widget("checkwindow")
        self.labeldialog1 = self.widgets.get_widget("labeldialog1")
        self.labeldialog2 = self.widgets.get_widget("labeldialog2")
        self.labeldialog3 = self.widgets.get_widget("labeldialog3")
        self.labeldialog4 = self.widgets.get_widget("labeldialog4")

# De aqui en adelante comienza las acciones propias del programa
# Como las ventanas especiales y las acciones a realizar

    # Funcion para abrir archivos (dialogo abrir archivo)
    def file_browse(self):
        "This function is used to browse for a file. Is a open dialog"
        dialog_buttons = (gtk.STOCK_CANCEL
                        , gtk.RESPONSE_CANCEL
                        , gtk.STOCK_OPEN
                        , gtk.RESPONSE_OK)
        file_open = gtk.FileChooserDialog(title=_("Select a file")
                    , action=gtk.FILE_CHOOSER_ACTION_OPEN
                    , buttons=dialog_buttons)
        # regresar la ruta del archivo
        resultado = ""
        if file_open.run() == gtk.RESPONSE_OK:
            resultado = file_open.get_filename()
        file_open.destroy()
        return resultado

    # Ventana de error
    def error(self, message):
        "Display the error dialog "
        dialog_error = gtk.MessageDialog(parent=None, flags=0, buttons=gtk.BUTTONS_OK)
        dialog_error.set_title(_("Error"))
        label = gtk.Label(message)
        dialog_error.vbox.pack_start(label, True, True, 0)
        label.show()
        dialog_error.run()
        dialog_error.destroy()

    # Ventana Acerca de.
    def about_info(self,data=None):
        "Display the About dialog "
        about = gtk.AboutDialog()
        about.set_name(Pysum.name)
        about.set_version(Pysum.version)
        about.set_comments(Pysum.description)
        about.set_copyright(Pysum.copyright)

        def openHomePage(widget,url,url2): #para abrir el sitio
            import webbrowser
            webbrowser.open_new(url)

        gtk.about_dialog_set_url_hook(openHomePage,Pysum.website)
        about.set_website(Pysum.website)
        about.set_authors(Pysum.authors)
        about.set_license(Pysum.license)
        about.set_wrap_license(True) #Adapta el texto a la ventana
        about.run()
        about.destroy()

    # lanza la ventana para comprobar sumas
    def check_win(self, files):
        progreso = 0
        good = 0
        bad = 0
        miss = 0
        self.checkwindow.show()
        for arch in files:
            progreso = progreso + 1
            total = "Check file %s of %s" % (progreso, len(files)) 
            self.labeldialog1.set_text(total)
            try:
#Nota: son de la forma arch = [nombre(0), suma(1), ruta_completa(2)]
                if (getmd5(arch[2])) == (arch[1]):
                    good = good + 1
                    print "%s  %s  OK" % (arch[1], arch[0])
                    self.labeldialog2.set_text(str(good))
                elif (getmd5(arch[2])) != (arch[1]):
                    bad = bad +1
                    print "%s  %s  Bad" % (arch[1], arch[0])
                    self.labeldialog3.set_text(str(bad))
            except:
                miss = miss +1
                print "%s  Missing (the file could not be read)"  % (arch[0])
                self.labeldialog4.set_text(str(miss))
            
# le devolvemos temporalmente el control a gtk para refrescar la ventana
# Mas info en: http://faq.pygtk.org/index.py?req=show&file=faq23.020.htp
            while gtk.events_pending():
                gtk.main_iteration(False)


# Declaramos las acciones a realizar (menus, botones, etc.):

    # Definimos las acciones de los menus
    def on_about1_activate(self, widget):
        self.about_info()

    # Definimos las acciones de los botones:
    def on_buttonopen1_clicked(self, widget):# Boton abrir
        ruta_archivo = self.file_browse() 
        self.entry1.set_text(ruta_archivo)

    def on_button2_clicked(self, widget): #Boton para iniciar comprobacion
        archivo = self.entry1.get_text() #obtiene la ruta desde la entrada
        if (len(archivo) == 0):
            self.error(_("Please choose a file"))
        else:
            try:
                milista = listasumas(archivo)
                self.check_win(milista) #mostral la ventana de chequeo
            except:
                self.error(_("Can't open the file: ") + archivo)

if __name__== "__main__":
    Gui()
    gtk.main()
