from flask import Flask, render_template, jsonify
import csv


app = Flask(__name__, static_url_path='/static')
global counter
global route_merge
counter = 0
with open('simulation/coords/merging_lane.csv') as f:
    route_merge = [{k: (v) for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]
@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/get_coords", methods=['GET','POST'])
def get_coords():
    global counter
    global route_merge
    c = route_merge[counter]
    counter = (counter +1 )%(len(route_merge))
    return jsonify(c)

if __name__ == "__main__":
    app.run(debug=True)