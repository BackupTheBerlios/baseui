from pprint import pprint

from xml.sax.handler import ContentHandler
from xml.sax import make_parser


class XMLelement(object):
    def __init__(self, tag=None, attributes=None, content=[]):
        self.tag = tag
        self.attributes = attributes
        self.content = content
        
        if self.tag == None:
            if isinstance(content, XMLelement):
                self.tag = content.tag
        
        self.level = 0
        
        self.attributes_text = ''
        if self.attributes <> None:
            self.attributes_text = self.get_attributes_text(self.attributes)
            
    
    def add_child_dict(self, child):
        self.content.append(child)


    def get_child_dict(self, tag):
        for tag_dict in self.content:
            curr_tag = tag_dict.get('tag')
            curr_content = tag_dict.get('content')
            
            #print curr_content
            if curr_tag == None:
                if type(curr_content) in [str, int]:
                    curr_tag = curr_content
                else:
                    curr_tag = curr_content.tag
                    #print 'MADE TO', curr_tag, 'EQUALS', tag
            if curr_tag == tag:
                return tag_dict


#    def set_node(self, node, tag=None, content=None, attributes=None):
#        node = self.get_node(node)
#        if tag <> None:
#            node['tag'] = tag
#        if content <> None:
#            node['content'] = content
#        if attributes <> None:
#            node['attributes'] = attributes
#        
#                
#    def get_tag_dict(self, tag):
#        #print 'TAG', tag
#        #if isinstance(tag, XMLelement):
#        #    print 'YEAH'
#        
#        for tag_dict in self.content:
#            read_tag = tag_dict.get('tag')
#            if read_tag == tag:
#                return tag_dict
#            
#            
#    def get_content(self, tag):
#        return self.get_tag_dict(tag).get('content')
#
#
#    def get_attributes(self, tag):
#        return self.get_tag_dict(tag).get('attributes')
        
        
#    def set_level(self, level):
#        self.level = level
        
        
    def get_attributes_text(self, attributes):
        text = ' '
        for key in attributes.keys():
            text += key + '="' + attributes.get(key) + '" '
        text = text[:len(text)-1]
        return text
        
        
    def spaces(self):
        s = ''
        for i in xrange(0, self.level):
            s += '  '
        return s

    
    def generate_xml(self, level=0):
        self.level = level
        text = '<%s%s>\n' % (self.tag, self.attributes_text)
        self.level += 1
        
        #print self.content
        for content_obj in self.content:
            tag = content_obj.tag
            attributes = content_obj.attributes
            content = content_obj.content
            
            #print tag, attributes, content
#            tag = tag_dict.get('tag')
#            content = tag_dict.get('content')
#            attributes = tag_dict.get('attributes')
#            comment = tag_dict.get('comment')
            
            if attributes == None:
                attributes_text = ''
            else:
                attributes_text = self.get_attributes_text(attributes)
            
            start_tag = ''
            end_tag = ''
            if content == None:
                content = ''

            if isinstance(content, XMLelement):
                content.level = self.level
                content = content.generate_xml(level=self.level)
            else:    
                start_tag = '<%s%s>' % (tag, attributes_text)
                end_tag = '</%s>' % tag
                
            text += '%s%s%s%s\n' % (self.spaces(), start_tag, content, end_tag)
        self.level -= 1
        text = text[:len(text)-1] + '\n' + '%s</%s>' % (self.spaces(), self.tag)
        return text
        
        
        
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