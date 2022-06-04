from simulation.route import Route

class Navigation:
    
    def __init__(self,all_routes,initial_route):
        self.all_routes = all_routes
        self.set_route(initial_route)
        self.position = 0
    

    def set_route(self, route_name):
        for route in self.all_routes:
            if route.name == route_name:
                self.current_route = route
    
    def get_coords(self,speed):
        self.position, coords = self.current_route.next_coord(self.position, speed)
        return coords
    
    def get_position(self):
        return self.position