# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI misc.DOM module
# by Mark Muzenhardt, published under LGPL-License.
#===============================================================================

import os
import xml.dom.minidom


class XmlBase(object):
    def __init__(self):
        self._filepath = None
        self._dom = None
        
        
    # Common file functions ----------------------------------------------------
    def delete(self):
        os.remove(self._filepath)
        self._filepath = None
        
        
    def load(self, filepath):
        self._filepath = filepath
        file_object = open(filepath, 'rb')
        self._xml_text = file_object.read()
        file_object.close()
        self._dom = xml.dom.minidom.parseString(self._xml_text)
        
    
    def save(self):
        self.save_as(self._filepath)
            
            
    def save_as(self, filepath):
        self._filepath = filepath
        self._xml_text = self._dom.toxml()
        file_object = open(filepath, 'wb')
        file_object.write(self._xml_text)
        file_object.close()
        
        
    # Common parse functions ---------------------------------------------------
    def get_value(self, element):
        value = None
        if element.firstChild <> None:
            value = element.firstChild.data
        return value
        
        
    def set_value(self, element, value):
        element.childNodes[0].nodeValue = value
    
    
    def get_first_element(self, parent_element, tag_name):
        child_elements = parent_element.getElementsByTagName(tag_name)
        if child_elements == []:
            return
        first_element = child_elements[0]
        return first_element
        
        
    def get_first_element_value(self, parent_element, tag_name):
        first_element = self.get_first_element(parent_element, tag_name)
        if first_element == None:
            return
        return self.get_value(first_element)
    
    
    def add_child(self, parent_element, tag_name, attributes={}, text=None):
        this_element = self._dom.createElement(tag_name)
        for key in attributes.keys():
            this_element.setAttribute(key, attributes[key])
        parent_element.appendChild(this_element)
        
        if text <> None:
            text_node = self._dom.createTextNode(text)
            this_element.appendChild(text_node)
        return this_element



