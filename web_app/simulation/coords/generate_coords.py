coord_file = open('test.csv','r+')
new_coord_file = open('coord_between.csv','w+')


a = [[float(line[0]),float(line[1].strip())] for line in [lines.split(',') for lines in coord_file][1:]]

new_coord_file.write("lat,lon\n")
for line in range(0,len(a)-1):
    new_coordX = (a[line][0] + a[line+1][0])/2
    new_coordY = (a[line][1] + a[line+1][1])/2
    new_coord_file.write(str(a[line][0]) + "," + str(a[line][1])+"\n")
    new_coord_file.write(str(new_coordX) + "," + str(new_coordY)+"\n")

new_coord_file.write(str(a[len(a)-1][0]) + "," + str(a[len(a)-1][1])+"\n")

