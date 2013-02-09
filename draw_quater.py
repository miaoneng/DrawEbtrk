'''
Created on Jan 6, 2013

@author: striges
'''

import math

class Quarter:
    """Draw a quarter"""
    
    def __init__(self, NE=-99, SE=-99, SW=-99, NW=-99, Center=(0,0), Fill_Missing=False):
        self.radius = (NE,SE,SW,NW)          
        self.X, self.Y = Center
        
    def __draw_quadrant(self,radius=-99,direction=0):
        """0 - 1st quadrant; 1 - 2nd quadrant; 2 - 3rd quadrant; 3 - 4th quadrant"""
        if radius < 0:
            return None
        ptlist = []
        for a in range(91):
            arc = (direction * 90 + a) / 180.0 * math.pi
            ptlist.append([radius * math.cos(arc) + self.X, radius * math.sin(arc) + self.Y])
        return ptlist 
       
    def get_pointList(self):
        self.pointList = []
        for p in map(self.__draw_quadrant, self.radius, range(4)):
            self.pointList += p
        self.pointList.append(self.pointList[0])
        return self.pointList