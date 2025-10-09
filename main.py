
from organizers import initialize
import logging
import pathlib
import datetime
import json #debugging iniziale
from flask import Flask


path = pathlib.Path(__file__).parent #first i retrieve the full path (the one with main.py), and then i retreive the dir main is in with .parent


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(funcName)s] / (%(asctime)s.%(msecs).03d) - %(levelname)s - %(message)s", #formatta i messaggi di logging al livello di DEBUG 
    datefmt="%I:%M:%S"
    
)

        
app = Flask(__name__)

def main():
    global compiti_time
    today = datetime.datetime.today()
    day = str(today.day) if today.day >= 10 else "0" + str(today.day)
    today = str(today.month) + "-" + day
    
    not_online = True
    print(" Online? y if yes anything if else")
    ans = input("> ")
    if ans.lower() == "y":
        not_online = False
        
    voti_materia, voti_tempo, compiti_materia, compiti_time, materie = initialize(path, not_online)
    

   






        



main()
@app.route("/")
def home():
    return "<h1>Benvenuto</h1><p>Questo è il mio widget</p><a href=/domani><button>Domani</button></a>"




@app.route("/domani")
def domani():
    s = [str(compiti_time[k]) for k in compiti_time if k[0:3] == "10-" and int(k[3:]) > 8]
    return str(s)
    
        
app.run(debug=False)
