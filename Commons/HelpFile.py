# -*- coding: iso-8859-1 -*-

#===============================================================================
# Commons HelpFile module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import os
import webbrowser


class HTML:
    def show(self, helpfile=''):
        docpath = os.getcwd() + '/doc'

        if os.path.exists(docpath + '/build'):
            docpath += '/build'
        if os.path.exists(docpath + '/htmlhelp'):
            docpath += '/htmlhelp'

        urlbase = 'file:///%s' % docpath

        try:
            webbrowser.open(url='%s/%s' % (urlbase, helpfile), autoraise=1)
        except Exception, inst:
            raise
        return


