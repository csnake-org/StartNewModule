""" Definition of the AboutTests class. """
import unittest
from about import About
import os

class AboutTests(unittest.TestCase):
    """ Tests of the About class. """
    def setUp(self):
        """ Run before test. """

    def tearDown(self):
        """ Run after test. """

    ## \test Test read and write of an about file.
    def testReadWrite(self):
        """ AboutTests: testReadWrite. """
        filename = "about_test.txt"
        # write the default about
        about = About()
        about.write(filename)
        # read it back
        about2 = About()
        about2.read(filename)
        # compare the 2 objects
        assert about == about2
        # clean up
        os.remove(filename)

if __name__ == "__main__":
    unittest.main()         