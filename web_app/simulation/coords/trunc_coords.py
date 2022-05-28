coord_file = open('merge_lane.csv','r+')
new_coord_file = open('coords_trunc.csv','w+')

a = [[float(line[0]),float(line[1])] for line in [lines.split(',') for lines in coord_file][1:]]

new_coord_file.write("lat,lon\n")
for coord in a:
    new_coordX = round(coord[0],7)
    new_coordY = round(coord[1],7)
    new_coord_file.write(str(new_coordX) + "," + str(new_coordY)+"\n")
