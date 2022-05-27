from flask import Flask, render_template, jsonify
import csv


app = Flask(__name__, static_url_path='/static')
global counter
global route_merge
global route_1
global route_2
counter = 0

with open('simulation/coords/merging_lane.csv') as f:
    route_merge = [{k: (v) for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]
with open('simulation/coords/lane_1.csv') as f:
    route_1 = [{k: (v) for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]
with open('simulation/coords/lane_2.csv') as f:
    route_2 = [{k: (v) for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/get_coords", methods=['GET','POST'])
def get_coords():
    global counter
    global route_merge
    global route_1
    global route_2
    merge = route_merge[counter]
    l1 = route_1[counter]
    l2 = route_2[counter]
    counter = (counter +1)%(len(route_2))
    all_coords = {"car1":merge,"car2":l1, "car3": l2}
    return jsonify(all_coords)

if __name__ == "__main__":
    app.run(debug=True)

