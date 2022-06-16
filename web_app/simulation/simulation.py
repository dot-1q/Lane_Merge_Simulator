from simulation.navigation import Navigation
from simulation.obu import OBU
from simulation.rsu import RSU
from simulation.route import Route
from threading import Thread
import random


class Simulation:
    def __init__(self):
        self.cars = []
        self.rsu = RSU("rsu", 1, "192.168.98.254", 5, 10, (41.704018, -8.798036))

    def run(self):

        routes = []
        routes.append(Route("lane_1"))
        routes.append(Route("lane_2"))
        routes.append(Route("lane_merge"))

        self.cars.append(OBU("car_merge", 4, "192.168.98.12", 5, 2, Navigation(routes, "lane_merge"), 57))
        self.cars.append(OBU("car_1", 2, "192.168.98.10", 5, 2, Navigation(routes, "lane_1"), 60))
        self.cars.append(OBU("car_2", 3, "192.168.98.11", 5, 2, Navigation(routes, "lane_2"), random.randint(110, 120)))

        thr_rsu = Thread(target=self.rsu.start)
        thr_rsu.start()

        thr_cars = []
        for i in range(0, len(self.cars)):
            thr = Thread(target=self.cars[i].start)
            thr_cars.append(thr)
            thr.start()

        for thr in thr_cars:
            thr.join()
        thr_rsu.join()

    def get_status(self):
        status = {}
        space = (0, 0)
        for car in self.cars:
            s = {"speed": car.speed, "state": car.state, "coords": car.coords}
            status[car.name] = s
            # Means he is merging to a new position
            if (car.new_space is not None):
                space = car.new_space
        
        status['inter'] = {"coords": space}
        return status


if __name__ == "__main__":
    s = Simulation()
    s.run()
