import sys, os, math

import proj
import shapefile
import pyproj

#WRF-LCC Projection
projecter = pyproj.Proj('+proj=lcc +lat_1=33 +lat_2=45 +lat_0=40 +lon_0=-97 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs')

class LocationClass:
    """Represents a location for one record"""
    def __init__(self, lon, lat):
        self.geo = (lon, lat)
        self.proj = projecter(lon, lat)
        
    def __str__(self):
        return "<Lon: %f, Lat: %f>" % self.geo
class AttributesClass:
    """Represents an attribute class for one record"""
    def __init__(self, mws, mcp, rmw, eye, poci, roci, kt34, kt50, kt64, typecode, distance):
        self.mws = mws
        self.mcp = mcp
        self.rmw = rmw
        self.eye = eye
        self.poci = poci
        self.roci = roci
        self.kt34 = kt34
        self.kt50 = kt50
        self.kt64 = kt64
        self.typecode = typecode
        self.distance = distance

class Hurricane:
    """Represents a hurricane structure"""
        
    def __init__(self, Id, Name):
        self.Id = Id
        self.Name = Name     
        self.Dictionary = {'mws': 'maximum wind speed',
                           'mcp': 'minimum central pressure',
                           'rmw': 'radius of maximum windspeed',
                           'eye': 'eyediameter',
                           'poci': 'pressure of outer closed isobar',
                           'roci': 'radius of outer closed isobar',
                           'kt34': 'radii (nm) of 34 kt wind to the NE SE SW and NW',
                           'kt50': 'radii (nm) of 50 kt wind to the NE SE SW and NW',
                           'kt64': 'radii (nm) of 64 kt wind to the NE SE SW and NW',
                           'typecode': 'storm code',
                           'distance': 'distance to landmass'}
        self.Locations = {}    
        self.Attributes = {}
        self.RecordsCount = 0        
        
    def add_record(self, time, lat, lon, mws, mcp, rmw, eye, poci, roci, kt34, kt50, kt64, typecode, distance):
        """Add a record to hurricane"""        
        self.Locations[time] = LocationClass(lon, lat)
        self.Attributes[time] = AttributesClass(mws, mcp, rmw, eye, poci, roci, kt34, kt50, kt64, typecode, distance)

class Worker:
    
    def __init__(self,path=r'C:\Users\sugar\Documents\Research\ExtendedTrack\ebtrk_atlc.txt'):
        self.datasource = path    
        #Initialize two shapefile writers
        self.ptwriter = shapefile.Writer(shapefile.POINT)
        self.ploywriter = shapefile.Writer(shapefile.POLYGON)
        
    def 

