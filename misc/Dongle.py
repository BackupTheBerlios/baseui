import os, sys
sys.path.append("..")

import md5
import Windows


class KeyDrive(object):
    def __init__(self, path, filename='key'):
        self.path = path
        self.filepath = os.path.join(path, filename)
        
    
    def create(self, salt=''):
        try:
            key_file = open(self.filepath, 'w')
            key_file.write(self.hash_drive_serial(salt))
            key_file.close()
        except:
            raise
            
        
    def verify(self, salt=''):
        try:
            key_file = open(self.filepath, 'r')
            saved_hash = key_file.read()
            key_file.close()
        except:
            raise
            return
            
        drive_hash = self.hash_drive_serial(salt)
        if drive_hash == saved_hash:
            return True
        return False
            
        
    def hash_drive_serial(self, salt=''):
        vol_hash = md5.new()
        vol_serial = Windows.get_volume_serial(self.path[:2])
        vol_hash.update(vol_serial + salt)
        return vol_hash.hexdigest()
        
        
    def get_drive_serial(self):
        return Windows.get_volume_serial(self.path[:2])
        
        
    
if __name__ == "__main__":
    drive_letter = raw_input('drive letter > ')
    salt = raw_input('salt > ')
    rewr = raw_input('(r)ead or (w)rite? > ')
        
    cls = KeyDrive(drive_letter)
    if rewr == 'w':
        cls.create(salt)
    else:
        print 'Valid?', cls.verify(salt)
        
    raw_input('give <RETURN> to exit...')

    
    
    