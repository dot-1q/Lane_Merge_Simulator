from flask import Flask, render_template, jsonify
import csv


app = Flask(__name__, static_url_path="/static")
global counter
global route_merge
global route_1
global route_2
counter = 0

with open("simulation/coords/merge_lane.csv") as f:
    route_merge = [
        {k: (v) for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)
    ]
with open("simulation/coords/lane_1.csv") as f:
    route_1 = [
        {k: (v) for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)
    ]
with open("simulation/coords/lane_2.csv") as f:
    route_2 = [
        {k: (v) for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)
    ]


@app.route("/")
def home():
    global counter
    counter = 0
    intersection = "41.703456 , -8.797550"
    return render_template("index.html", intersection_point=intersection)


@app.route("/get_status", methods=["GET", "POST"])
def get_coords():
    global counter
    global route_merge
    global route_1
    global route_2
    merge = route_merge[counter]
    l1 = route_1[counter]
    l2 = route_2[counter]
    counter = (counter + 3) % (len(route_merge))

    status_merge = {"speed": 100, "status": "merging", "coords": merge}
    status_car_1 = {"speed": 100, "status": "merging", "coords": l1}
    status_car_2 = {"speed": 100, "status": "merging", "coords": l2}

    all_coords = {
        "car_merge": status_merge,
        "car_1": status_car_1,
        "car_2": status_car_2,
    }
    return jsonify(all_coords)


if __name__ == "__main__":
    app.run(debug=True)
