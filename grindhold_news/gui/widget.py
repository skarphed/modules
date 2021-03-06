#!/usr/bin/python
#-*- coding: utf-8 -*-

###########################################################
# © 2011 Daniel 'grindhold' Brendle and Team
#
# This file is part of Skarphed.
#
# Skarphed is free software: you can redistribute it and/or 
# modify it under the terms of the GNU Affero General Public License 
# as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
#
# Skarphed is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public 
# License along with Skarphed. 
# If not, see http://www.gnu.org/licenses/.
###########################################################

import pygtk
pygtk.require("2.0")
import gtk

import os

from skarphedadmin.data.skarphed.Skarphed import module_rpc

from skarphedadmin.gui.skarphed.ViewGenerationControl import ViewGenerationControl
from skarphedadmin.gui.InputBox import InputBox

class WidgetPage(gtk.VBox):
    def __init__(self, parent, widget):
        self.par = parent
        gtk.VBox.__init__(self)
        self.widgetId = widget.getLocalId()

        self._news = {}
        self._current_entry = {}

        path = os.path.realpath(__file__)
        path = path.replace("widget.pyc","")
        self._path = path.replace("widget.py","")

        self.builder = gtk.Builder()
        self.builder.add_from_file(self._path+"widget.glade")
        self.handlers = {
            "save_cb"           : self.saveCallback,
            "new_cb"            : self.newCallback,
            "choose_news_cb"    : self.chooseNewsCallback,
            "delete_cb"         : self.deleteCallback,
            "toggle_nws_del_cb" : self.toggleDeleteNewsCallback,
            "toggle_com_del_cb" : self.toggleDeleteCommentCallback
        }
        self.builder.connect_signals(self.handlers)

        self.widget = self.builder.get_object("widget")

        self._newsstore = self.builder.get_object("newsstore")
        self._commentstore = self.builder.get_object("commentstore")

        self.widget.pack_start(ViewGenerationControl(self, widget),False)

        self.add(self.widget)
        self.loadNews()

    def render(self):
        def search_news(model,path,rowiter):
            nr = model.get_value(rowiter,4)
            if str(nr) not in self._news.keys():
                self._itersToRemove.append(rowiter)
            else:
                model.set_value(rowiter,1,self._news[str(nr)]["title"])
                model.set_value(rowiter,2,self._news[str(nr)]["author"])
                model.set_value(rowiter,3,self._news[str(nr)]["date"])
            self._news_handled.append(nr)
        
        def search_comments(model,path,rowiter):
            comments = self._current_entry["comments"]
            nr = model.get_value(rowiter,4)
            if str(nr) not in comments.keys():
                self._itersToRemove.append(rowiter)
            else:
                model.set_value(rowiter,1,comments[str(nr)]["date"])
                model.set_value(rowiter,2,comments[str(nr)]["author"])
                model.set_value(rowiter,3,comments[str(nr)]["content"])
            self._comments_handled.append(nr)

        self._news_handled = []
        self._itersToRemove = []
        self._newsstore.foreach(search_news)

        for rowiter in self._itersToRemove:
            self._newsstore.remove(rowiter)

        for nr in self._news.keys():
            if int(nr) not in self._news_handled:
                self._newsstore.append((False,
                                        self._news[nr]["title"],
                                        self._news[nr]["author"],
                                        self._news[nr]["date"],
                                        int(nr)))

        del(self._news_handled)

        if self._current_entry != {}:
            self._itersToRemove = []
            self._comments_handled = []

            self._commentstore.foreach(search_comments)

            for rowiter in self._itersToRemove:
                self._commentstore.remove(rowiter)

            for nr in self._current_entry["comments"].keys():
                if int(nr) not in self._comments_handled:
                    self._commentstore.append((False,
                                               self._current_entry["comments"][nr]["date"],
                                               self._current_entry["comments"][nr]["author"],
                                               self._current_entry["comments"][nr]["content"],
                                               int(nr)))
            del(self._comments_handled)

            self.builder.get_object("title").set_sensitive(True)
            self.builder.get_object("content").set_sensitive(True)
            self.builder.get_object("save").set_sensitive(True)
            self.builder.get_object("title").set_text(self._current_entry["title"])
            self.builder.get_object("content").get_buffer().set_text(self._current_entry["content"])
            self.builder.get_object("r_public").set_inconsistent(False)
            self.builder.get_object("r_private").set_inconsistent(False)
            self.builder.get_object("r_public").set_active(self._current_entry["show"])
            self.builder.get_object("r_private").set_active(not self._current_entry["show"])
        else:
            self.builder.get_object("title").set_text("")
            self.builder.get_object("content").get_buffer().set_text("")
            self.builder.get_object("title").set_sensitive(False)
            self.builder.get_object("content").set_sensitive(False)
            self.builder.get_object("save").set_sensitive(False)
            self.builder.get_object("r_public").set_inconsistent(True)
            self.builder.get_object("r_private").set_inconsistent(True)

            self._commentstore.clear()


        del(self._itersToRemove)

    def loadNewsCallback(self,data):
        self._news = data
        self.render()

    @module_rpc(loadNewsCallback)
    def get_news(self):
        pass

    def loadNews(self):
        self.get_news()


    def loadNewsEntryCallback(self,data):
        self._current_entry = data
        self.render()

    @module_rpc(loadNewsEntryCallback)
    def get_news_entry(self, entry_id):
        pass

    def loadNewsEntry(self, entry_id):
        self.get_news_entry(entry_id)

    def chooseNewsCallback(self, tree=None, path=None, data=None):
        selection = self.builder.get_object("newsview").get_selection()
        rowiter = selection.get_selected()[1]
        if not rowiter:
            return
        nr = self._newsstore.get_value(rowiter,4)
        self.loadNewsEntry(nr)

    def savedEntryCallback(self, data):
        self.loadNewsEntry(self._current_entry["id"])

    @module_rpc(savedEntryCallback)
    def save_news_entry(self, saving_entry):
        pass

    def saveCallback(self, widget=None, data=None):
        self._saving_entry = self._current_entry

        self._saving_entry["title"] = self.builder.get_object("title").get_text()
        textbuffer = self.builder.get_object("content").get_buffer()
        self._saving_entry["content"] = textbuffer.get_text(textbuffer.get_start_iter(),textbuffer.get_end_iter())
        self._saving_entry["show"] = self.builder.get_object("r_public").get_active()
        self.save_news_entry(self._saving_entry)

    def createNewEntryCallback(self, data):
        self.loadNews()

    def newCallback(self, widget=None, data=None):
        InputBox(self, "Please enter the title of the new news-entry", self.executeNew, notEmpty=True)

    @module_rpc(createNewEntryCallback)
    def create_news_entry(self, title):
        pass

    def executeNew(self, title):
        self.create_news_entry(title)

    def deleteEntriesCallback(self, data):
        self.loadNewsEntry(self._current_entry["id"])
        self.loadNews()

    @module_rpc(deleteEntriesCallback)
    def delete_entries(self, data):
        pass
    
    def deleteCallback(self, data):
        self._nws_to_delete = []
        self._com_to_delete = []
        def search_news(model,path,rowiter):
            if model.get_value(rowiter,0):
                self._nws_to_delete.append(model.get_value(rowiter,4))
        
        def search_comments(model,path,rowiter):
            if model.get_value(rowiter,0):
                self._com_to_delete.append(model.get_value(rowiter,4))

        self._newsstore.foreach(search_news)
        self._commentstore.foreach(search_comments)
        data = {"nws" : self._nws_to_delete, "com" : self._com_to_delete}
        del(self._nws_to_delete)
        del(self._com_to_delete)
        self.delete_entries(data)

    def toggleDeleteNewsCallback(self, renderer, path, date=None):
        rowiter = self._newsstore.get_iter(path)
        self._newsstore.set_value(rowiter, 0, not self._newsstore.get_value(rowiter,0))

    def toggleDeleteCommentCallback(self, renderer, path, data=None):
        rowiter = self._commentstore.get_iter(path)
        self._commentstore.set_value(rowiter, 0, not self._commentstore.get_value(rowiter,0))

    def getPar(self):
        return self.par

    def getApplication(self):
        return self.par.getApplication()
