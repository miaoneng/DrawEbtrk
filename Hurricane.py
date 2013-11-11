import sys, os, math

import shapefile
import pyproj
import numpy
import copy
import datetime

class Hurricane:
    """Represents a hurricane structure"""

    fieldDef=[('date','a8'),('hours','<f4'),
            ('lon','<f4'), ('lat','<f4'),
            ('kt34-1','f4'), ('kt34-2','f4'), ('kt34-3','f4'), ('kt34-4','f4'),
            ('kt50-1','f4'), ('kt50-2','f4'), ('kt50-3','f4'), ('kt50-4','f4'),
            ('kt64-1','f4'), ('kt64-2','f4'), ('kt64-3','f4'), ('kt64-4','f4'),
            ]

    def __init__(self, Id, Name, Records):
        """
        :param Id: str
        :param Name: str
        :param Records: list(tuple,tuple,tuple,...,tuple), each tuple contains hurricane information at one time
        """
        self.Id = Id
        self.Name = Name
        self.Records = numpy.array(Records, dtype=Hurricane.fieldDef)
        self.isProjected = False

    def appendRecord(self, Record):
        """
        Append one line to current hurricane record
        :param Record: tuple, tuple contains hurricane information at one time
        """
        self.Records = numpy.append(self.Records, numpy.array(Record, dtype=Hurricane.fieldDef))

    def project(self, ProjStr='+proj=lcc +lat_1=33 +lat_2=45 +lat_0=39 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs'):
        """
        Project current hurricane to specified coordiate system
        :param ProjStr: str, proj4 definition as string
        :return: Hurricane.Hurricane, Hurricane projected from (lon,lat) to (x,y) defined by ProjStr
        """
        projected = copy.deepcopy(self)
        assert isinstance(projected, Hurricane)
        projected.isProjected = True
        proj = pyproj.Proj(ProjStr)
        for p in projected.Records:
            p['lon'],p['lat'] = proj(p['lon'],p['lat'])
        return projected

    def interpolate(self, hours=1.0):
        """
        Interpolate current hurricane to high temporal resolution.
        :param hours: float, temporal resolution to interploate.
        :return: Hurricane.Hurriance, Interpolated hurricane instance
        """
        if not self.isProjected:
            raise Exception("Hurricane is not projected. You must project it before interpolation!")
        #we know that our original temporal reslution is 6hr.
        xp = numpy.array([6.0 * p for p in range(self.Records.shape[0])])[:]
        x = numpy.arange(0, numpy.max(xp), hours)[:]
        if not xp.max() == x.max(): x = numpy.append(x, xp.max())
        interp_hurricane = copy.deepcopy(self)
        interpolated = numpy.ndarray((len(x),), dtype=Hurricane.fieldDef)
        #Special handling of date and hours
        start_date = datetime.datetime.strptime(self.Records[0][0], '%Y%m%d')
        start_hour = self.Records[0][1]
        start_time = start_date + datetime.timedelta(hours=float(start_hour))
        for i in range(len(interpolated)):
            current_time = start_time + datetime.timedelta(hours=float(x[i]))
            interpolated[i]['date'] = current_time.strftime('%Y%m%d')
            interpolated[i]['hours'] = current_time.hour + current_time.minute / 60.0 + current_time.second / 3600.0
        #Interpolated rest field by field
        for i in range(2,len(Hurricane.fieldDef)):
            fp = self.Records[Hurricane.fieldDef[i][0]]
            #Special case, if all values are -99 -> unknown, we have no way to set all of them to 0
            if numpy.all(fp == -99):
                f = numpy.zeros_like(x)
            else:
                f = numpy.interp(x, xp[fp != -99], fp[fp != -99])
            interpolated[Hurricane.fieldDef[i][0]] = f
        interp_hurricane.Records = interpolated
        return interp_hurricane






