from simulation.navigation import Navigation
from simulation.obu import OBU
from simulation.rsu import RSU
from simulation.route import Route
from threading import Thread
import time
import random


class Simulation:
    def __init__(self):
        self.cars = []
        self.rsu = None

    def run(self, situation):

        routes = []
        routes.append(Route("lane_1"))
        routes.append(Route("lane_2"))
        routes.append(Route("lane_merge"))
        self.rsu = RSU("rsu", 99, "192.168.98.254", 5, 10, (41.704018, -8.798036))

        # Situation 1 | merge = 70, car_1 = 65
        # Situation 2 | merge = 70, car_1 = 55, car_2 = 70 e lane1

        if situation == 1:
            self.cars.append(OBU("car_merge", 4, "192.168.98.13", 5, 2, Navigation(routes, "lane_merge"), 70))
            self.cars.append(OBU("car_1", 1, "192.168.98.10", 5, 2, Navigation(routes, "lane_1"), 67))
            self.cars.append(OBU("car_2", 2, "192.168.98.11", 5, 2, Navigation(routes, "lane_2"), 75))
            self.cars.append(OBU("car_3", 3, "192.168.98.12", 5, 2, Navigation(routes, "lane_2"), 67))

        elif situation == 2:
            self.cars.append(OBU("car_merge", 4, "192.168.98.13", 5, 2, Navigation(routes, "lane_merge"), 70))
            self.cars.append(OBU("car_1", 1, "192.168.98.10", 5, 2, Navigation(routes, "lane_1"), 55))
            self.cars.append(OBU("car_2", 2, "192.168.98.11", 5, 2, Navigation(routes, "lane_1"), 70))
            self.cars.append(OBU("car_3", 3, "192.168.98.12", 5, 2, Navigation(routes, "lane_2"), 57))

        elif situation == 3:
            self.cars.append(OBU("car_merge", 4, "192.168.98.13", 5, 2, Navigation(routes, "lane_merge"), 65))
            self.cars.append(OBU("car_1", 1, "192.168.98.10", 5, 2, Navigation(routes, "lane_1"), 55))
            self.cars.append(OBU("car_2", 2, "192.168.98.11", 5, 2, Navigation(routes, "lane_1"), 70))
            self.cars.append(OBU("car_3", 3, "192.168.98.12", 5, 2, Navigation(routes, "lane_2"), 45))

        elif situation == 4:
            route_names = ["lane_1", "lane_2"]
            self.cars.append(OBU("car_merge", 4, "192.168.98.13", 5, 2, Navigation(routes, "lane_merge"), random.randint(50, 80)))
            self.cars.append(OBU("car_1", 1, "192.168.98.10", 5, 2, Navigation(routes, route_names[random.randint(0, 1)]), random.randint(50, 80)))
            self.cars.append(OBU("car_2", 2, "192.168.98.11", 5, 2, Navigation(routes, route_names[random.randint(0, 1)]), random.randint(50, 80)))
            self.cars.append(OBU("car_3", 3, "192.168.98.12", 5, 2, Navigation(routes, route_names[random.randint(0, 1)]), random.randint(50, 80)))

        thr_rsu = Thread(target=self.rsu.start)
        thr_rsu.start()

        thr_cars = []
        for i in range(0, len(self.cars)):
            thr = Thread(target=self.cars[i].start)
            thr_cars.append(thr)
            thr.start()

        for thr in thr_cars:
            thr.join()
        
        print("all cars ended")
        self.rsu.finished = True
        thr_rsu.join()

        # Clean up the cars, rsu and their respective threads
        self.cars = []
        self.rsu = None

    def get_status(self):
        status = {}
        bl = (0, 0)
        fl = (0, 0)
        new_position = (0, 0)
        for car in self.cars:
            s = {"speed": car.speed, "state": car.state, "coords": car.coords}
            status[car.name] = s
            # Means he is merging to a new position
            if (car.new_space is not None and car.name == "car_merge"):
                bl = car.bl
                fl = car.fl
                new_position = car.new_space

        # The limits for the merge
        status['bl'] = {"coords": bl}
        status['fl'] = {"coords": fl}
        status['new_position'] = {"coords": new_position}
        return status

    def kill_simulation(self):
        for car in self.cars:
            car.set_finished(True)

        self.rsu.set_finished(True)


if __name__ == "__main__":
    s = Simulation()
    s.run()
