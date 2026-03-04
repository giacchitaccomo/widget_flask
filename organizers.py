import logging
from collections import defaultdict
from cache import save_cache, fetch_cache
from fetchers import fetch_online
from login import fetch
from datetime import date, timedelta, datetime

inizio = str(date.today())
fine = str(date.today() + timedelta(days=6))

def get_day(date):
    

    dt = datetime.fromisoformat(date)

    giorni = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6
    }

    date = giorni[dt.strftime("%A")]
    
    return date





urls = {
    "materie" : "https://galilei-cr-sito.registroelettronico.com/api/v3/scuole/galilei-cr/studenti/1008147/2025_2026/materie_nextapi/" , #per ora funziona solo con me (1008147)
    "compiti" : "https://galilei-cr-sito.registroelettronico.com/api/v3/scuole/galilei-cr/studenti/1008147/2025_2026/compiti_plain/",
    "voti" : "https://galilei-cr-sito.registroelettronico.com/api/v3/scuole/galilei-cr/studenti/1008147/2025_2026/voti_plain/",
    "orario" : f"https://galilei-cr-sito.registroelettronico.com/api/v3/scuole/galilei-cr/studenti/1008147/2025_2026/orario_plain/?data_inizio={inizio}&data_fine={fine}"
    
}

files = {
    "compiti_time" : "compiti_time.txt",
    "voti_time" : "voti_time.txt",
    "materie" : "materie.txt", 
    "compiti_materia" : "compiti_materia.txt",
    "voti_materia" : "voti_materia.txt",
    "info" : "cache.txt",
    "orario" : "orario.txt",
    "orario_html" : "orario_html.txt"
}

def initialize(path):
    
    not_online = True
    print(" Online? y if yes anything if else")
    ans = input("> ")
    if ans.lower() == "y":
        not_online = False
        
    
    if not_online:
        # OFFLINE: read everything from cache
        info = fetch_cache(path, files["info"])
        materie = fetch_cache(path, files["materie"])
        compiti_materia = fetch_cache(path, files["compiti_materia"])
        compiti_time = fetch_cache(path, files["compiti_time"])
        voti_materia = fetch_cache(path, files["voti_materia"])
        voti_tempo = fetch_cache(path, files["voti_time"])
        orario = fetch_cache(path, files["orario"])
        orario_html = fetch_cache(path, files["orario_html"])

    else:
        # ONLINE: fetch from server and rebuild caches
        info = fetch(path)
        info = catalog_info(info, path)

        headers = info["headers"]

        materie_raw = fetch_online(headers, urls["materie"])
        materie = categorize_subjects(materie_raw, path)

        compiti_raw = fetch_online(headers, urls["compiti"])
        compiti_materia, compiti_time = catalog_compiti(compiti_raw, path)

        voti_raw = fetch_online(headers, urls["voti"])
        voti_materia, voti_tempo = catalog_voti(voti_raw, path)
        
        orario = fetch_online(headers, urls["orario"])
        orario, orario_html = catalog_orario(orario, path, materie)

    return voti_materia, voti_tempo, compiti_materia, compiti_time, materie, orario, orario_html
    
  
    
def categorize_subjects(subjects, path):   
    materie = {}
    
    
    for x in subjects:
        prof = x["professori"][0]["nome"]
        nome = x["nome_materia_sito"]
        id_materia = x["id"]
        
        materie[id_materia] = {
            "professore" : prof,
            "nome" : nome,  
        }
    
    save_cache(materie, path, files["materie"] )
    
    return materie     
        

def catalog_info(answer, path):
    """
    ricava alcune info utili dal blocco restituito al login
    """
    
    
    
    info = {}
    info["nome"] = answer["studenti"][0]["nome"]
    info["indirizzo"] = answer["studenti"][0]["anni"][0]["indirizzo"]
    info["classe"] = answer["studenti"][0]["anni"][0]["classe"]
    info["token"] = answer["token"]
    
    headers = {
        "authorization" : "JWT " + info["token"]
        } 
 
    info["headers"] = headers
    logging.debug("Info categorized successfully")
    save_cache(info, path, files["info"])
    return info


def catalog_orario(orario, path, materie):
    orario_org = defaultdict(list)
    corrette = fetch_cache(path, "materie_corrette.txt")
    last_weight = -1
    last_seen = ""
    orario_pulito = []
    
    for x in range(len(orario)):
        obj = orario[x]
        nome = materie[obj["id_materia"]]["nome"]
        weight = corrette[nome][1]
        ora = obj["data_ora_inizio"]
        
        orario_pulito.append(obj)
        if last_seen == ora:
            if last_weight > weight:
                orario_pulito.pop()
            else:
                orario_pulito.pop(-2)
                
        last_seen = ora
        last_weight = weight

    
    
    for obj in orario_pulito:

        orario_org[get_day(obj["data_ora_inizio"][:10])].append(corrette[materie[obj["id_materia"]]["nome"]][0]) 
        

    orario_ordinato = dict(sorted(orario_org.items()))
    
    orario_html = {}

    giorni_chiavi = [0, 1, 2, 3, 4, 5] 
    orario_html = {}

    for x in range(8):
        if x == 5:
  
            orario_html[x] = "PAUSA"
            continue
        
        # x_adj serve per saltare l'indice della pausa
  
        x_adj = x if x < 5 else x - 1
        riga_ora = []
        
        for g in giorni_chiavi:
            # orario_ordinato deve essere il dict {giorno: [materie]}
            materie_giorno = orario_ordinato.get(g, [])
            
            if len(materie_giorno) > x_adj:
                riga_ora.append(materie_giorno[x_adj])
            else:
                riga_ora.append("") # Cella vuota se non c'è lezione
        
        orario_html[x] = riga_ora

    save_cache(orario_html, path, files["orario_html"])  
    save_cache(orario_ordinato, path, files["orario"])   
    return orario_ordinato, orario_html
    


#migliorato
# def catalog_compiti(compiti):
#     answer = {}
    
    
#     data_compito = namedtuple("data_compito", ["year", "month", "day", "hour"])
    
#     for x in compiti:
#         nome = x["sottotitolo"]
#         consegna = x["assegnazioni"]
        
#         d = x["data"]
#         tempo = data_compito(
#             d[0:4],
#             d[5:7],
#             d[8:10],
#             d[11:16]
#             )
        
#         answer[tempo] = {
#             "data" : tempo,
#             "materia" : nome, 
#             "consegna" : consegna
#         }
        
#     return answer

def parse_ISO(d):
    month, day = d[5:7], d[8:10]
    s = str(month) + "-" + str(day)
    return s


def catalog_compiti(compiti, path): 
    by_materia = defaultdict(list)
    by_time = defaultdict(list)
    
    for x in compiti:
        materia = x["sottotitolo"]
        consegna = x["assegnazioni"]
        d = x["data"]
        
        
        time = parse_ISO(d)
        
        by_materia[materia].append({"time" : time, "consegna" : consegna})
        by_time[time].append({"materia" : materia, "consegna" : consegna})
        
        
        
    save_cache(by_materia, path, files["compiti_materia"])
    save_cache(by_time, path, files["compiti_time"])
    return by_materia, by_time #tuple key is faster for filtering 


def catalog_voti(voti, path):
    by_materia = defaultdict(list)
    by_time = defaultdict(list)
    
    for x in voti:
        materia = x["titolo"]
        argomento = x["dettaglio"]
        tipo = x["sottotitolo"]
        valore = x["voto_numerico"]
        time = parse_ISO(x["data"])
        
        by_materia[materia].append({"argomento" : argomento, "tipo" : tipo, "valore" : valore, "data" : time})
        by_time[time].append({"argomento" : argomento, "tipo" : tipo, "valore" : valore, "materia" : materia})
        
    save_cache(by_materia, path, files["voti_materia"])
    save_cache(by_time, path, files["voti_time"])
        
    return by_materia, by_time 
        