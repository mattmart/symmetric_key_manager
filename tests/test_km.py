from .context import key_manager, KeyNoExistException, KeyFormatException
import unittest
import tempfile
import os

class testKM(key_manager.KeyManager):
    """
    subclass KeyManager to get around
    the hard fast fail. Solely for testing
    instance methods.
    """
    def __init__(self,my_kfile):
        self.kfile = my_kfile

class TestKmSuite(unittest.TestCase):
    """Tests the KeyManager"""

    def test_init_fail(self):
        """
        makes sure that a keyfile not existing
        causes an error when initting a KeyManager
        """
        ntf = tempfile.NamedTemporaryFile()
        ntf.close()
        try:
            key_manager.KeyManager(ntf.name)
            assert False
        except KeyNoExistException as e:
            assert "not found" in str(e)
        except KeyFormatException as e:
            raise Exception("Key exists when it's not supposed to, check the test!")

    def test_key_mechanics_work(self):
        """
        verifies key manager hands key out when read
        from disk
        """
        key = 'this should work as expected 123'
        ntf = tempfile.NamedTemporaryFile()
        ntf.write(key)
        ntf.flush()
        km = key_manager.KeyManager(ntf.name)
        assert key == km.get_api_key()
        ntf.close()

    def test_verify_file_exist(self):
        """
        tests behavior of _verify_file_existence 
        in key_manager using overridden class for testing
        """
        ntf = tempfile.NamedTemporaryFile()
        fname = ntf.name
        km = testKM(fname)
        assert km._verify_file_exist()
        ntf.close()
        try:
            km._verify_file_exist()
            assert False
        except KeyNoExistException as e:
            assert "not found" in str(e)

    """
    next several tests test the behavior of how
    key formatting works using a crappy method to
    avoid fast fail if file doesn't exist
    """

    def test_empty_keyfile(self):
        km = testKM("doesnt matter")
        try:
            pretend_contents = []
            km._get_keyfile_from_contents(pretend_contents)
            assert False
        except KeyFormatException as e:
            assert "empty" in str(e)
    
    def test_key_long(self):
        km = testKM("doesnt matter")
        try:
            pretend_contents = ['too looooooooooooooooooooooooooooooooooong']
            km._get_keyfile_from_contents(pretend_contents)
            assert False
        except KeyFormatException as e:
            assert "long" in str(e)

    def test_key_short(self):
        km = testKM("doesnt matter")
        try:
            pretend_contents = ['too short']
            km._get_keyfile_from_contents(pretend_contents)
            assert False
        except KeyFormatException as e:
            assert "short" in str(e)

    def test_key_multi_line(self):
        km = testKM("doesnt matter")
        try:
            pretend_contents = ['one', 'two']
            km._get_keyfile_from_contents(pretend_contents)
            assert False
        except KeyFormatException as e:
            assert "more than one" in str(e)

    def test_key_works(self):
        km = testKM("doesnt matter")
        try:
            winning_key = 'this should work as expected 123'
            pretend_contents = [ winning_key ]
            assert winning_key == km._get_keyfile_from_contents(pretend_contents)
        except KeyFormatException as e:
            print("")
            print("this key should have worked, but instead we got the following error:")
            print(e)
            assert False

        

        
if __name__ == '__main__':
    unittest.main()
