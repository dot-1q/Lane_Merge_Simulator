import csv
import os

class Route:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.load_coords()
        self.precision = len(self.coords)

    def get_position(self):
        return self.coords[self.position]

    def next_coord(self,speed):
        self.position = (self.position + 1)%self.precision
        return self.coords[self.position]

    def prev_coord(self):
        pass

    def set_position(self):
        pass

    def load_coords(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir,'coordinates',self.name+'.csv')
        with open(filename) as f:
            self.coords = [(float(line[0]),float(line[1])) for line in [lines.split(',') for lines in f][1:]]