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

    def passed_test_read(self):
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
        import os
        homedir = os.environ['USERPROFILE']
        import draw_quater
        d = draw_quater.Quarter(100,50,25,12.5,(0,0))
        from pprint import pprint as pp        
        pp(d.get_pointList())
        import shapefile
        w = shapefile.Writer(shapefile.POLYGON)
        w.autoBalance = 1
        w.poly(parts=[d.get_pointList()])
        w.field('FIRST_FLD', 'C', '40')
        w.record('3', 'Polygon')
        w.save(homedir + '/test')
        return True

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()