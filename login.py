import requests
import logging
import json





def fetch(path):
    """
    Dal sito del registro elettronico accedo e ricavo le informazioni generali, ritornate come dict
    """
    url =  "https://" + "galilei-cr-sito.registroelettronico.com/api/v4/utenti/login-web/"
    pack = ""
    
    path = path / "config.txt"
    
    with open(path, "r") as r:
        pack = json.load(r)
        
    answer = requests.post(url, json=pack)
    logging.debug("Accesso eseguito con successo")
    
    return answer.json()
        
        
        
    
