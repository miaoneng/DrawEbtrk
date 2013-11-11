'''
Created on Jan 10, 2013

@author: striges
'''
import unittest

class MainTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_worker(self):
        import Worker
        p = Worker.Worker()
        p.read()
        return True
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()