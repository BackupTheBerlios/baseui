import os, sys
sys.path.append("..")

import md5
from misc import Windows


class KeyDrive(object):
    def __init__(self, drive_letter, filepath='key'):
        self.drive_letter = drive_letter
        self.filepath = os.path.join(self.drive_letter + '\\', filepath)
        
    
    def create(self, salt):
        try:
            key_file = open(self.filepath, 'w')
            key_file.write(self.hash_drive_serial(salt))
            key_file.close()
        except:
            raise
            
        
    def verify(self, salt):
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
            
        
    def hash_drive_serial(self, salt):
        vol_hash = md5.new()
        vol_serial = Windows.get_volume_serial(self.drive_letter)
        vol_hash.update(vol_serial + salt)
        return vol_hash.hexdigest()
        
    
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
    
# drive_letter = raw_input('drive letter > ')
# salt = raw_input('salt > ')

# vol_hash = md5.new()
# vol_serial = Windows.get_volume_serial(drive_letter)
# vol_hash.update(vol_serial + salt)
# hash_hex = vol_hash.hexdigest()
# print vol_serial, hash_hex

# key_file_path = os.path.join(drive_letter, '\keyfile')
# print 'keyfile_path:', key_file_path
# key_file = open(key_file_path, 'r')
# saved_hash = key_file.read()
# key_file.close()

# print 'saved_hash:', saved_hash
# print
# if hash_hex == saved_hash:
    # print 'valid license'
# else:
    # print 'INVALID LICENSE!'
    
# raw_input('give <RETURN> to exit...')
#data = os.popen('vol '+'c:', 'r').read()
#data = data.split()
#print data[len(data)-1:]
