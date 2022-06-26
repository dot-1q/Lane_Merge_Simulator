## Lane Merge Simulator using Vanetza to exchange ITS-G5 messages

## DEMO
![alt text](lane_merge.gif)

## How to install

Make sure you have the latest NAP-Vanetza docker image.
You can get it [here](https://code.nap.av.it.pt/mobility-networks/vanetza).
Note that the tag you give it upon installing it, need's to be the same that's on the [docker-compose.yml](web_app/simulation/docker-compose.yml) file.
In this case, we built it with the tag **vanetza:lane_merge**
1. Clone this repository
```bash
git clone https://github.com/dot-1q/Lane_Merge_Simulator.git
cd Lane_Merge_Simulator
```

2. Create a virtual environment (venv)
```bash
python3 -m venv venv
```

3. Activate the virtual environment (you need to repeat this step, and this step only, every time you start a new terminal/session):
```bash
source venv/bin/activate
```

4. Install the game requirements:
```bash
pip3 install -r requirements.txt
```

## How to run

```bash
python3 web_app/main.py
```

**Before launching the localhost web page, make sure you have the OBU's and RSU's containers running**

On a **NEW** a new terminal window but still inside the repo's directory
```bash
cd web_app/simulation/
docker-compose up 
```
To kill the docker-compose, simply CTRL+C

