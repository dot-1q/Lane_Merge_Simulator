import os
from geopy.distance import geodesic as GD


class Route:
    def __init__(self, name):
        self.name = name
        self.coords = []
        self.load_coords()
        self.route_length = len(self.coords)
        self.longitudes = [coord[1] for coord in self.coords]

    def __getitem__(self, key):
        return self.coords[key]

    def get_longitudes(self):
        return self.longitudes

    def next_coord(self, car_position, speed):
        velocity_ms = self.kmh_to_ms(speed)  # speed in km/h
        distance_m = self.next_distance(velocity_ms, 0.5)
        new_position = self.next_position(car_position, distance_m)
        return new_position, self.coords[(new_position) % self.route_length]

    def kmh_to_ms(self, speed):
        return (speed * 1000) / 3600

    # method to calculate how much distance a car drive from previous coords
    # for default, refresh rate is 1.5 sec
    # speed in m/s and time in sec
    def next_distance(self, speed, refresh_rate):
        return round(speed * refresh_rate, 4)

    def next_position(self, position, distance):
        for pos in range(position + 1, len(self.coords)):
            d = GD(self.coords[position], self.coords[pos]).m

            if d >= distance:
                return pos
        return 0

    def get_route_coords(self):
        return self.coords

    def load_coords(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, "coordinates", self.name + ".csv")
        with open(filename) as f:
            self.coords = [
                (float(line[0]), float(line[1]))
                for line in [lines.split(",") for lines in f][1:]
            ]
