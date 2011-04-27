# -*- coding: iso-8859-1 -*-

#===============================================================================
# GTKapi Buttons module.
# by Mark Muzenhardt, published under LGPL-License.
#===============================================================================

import os
import gtk

PATH = os.path.dirname(__file__)


class Base:
    def __init__(self, widget):
        self.widget = widget
        
        
    def initialize(self, image_path=None, stock_image=None, label_text=None, width=-1, height=-1):
        hbox = gtk.HBox()
        image = gtk.Image()
        if image_path <> None:
            image.set_from_file(image_path)
            hbox.pack_start(image)
        if stock_image <> None:
            image.set_from_stock(stock_image, gtk.ICON_SIZE_BUTTON)
            hbox.pack_start(image)

        if label_text <> None:
            label = gtk.Label(label_text)
            label.set_padding(4, 0)
            label.set_use_underline(True)
            hbox.pack_start(label)
        self.widget.add(hbox)
        self.widget.set_size_request(width=width, height=height)
        
        
        
class Simple(Base):
    def __init__(self, widget=None):
        Base.__init__(self, widget)


    def create(self, image_path=None, stock_image=None, label_text=None, width=-1, height=-1):
        self.widget = gtk.Button()
        self.initialize(image_path, stock_image, label_text, width, height)
        return self.widget



class Toggle(Base):
    # Shut that bullshit off and delete the whole class for unification to Simple!
    def __init__(self, widget=None):
        Base.__init__(self, widget)


    def create(self, image_path=None, stock_image=None, label_text=None, width=-1, height=-1):
        self.widget = gtk.ToggleButton()
        self.initialize(image_path, stock_image, label_text, width, height)
        return self.widget

        