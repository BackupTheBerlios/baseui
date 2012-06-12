# -*- coding: iso-8859-1 -*-

from pprint import pprint

#from xml.sax.handler import ContentHandler
#from xml.sax import make_parser


class XMLelement(object):
    def __init__(self, tag=None, attributes=None, content=''):
        self.tag = tag
        self.attributes = attributes
        self.content = content
        self._intend_level = 0
        
        if isinstance(content, XMLelement):
            # If the content is an instance of an XMLelement, get tag, content 
            # and attributes from that object below.
            self.tag = content.tag
            self.attributes = content.attributes
            
            
    def get_child(self, tag=None):
        for child_obj in self.content:
            if tag == child_obj.tag:
                return child_obj
            
            
    def get_child_tags(self):
        tag_list = []
        for child_obj in self.content:
            tag_list.append(child_obj.tag)
        return tag_list
        
        
    def _attributes_to_str(self, attributes):
        if attributes == None:
            return ''
        
        text = ' '
        for key in attributes.keys():
            text += key + '="' + str(attributes.get(key)) + '" '
        text = text[:len(text)-1]
        return text
        
        
    def _intend(self):
        s = ''
        for i in xrange(0, self._intend_level):
            s += '  '
        return s
        
        
    def read_xml(self, text, depth=0):
        print text, self.tag
        
        
    def generate_xml(self, level=0, depth=0, header=False):
        ''' Generates pretty xml for this object and all subobjects. The ``level``
            tells, which intendation level is needed, ``depth`` stands for the
            depth of the xml-tree-scan, where 0 stands für infinite. If ``header``
            is true, the xml standard-header will be on top of the xml output. '''
        
        text = ''
        if level == 0 and header == True:
            text += '<?xml version="1.0" encoding="utf-8"?>\n'
            
        self._intend_level = level
        text += '<%s%s>\n' % (self.tag, self._attributes_to_str(self.attributes))
        self._intend_level += 1
        nointend = False
        if type(self.content) == list:
            # Content can be a list.
            for element in self.content:
                tag = element.tag
                attributes = element.attributes
                content = element.content
                
                text += '%s<%s%s>\n' % (self._intend(), tag, self._attributes_to_str(attributes))
                if type(content) == list:
                    self._intend_level += 1
                    for element in content:
                        text += '%s%s' % (self._intend(), element.generate_xml(level=self._intend_level)) + '\n'
                    self._intend_level -= 1
                    text += self._intend()
                else:
                    text = text[:len(text)-1] + '%s' % content
                text += '</%s>\n' % tag
        else:
            # Content can be a value.
            text = text[:len(text)-1] + '%s' % self.content
            nointend = True
        
        # Close the Tag at the end.
        if nointend == True:
            text += '</%s>' % self.tag
            nointend = False
        else:
            self._intend_level -= 1
            text += '%s</%s>' % (self._intend(), self.tag)
        return text

        
        
        
#class XML_to_dict(ContentHandler):    
#    def __init__(self):
#        self.end_tag = False
#
#
#    def startDocument(self):
#        self.dict_str = ""
#
#
#    def endDocument(self):
#        self.dict_str = self.dict_str[0:len(self.dict_str)-1]
#        self.dict_str += '}'
#        self.dict = eval(self.dict_str)
#        
#
#    def startElement(self, name, attrs):
#        self.name = name
#        if self.end_tag:
#            self.end_tag = False
#            self.dict_str += "'%s':" % name
#        else:
#            self.dict_str += "{'%s':" % name
#        
#        
#    def endElement(self, name):
#        if name == self.name:
#            if self.dict_str[len(self.dict_str)-1:len(self.dict_str)] == ":":
#                self.dict_str += "''"
#            self.dict_str += ","
#            self.end_tag = True
#        else:
#            self.dict_str = self.dict_str[0:len(self.dict_str)-1]
#            self.dict_str += "},"
#        print 'end:', name
#
#    
#    def characters(self, content):
#        content = content.replace('\t', '').replace('\n', '')
#        if content <> '':
#            self.dict_str += "'%s'" % content
#            print 'content:', content,



if __name__ == '__main__':
    raw_input('give <RETURN> to exit...')

    #order = XML_to_dict()
    #saxparser = make_parser()
    #saxparser.setContentHandler(order)
    
    #datasource = open("xml/order_7845.xml","r")
    #saxparser.parse(datasource)
    
    #pprint(order.dict)
    #print order.dict_str
   
    
    