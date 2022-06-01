import os
from geopy.distance import geodesic as GD
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
        # vel = self.kmh_to_ms(100)
        # dist = self.next_distance(vel, 0.5)
        # self.position = (self.position + self.next_position(dist))
        return self.coords[self.position]

    def kmh_to_ms(self, speed):
        return (speed*1000)/3600
        
    #fuction tp calculate how much distance a car drive from previous coords
    #for default, refresh rate is 0,5 sec
    #speed in m/s and time in sec
    def next_distance(self, speed, refresh_rate):
        return speed*refresh_rate

    def next_position(self, distance):
        for pos in range(self.position +1, len(self.coords)):
            d = GD(self.coords[self.position], self.coords[pos]).km
            #passar de km to m
            d = d*1000
            if d >= (distance-2) and d <= (distance+2):
                valor =  pos
                break
        return valor

    def prev_coord(self):
        pass

    def set_position(self):
        pass

    def load_coords(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir,'coordinates',self.name+'.csv')
        with open(filename) as f:
            self.coords = [(float(line[0]),float(line[1])) for line in [lines.split(',') for lines in f][1:]]