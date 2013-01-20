import arcpy
import xlrd

class Worker:
    
    def __init__(self,path='M:/tang/extended_track_al.xlsx'):
        self.wb = xlrd.open_workbook(path)

    


