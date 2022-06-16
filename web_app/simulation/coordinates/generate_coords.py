from posixpath import normpath
from geopy.distance import geodesic as GD

number_of_coords = 100
f1 = "lane_1_new"
f2 = "lane_2_new"
f3 = "lane_merge_new"
start_coord = (41.703456, -8.797550)

l1 = []
l2 = []
lm = []

for i in range(0, number_of_coords):
    east_coord = GD(meters=3.75).destination(start_coord, 60).format_decimal()
    east_coord2 = GD(meters=7).destination(start_coord, 60).format_decimal()
    north_coord = GD(meters=1).destination(start_coord, 150).format_decimal()
    start_coord = north_coord
    l1.append(east_coord)
    l2.append(east_coord2)
    lm.append(north_coord)


print(lm)
