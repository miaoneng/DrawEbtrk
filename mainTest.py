'''
Created on Jan 10, 2013

@author: striges
'''
import unittest


class TestMain(unittest.TestCase):

    def setUp(self):

        pass

    def tearDown(self):
        pass

    def test_read(self):
        import main
        self.Worker = main.Worker()
        self.wb = self.Worker.wb
        for s in self.wb.sheets():
            print 'Sheet:',s.name
            for row in range(s.nrows):
                values = []
                for col in range(s.ncols):
                    values.append(str(s.cell(row,col).value))
        return True
    
    def test_quadrant(self):
        from draw_utils import draw_quater
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()