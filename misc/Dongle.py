import os, sys, md5, time
import Windows


class KeyDrive(object):
    def __init__(self, path, filename='key'):
        self.path = path
        self.filepath = os.path.join(path, filename)
        
    
    def create(self, salt=''):
        try:
            key_file = open(self.filepath, 'w')        
            timestamp = self.get_timestamp()
            key_file.write(self.hash_drive_serial(salt)) # + timestamp))
            key_file.close()
        except:
            raise
            
        
    def verify(self, salt=''):
        try:
            saved_hash = self.get_saved_hash()
        except:
            raise
            return
            
        drive_hash = self.hash_drive_serial(salt) # + timestamp)
        if drive_hash == saved_hash:
            return True
        return False
            
        
    def get_saved_hash(self):
        try:
            key_file = open(self.filepath, 'r')
            saved_hash = key_file.readline().replace('\n', '')
            key_file.close()
        except:
            raise
            return
        return saved_hash
        
        
    def set_text(self, text):
        hash = self.get_saved_hash()
        key_file = open(self.filepath, 'w')
        new_content = hash + '\n\n' + text
        key_file.write(new_content)
        key_file.close()
        
        
    def get_text(self):
        key_file = open(self.filepath, 'r')
        key_file.readline()
        key_file.readline()
        text = key_file.read()
        key_file.close()
        return text
        
        
    def hash_drive_serial(self, salt=''):
        vol_hash = md5.new()
        vol_serial = Windows.get_volume_serial(self.path[:2])
        vol_hash.update(vol_serial + salt)
        return vol_hash.hexdigest()
        
        
    def get_drive_serial(self):
        return Windows.get_volume_serial(self.path[:2])
        
        
    def get_timestamp(self):
        sec_stamp=time.localtime(os.path.getctime(self.filepath))
        return time.strftime('%Y-%m-%d %H:%M:%S', sec_stamp)
        
        
        
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

    
    
    