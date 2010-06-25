from pprint import pprint

from xml.sax.handler import ContentHandler
from xml.sax import make_parser



class XML_to_dict(ContentHandler):    
    def __init__(self):
        self.end_tag = False
        
    def startDocument(self):
        self.dict_str = ""
        
    def endDocument(self):
        self.dict_str = self.dict_str[0:len(self.dict_str)-1]
        self.dict_str += '}'
        self.dict = eval(self.dict_str)
        pass
        
    def startElement(self, name, attrs):
        self.name = name
        if self.end_tag:
            self.end_tag = False
            self.dict_str += "'%s':" % name
        else:
            self.dict_str += "{'%s':" % name
        
    def endElement(self, name):
        if name == self.name:
            if self.dict_str[len(self.dict_str)-1:len(self.dict_str)] == ":":
                self.dict_str += "''"
            self.dict_str += ","
            self.end_tag = True
        else:
            self.dict_str = self.dict_str[0:len(self.dict_str)-1]
            self.dict_str += "},"
        print 'end:', name
    
    def characters(self, content):
        content = content.replace('\t', '').replace('\n', '')
        if content <> '':
            self.dict_str += "'%s'" % content
            print 'content:', content,

    
order = XML_to_dict()
saxparser = make_parser()
saxparser.setContentHandler(order)

datasource = open("xml/order_7845.xml","r")
saxparser.parse(datasource)

pprint(order.dict)
#print order.dict_str