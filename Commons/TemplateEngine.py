# -*- coding: iso-8859-1 -*-

#===============================================================================
# Commons TemplateEngine module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import string


class Template:
    def __init__(self, template):
        self.start_delimiter = '<% '
        self.end_delimiter = ' %>'

        #f_in = open(template, "r")
        #self.htmlText = f_in.read()
        #f_in.close
        pass

    def set_text(self, text):
        self.text = text


    def substitute(self, **params):
        for arg in params:
            replaceString = self.start_delimiter + arg + self.end_delimiter
            self.htmlText = string.replace(self.htmlText, replaceString, params[arg])


    def writeHTML(self, fileName):
        f_out = open(fileName, "w")
        f_out.write(self.htmlText)
        f_out.close()