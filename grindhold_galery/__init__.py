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

from skarphedcore.module import AbstractModule

class ModuleException(Exception): 
    ERRORS = {
        0:"""This instance does not have a WidgetId. Therefore, Widget-bound methods cannot be used"""
    }

    @classmethod
    def get_msg(cls,nr, info=""):
        return "DB_"+str(nr)+": "+cls.ERRORS[nr]+" "+info

class Module(AbstractModule):
    def __init__(self, core):
        AbstractModule.__init__(self,core)
        self._path = os.path.dirname(__file__)
        self._load_manifest()

    def upload_image(self, widget_id, galery_id, image):
        """
        called to upload an image to the galery identified
        by galery_id
        """
        pass

    def get_galery(self, widget_id, galery_id):
        """
        returns the requested galery
        """
        pass

    def get_thumbnail(self, widget_id, image_id):
        """
        returns the thumbnail of the image with the requested id
        """
        pass

    def create_galery(self, widget_id, galery_name):
        """
        creates a new galery
        """
        pass

    def set_image_info(self, widget_id, image_id, title, description):
        """
        sets the info according to the image identified
        by image_id
        """
        pass

    def set_galery_info(self, widget_id, galery_id, title, description):
        """
        sets the  title and description of the galery identified
        by galery_id
        """
        pass

    def render_pure_html(self, widget_id, args={}):
        pass

    def render_html(self, widget_id, args={}):
        pass

    def render_javascript(self, widget_id, args={}):
        pass
