from concurrent.futures import thread
from flask import Flask, render_template, jsonify
import csv
from simulation.simulation import Simulation
from threading import Thread


app = Flask(__name__, static_url_path="/static")

## Start Simulation
s = Simulation()


@app.route("/")
def home():
    refresh_rate = 100
    intersection = "41.703456 , -8.797550"
    thr = Thread(target=s.run)
    thr.start()
    return render_template("index.html", intersection_point=intersection, refresh_rate=refresh_rate)


@app.route("/get_status", methods=["GET", "POST"])
def get_coords():
    status = s.get_status()
    return jsonify(status)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
