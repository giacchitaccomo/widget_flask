
from organizers import initialize
import logging
import pathlib
from datetime import datetime, timedelta
import json #debugging iniziale
from flask import Flask, render_template


path = pathlib.Path(__file__).parent #first i retrieve the full path (the one with main.py), and then i retreive the dir main is in with .parent


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(funcName)s] / (%(asctime)s.%(msecs).03d) - %(levelname)s - %(message)s", #formatta i messaggi di logging al livello di DEBUG 
    datefmt="%I:%M:%S"
    
)

voti_materia, voti_tempo, compiti_materia, compiti_time, materie, orario, orario_html = initialize(path)     
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/orario_settimanale")
def orario_settimanale():
    return render_template("orario_settimanale.html", orario_html = orario_html)

@app.route("/voti")
def voti():
    return render_template("voti.html")

@app.route("/compiti")
def compiti():
    return render_template("compiti.html")


def main():
    app.run(debug=False)
    pass
    
  
  
if __name__ == "__main__":
    main()
