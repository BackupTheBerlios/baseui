# -*- coding: iso-8859-1 -*-

#===============================================================================
# FTP module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import ftplib 


class FTP:
    def __init__(self):
        self.hostname = ''
        self.username = ''
        self.password = ''
        self.connection = None
        
        
    def connect(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        
        try:
            self.connection = ftplib.FTP(self.hostname)
            self.connection.login(self.username, self.password)
            print self.connection.getwelcome()
        except:
            raise
            
        return self.connection
        
        
    def close(self):
        self.connection.quit()
        

