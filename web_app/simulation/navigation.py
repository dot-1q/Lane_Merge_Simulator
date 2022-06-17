from simulation.route import Route
import math
import numpy as np
from geopy.distance import geodesic as GD


class Navigation:
    def __init__(self, all_routes, initial_route):
        self.all_routes = all_routes
        self.current_route: Route = None
        self.set_route(initial_route)
        self.position = 0
        # Adjacent routes
        self.adjacency = {
            "lane_1":  "lane_2",
            "lane_2": "lane_1",
            "lane_merge": "lane_1",
        }
        self.intersection = None
        # This is the safe distance in meters, meaning, it's the space that has to
        # be in between cars for safe driving on the road
        self.safe_distance = 5

    def set_route(self, route_name):
        for route in self.all_routes:
            if route.name == route_name:
                self.current_route = route

    def get_coords(self, speed):
        self.position, coords = self.current_route.next_coord(self.position, speed)
        return coords

    def get_position(self):
        return self.position

    def get_adj_route(self):
        for lane, adj in self.adjacency.items():
            if lane == self.current_route.name:
                return self.get_route(adj)

    # Get the new merge location, given the route we want to enter
    # By default, we get the coordinate that is 2 meters ahead in the new route
    def get_merge_location(self, route):
        # in range is a slice till the end of the coordinates array. Mind the ":"
        for new_p in route[self.position:]:
            d = GD(route[self.position], new_p).m

            # the new position has to be 2 meters, and we need to
            # make sure it's ahead, because sometimes it could calculate
            # 2 meters behind
            if d >= 2 and (not self.is_behind(new_p, self.current_route[self.position])):
                return new_p
        return 0

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

    def get_route(self, name):
        for route in self.all_routes:
            if route.name == name:
                return route

    def set_position(self, position):
        self.position = position

    def space_between(self, route, length):
        # Distance backwards and distance forward refer to the set of coordinates
        # that delimits the space needed for merge
        # It's calculated by adding and subtracting from the new position we want to be in,
        # The length/2 of the car and the safe distance that needs to be between cars
        backward_limit = 0
        forward_limit = 0

        margin = float(length/2) + self.safe_distance

        # TODO THIS NEEDS TO URGENTLY BY OPTIMIZIED, SINCE WHILE
        # IN PYTHON IS HIGHLY INNEFICIENT
        # PLUS, IT LOOKS UGLY

        # Find the coordinate that is sufficiently backwards from the merge
        # point
        offset = 0
        while 1:
            distance = GD(route[self.position], route[self.position-offset]).m
            if distance >= margin:
                backward_limit = offset
                break
            offset += 1

        # Find the coordinate that is sufficiently forwards from the merge
        # point
        offset = 0
        while 1:
            distance = GD(route[self.position], route[self.position+offset]).m
            if distance >= margin:
                forward_limit = offset
                break
            offset += 1

        # Return the slice of the route that is encompassed by the distance we want
        return route[(self.position - backward_limit):(self.position + forward_limit)]

    # Check if a given car coordinate is withing a set of coordinates
    # We had to implement this in our own way, since the comunication with vanetza
    # introduced unwanted rounding.
    # Because of that, we couldn't simply use the python one liner "is" to check
    # if a coordinate is in an array of coordinates
    def check_in_between(self, space, car_coord):
        for coord in space:
            # Means that the distance from our set os space coordinates
            # And the coordinate of the car , falls between a margin of error acceptable
            # Also, to optimize, we only check on the latitude  coordinate
            if math.isclose(coord[0], car_coord[0], abs_tol=0.000002):
                return True
        # Else, it is not in that space
        return False

    def check_in_route(self, route, car_coord):
        for coord in route:
            # Means that the distance from our set os space coordinates
            # And the coordinate of the car , falls between a margin of error acceptable
            # Also, to optimize, we only check on the latitude  coordinate
            if math.isclose(coord[0], car_coord, abs_tol=0.000002):
                return True
        # Else, it is not in that space
        return False
