import requests





def fetch_online(headers, url):
    """
    trasforma in un dizionario e ritorna la risposta di get(url)
    """
    response = requests.get(url=url, headers=headers)
    response = response.json()
    return response




#fatto sì che fetch online sia elastico  

# def fetch_subjects(headers):
#     """
#     crea un dizionario con struttura id_materia : nome_professore, nome_materia
#     """
#     url = "https://galilei-cr-sito.registroelettronico.com/api/v3/scuole/galilei-cr/studenti/1008147/2025_2026/materie_nextapi/" 
    
    
    
#     subjects = requests.get(url=url, headers=headers)
#     subjects = subjects.json()
    
#     return subjects




    

    
    
# def fetch_compiti(headers):
#     """
#     fetch di tutti i compiti, ritorna dict 
#     """
    
#     url = "https://galilei-cr-sito.registroelettronico.com/api/v3/scuole/galilei-cr/studenti/1008147/2025_2026/compiti_plain/"
    
#     answer = requests.get(url, headers=headers)
#     answer = answer.json()
    
#     return answer
    
    
    
# def fetch_voti(headers):
    #//