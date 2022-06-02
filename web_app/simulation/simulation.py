from simulation.obu import OBU
from simulation.rsu import RSU
from simulation.route import Route
from threading import Thread
import time


class Simulation:
    def __init__(self):
        self.cars = []
        self.rsu = RSU("rsu", 1, "192.168.98.254", 5, 10, (41.704018, -8.798036))

    def run(self):

        route_1 = Route("lane_1")
        route_2 = Route("lane_2")
        route_merge = Route("merge_lane")

        self.cars.append(OBU("car_1", 2, "192.168.98.10", 10, 3, route_1, 30))
        self.cars.append(OBU("car_2", 3, "192.168.98.11", 10, 3, route_2,120))
        self.cars.append(OBU("car_merge", 4, "192.168.98.12", 10, 3, route_merge,60))

        thr_rsu = Thread(target=self.rsu.start)
        thr_rsu.start()

        thr_cars=[]
        for i in range(0,len(self.cars)):
            thr = Thread(target=self.cars[i].start)
            thr_cars.append(thr)
            thr.start()


    def get_status(self):
        status = {}
        for car in self.cars:
            s = {"speed": car.speed, "state": car.state, "coords": car.coords}
            status[car.name] = s
        return status


if __name__ == "__main__":
    s = Simulation()
    s.run()
