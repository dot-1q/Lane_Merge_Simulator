from simulation.obu import OBU
from simulation.rsu import RSU
from simulation.route import Route
import time


class Simulation:
    def __init__(self):
        self.cars = []

    def run(self):

        route_1 = Route("lane_1")
        route_2 = Route("lane_2")
        route_merge = Route("merge_lane")

        self.cars.append(OBU("car_1", 2, "192.168.98.10", 10, 3, route_1))
        self.cars.append(OBU("car_2", 3, "192.168.98.11", 10, 3, route_2))
        self.cars.append(OBU("car_merge", 4, "192.168.98.12", 10, 3, route_merge))

        while True:
            for car in self.cars:
                car.set_coords(car.route.next_coord(0))

            time.sleep(0.3)

    def get_status(self):
        status = {}
        for car in self.cars:
            s = {"speed": car.speed, "state": car.state, "coords": car.coords}
            status[car.name] = s
        return status


if __name__ == "__main__":
    s = Simulation()
    s.run()
