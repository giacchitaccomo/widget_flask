
import logging
import json


    
        
def fetch_cache(path, file):
    """
    cerca nella cache il file argomento, lo restituisce come dict
    """
    
    
    path = path / "cache" / file
    
    with  open(path, "r") as t:
        answer = json.load(t)
        
    messaggio_successo = file + " successfully read"
        
    logging.debug(messaggio_successo)   
    
    return answer



def save_cache(cache, path, file):
    """
    dizionario come argomento, salva nel file il dizionario jsonificato
    """
    
    path = path / "cache" / file
    
    with open(path, "w") as o:
        json.dump(cache, o, indent=4) #scrive in cache con argomento tree
        
    message_success = file + " updated correctly"
        
    logging.debug(message_success)
    
    return 


