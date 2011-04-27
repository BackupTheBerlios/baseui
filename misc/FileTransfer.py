# -*- coding: iso-8859-1 -*-

#===============================================================================
# FTP module.
# by Mark Muzenhardt, published under LGPL-License.
#===============================================================================

import ftplib, re, time, posixpath

from datetime import datetime


class FTP:
    def __init__(self, debug=False):
        self.debug = debug
        
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
        if self.connection <> None:
            self.connection.quit()
        else:
            if self.debug:
                print "Could not close connection because there is none opened!"


    def get_filenames(self, top):
        self.connection.cwd(top)
        raw_list = self.listdir()
        
        file_list = []
        for tuple in raw_list[1]:
            file_list.append(tuple[0])
        return file_list
    
    
    def listdir(self):
        """
        List the contents of the FTP opbject's cwd and return two tuples of
    
           (filename, size, mtime, mode, link)
    
        one for subdirectories, and one for non-directories (normal files and other
        stuff).  If the path is a symbolic link, 'link' is set to the target of the
        link (note that both files and directories can be symbolic links).
    
        Note: we only parse Linux/UNIX style listings; this could easily be
        extended.
        """
        
        _calmonths = dict((x, i+1) 
            for i, x in enumerate(
                ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                )
            )
        )

        dirs, nondirs = [], []
        listing = []
        self.connection.retrlines('LIST', listing.append)
        for line in listing:
            # Parse, assuming a UNIX listing
            words = line.split(None, 8)
            if len(words) < 6:
                print >> sys.stderr, 'Warning: Error reading short line', line
                continue
    
            # Get the filename.
            filename = words[-1].lstrip()
            if filename in ('.', '..'):
                continue
    
            # Get the link target, if the file is a symlink.
            extra = None
            i = filename.find(" -> ")
            if i >= 0:
                # words[0] had better start with 'l'...
                extra = filename[i+4:]
                filename = filename[:i]
    
            # Get the file size.
            size = int(words[4])
    
            # Get the date.
            year = datetime.today().year
            month = _calmonths[words[5]]
            day = int(words[6])
            mo = re.match('(\d+):(\d+)', words[7])
            if mo:
                hour, min = map(int, mo.groups())
            else:
                mo = re.match('(\d\d\d\d)', words[7])
                if mo:
                    year = int(mo.group(1))
                    hour, min = 0, 0
                else:
                    raise ValueError("Could not parse time/year in line: '%s'" % line)
            dt = datetime(year, month, day, hour, min)
            mtime = time.mktime(dt.timetuple())
    
            # Get the type and mode.
            mode = words[0]
    
            entry = (filename, size, mtime, mode, extra)
            if mode[0] == 'd':
                dirs.append(entry)
            else:
                nondirs.append(entry)
        return dirs, nondirs
    
    
    def walk(self, top, topdown=True, onerror=None):
        """
        Generator that yields tuples of (root, dirs, nondirs).
        """
        # Make the FTP object's current directory to the top dir.
        try:
            self.connection.cwd(top)
            print 'walking top:', top
        except:
            raise
        
        try:
            dirs, nondirs = self.listdir()
        except os.error, err:
            if onerror is not None:
                onerror(err)
            return
    
        if topdown:
            yield top, dirs, nondirs
        for entry in dirs:
            dname = entry[0]
            path = posixpath.join(top, dname)
            if entry[-1] is None: # not a link
                for x in self.walk(path, topdown, onerror):
                    yield x
        if not topdown:
            yield top, dirs, nondirs
    
        
    def download(self, ftp_filepath, local_filepath):
        ftp_command = 'RETR %s' % ftp_filepath
        if self.debug:
            print ftp_command
        
        try:
            file_object = open(local_filepath, 'wb')
            self.connection.retrbinary(ftp_command, file_object.write)
            file_object.close()
        except:
            raise
        return
        
    
    def upload(self, local_filepath, ftp_filepath):
        ftp_command = 'STOR %s' % ftp_filepath
        if self.debug:
            print ftp_command
            
        try:                
            file_object = open(local_filepath, 'rb')
            self.connection.storbinary(ftp_command, file_object)
            file_object.close()
        except:
            raise
        return


