import os.path

class KeyInitException(Exception):
    """
    Signifies there was an error with initializing the key
    Right now, prolly just means the file ain't there
    """
    pass

class KeyNoExistException(KeyInitException):
    pass

class KeyFormatException(KeyInitException):
    pass

class KeyManager:
    def __init__(self,my_kfile):
        self.kfile = my_kfile
        self.import_key()
    
    def import_key(self):
        """
        should *always* be called to set up the key
        if you want your module to fast fail via exception,
        call this immediately upon startup.
        """
        self._verify_file_exist()
        self.key = self._get_api_key_from_file()

    def get_api_key(self):
        return self.key

    def _get_api_key_from_file(self):
        """
        gets the api key from disk, strips all whitespace,
        and returns it
        """
        self._verify_file_exist()
        key_file = open(self.kfile,'r')
        kf_contents = key_file.readlines()
        key = self._get_keyfile_from_contents(kf_contents)
        return key

    def _get_keyfile_from_contents(self,kf_contents):
        """
        verifies everything we wanna know about a keyfile
        before we start using it. Throws exception if not
        so we can fail init. returns key after everything 
        looks good
        """
        num_lines = len(kf_contents)
        if num_lines == 0:
            raise KeyFormatException("Key file was empty!")
        if num_lines > 1:
            raise KeyFormatException("Key file had more than one line!")
        
        key = kf_contents[0].strip()
        key_length = len(key)
        if key_length < 32:
            raise KeyFormatException("Key was not appropriate length - too short!")
        if key_length > 32:
            raise KeyFormatException("Key was not appropriate length - too long!")
        return key
        
    def _verify_file_exist(self):
        """
        verifies that the keyfile exists  before we fetch it
        """
        if not os.path.exists(self.kfile):
            raise KeyNoExistException("Key file: " + self.kfile + " was not found on disk!")
        return True
