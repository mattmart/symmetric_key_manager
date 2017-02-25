import os.path

class KeyInitException(Exception):
    """
    Signifies there was an error with initializing the key
    Right now, prolly just means the file ain't there
    """
    pass

class KeyManager:
    def __init__(self,kfile):
        self.import_key(kfile)
    
    def import_key(self,kfile):
        """
        should *always* be called to set up the key
        if you want your module to fast fail via exception,
        call this immediately upon startup.
        """
        self._verify_file_existence(kfile)
        self.key = self._get_api_key_from_file(kfile)

    def get_api_key(self):
        return self.key

    def _get_api_key_from_file(self,kfile):
        """
        gets the api key from disk, strips all whitespace,
        and returns it
        """
        self._verify_file_existence(kfile)
        key_file = open(kfile,'r')
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
            raise KeyInitException("Key file was empty!")
        if num_lines > 1:
            raise KeyInitException("Key file had more than one line!")
        
        key = kf_contents[0].strip()
        key_length = len(key)
        if key_length < 32:
            raise KeyInitException("Key was not appropriate length - too short!")
        if key_length > 32:
            raise KeyInitException("Key was not appropriate length - too long!")
        return key
        
    def _verify_file_existence(self, kfile):
        """
        verifies that the keyfile exists  before we fetch it
        """
        if os.path.exists(kfile):
            pass
        else:
            raise KeyInitException("Key file: " + kfile + " was not found on disk!")
