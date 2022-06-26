from flask import Flask, render_template, jsonify, request
from simulation.simulation import Simulation
from threading import Thread
import logging


app = Flask(__name__, static_url_path="/static")

# DISABLE GET AND POST REQUESTS FROM STANDART OUTPUT
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Start Simulation
s = Simulation()


@app.route("/", methods=["GET", "POST"])
def home():
    refresh_rate = 50
    intersection = "41.703456 , -8.797550"
    situation = 0
    if request.method == 'POST':
        if request.form.get('situation1'):
            print("Situation1")
            situation = 1
        if request.form.get('situation2'):
            print("Situation2")
            situation = 2
        if request.form.get('situation3'):
            print("Situation3")
            situation = 3
        if request.form.get('situation4'):
            print("Situation4")
            situation = 4

    if situation != 0:
        thr = Thread(target=s.run, args=[situation])
        thr.start()
        thr.join()

    return render_template("index.html", intersection_point=intersection, refresh_rate=refresh_rate)


@app.route("/get_status", methods=["GET", "POST"])
def get_coords():
    status = s.get_status()
    return jsonify(status)


@app.route("/kill_simulation", methods=["GET"])
def kill_simulation():
    s.kill_simulation()
    return "Killed Simulation"


if __name__ == "__main__":
    app.run(threaded=True)
