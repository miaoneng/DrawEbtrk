'''
Created on Jan 6, 2013

@author: striges
'''

import arcpy
import math

class Quarter:
    """Draw a quarter"""
    
    def __init__(self, NE=-99, SE=-99, SW=-99, NW=-99):
        self.radius = (NE,SE,SW,NW)
        
    def __draw_quadrant(self,radius=-99,direction=0):
        """0 - 1st quadrant; 1 - 2nd quadrant; 2 - 3rd quadrant; 3 - 4th quadrant"""
        if radius < 0:
            return None
        ptlist = []
        for a in range(90):
            arc = (direction * 90 + a) / 180.0 * math.pi
            ptlist.append((radius * math.cos(arc), radius * math.sin(arc)))
        return ptlist 
    
    def __draw_ellipse(self):
        pass
    
    def get_geometry(self):
        self.get_pointList()
        g = arcpy.Polygon()
        pass
    
    def get_pointList(self):
        self.pointList = []
        for p in map(self.radius, range(4), self.__draw_quadrant):
            self.pointList += p
        return self.pointList