'''
Created on Jan 6, 2013

@author: striges
'''

import math
import numpy as np

class Quarter:
    """Draw a quarter"""

    def __init__(self, radius, center):
        """self.radius = [NE,SE,SW,NW]"""
        self.X, self.Y = center
        self.radius = radius

    def __draw_quadrant(self,radius,direction):
        """
        :param radius: the raidus that we draw quarters
        :type radius: float
        :param radius
        """
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

