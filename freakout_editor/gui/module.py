import pygtk
pygtk.require("2.0")
import gtk

import os

import widget

class ModulePage(gtk.VBox):
    def __init__(self, parent, module):
        self.par = parent
        gtk.VBox.__init__(self)
        self.module_id = module.getLocalId()

    def render(self):
        pass

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
