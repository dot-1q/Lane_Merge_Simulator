from simulation.route import Route
import math
import numpy as np


class Navigation:
    def __init__(self, all_routes, initial_route):
        self.all_routes = all_routes
        self.current_route = []
        self.set_route(initial_route)
        self.position = 0
        # Adjacent routes
        self.adjacency = {
            "lane_1": ["lane_merge", "lane_2"],
            "lane_2": ["lane_1"],
            "lane_merge": ["lane_1"],
        }

    def set_route(self, route_name):
        for route in self.all_routes:
            if route.name == route_name:
                self.current_route = route

    def get_coords(self, speed):
        self.position, coords = self.current_route.next_coord(self.position, speed)
        return coords

    def get_position(self):
        return self.position
    
    def is_behind(self, coord1, coord2):
        dLon = coord2[1] - coord1[1]
        y = math.sin(dLon) * math.cos(coord2[0])
        x = math.cos(coord1[0])*math.sin(coord2[0]) - math.sin(coord1[0])*math.cos(coord2[0])*math.cos(dLon)
        bearing = np.rad2deg(math.atan2(y, x))
        if bearing < 0:
            bearing += 360
        
        # means it's behind
        if bearing >= 90:
            return True
        else:
            return False
