'''
Created on Oct 8, 2013

@author: striges
'''

import shapefile
import csv
import sys
import os
from Hurricane import Hurricane
from DrawQuarter import Quarter

from pprint import pprint as pp

#Configurations
ProjStr='+proj=lcc +lat_1=33 +lat_2=45 +lat_0=39 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs'
Interp=6.0
Draw=64 #Could be 64, 50 or 34. Otherwise, print all result to console
Path=r'extended_track_hurricane_only.csv'

class Worker:

    def __init__(self, path=Path):
        """
        :param self: Worker.Worker
        :param path: str
        """
        #file descriptor of source csv
        self.datasource = path
        self.fd = open(path, 'rU')
        #Initialize two shapefile writers: Center and Area
        self.ptwriter = shapefile.Writer(shapefile.POINT)
        self.ploywriter = shapefile.Writer(shapefile.POLYGON)
        self.ploywriter.autoBalance = True
        #Hurricane set
        self.hurricanes = []

    def processRecords(self, records, name, hurricane_id):
        """
        :param records: list,
        :return: Hurricane, interpolated
        """
        h = Hurricane(hurricane_id, name, records)
        proj_h = h.project(ProjStr)
        interp_h = proj_h.interpolate(Interp)
        return interp_h

    def read(self, verbose=False):
        """
        :param self: Worker.Worker
        :param verbose: boolean
        """
        getOrElse = lambda p,q: float(p[q]) * 1825 if p.has_key(q) else 0.0;
        csvdict = csv.DictReader(self.fd)
        #Let's store everything on memory
        alldata = [d for d in csvdict]
        if verbose: pp(alldata)
        else: pp(len(alldata))
        last_id = None
        hrecords = []
        name = None
        hurricane_id = None
        for entry in alldata:
            if entry['Storm identification number'] != last_id and last_id != None:
                self.hurricanes.append(self.processRecords(hrecords, name, hurricane_id))
                hrecords = []
            hurricane_id = entry['Storm identification number']
            name = entry['storm name']
            hrecords.append((entry['year'] + entry['MMDDHH'].rjust(6,'0')[0:4], float(entry['MMDDHH'][-2:]),
                            -float(entry['longitude (deg W)']), float(entry['latitude (deg N)']),
                            getOrElse(entry, 'NE(34)'), getOrElse(entry,'NW(34)'), getOrElse(entry,'SE(34)',), getOrElse(entry,'SW(34)'),  #34knots
                            getOrElse(entry, 'NE(50)'), getOrElse(entry,'NW(50)'), getOrElse(entry,'SE(50)',), getOrElse(entry,'SW(50)'),  #50knots
                            getOrElse(entry, 'NE(64)'), getOrElse(entry,'NW(64)'), getOrElse(entry,'SE(64)',), getOrElse(entry,'SW(64)')
                            ))
            last_id = entry['Storm identification number']
        self.draw(Draw)

    def draw(self, Draw):
        """
        :param self: Worker.Worker
        :param Draw: int
        """
        if not Draw in (64, 50, 34):
            pp(self.hurricanes)
            return
        self.ploywriter.field('ID')
        self.ploywriter.field('NAME')
        self.ploywriter.field('YYYYMMDD','C','10')
        self.ploywriter.field('HOURS','N')
        self.ploywriter.field('NE','N')
        self.ploywriter.field('NW','N')
        self.ploywriter.field('SE','N')
        self.ploywriter.field('SW','N')

        for h in self.hurricanes:
            for record in h.Records:
                #Get shape information
                center = (record['lon'],record['lat'])
                q = Quarter([record["kt%d-%d" % (Draw, i)] for i in [1,2,3,4]], center)
                pointList = q.get_pointList()
                self.ploywriter.poly(parts=[pointList])
                self.ploywriter.record(h.Id,h.Name,record['date'],record['hours'],
                                       record['kt%d-1' % Draw], record['kt%d-2' % Draw], record['kt%d-3' % Draw], record['kt%d-4' % Draw])


    def close(self):
        """
        :param self: Worker.Worker
        """
        #Write out shapefile
        #self.ptwriter.save("extended_track_hurricane_only_center")
        del self.ptwriter
        self.ploywriter.save("extended_track_hurricane_only_area")
        #Close input source
        self.fd.close()

if __name__ == "__main__":
    p = Worker()
    p.read()
    p.close()
