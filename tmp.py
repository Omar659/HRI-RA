import json

# Crea un dizionario di esempio
data = {
    "image_name": "./../images/tiles/tiles_1b.png",
    "difficult": "easy",
    "tiles": [["5", "0", "4"], 
              ["1", "-", "7"],
              ["3", "2", "6"]],
    "bx": 1,
    "by": 1,
    # "tiles": [
    #     ["0", "1", "2"], 
    #     ["3", "4", "5"],
    #     ["6", "-", "7"]
    # ],
    # "bx": 2,
    # "by": 1,
    "record_moves": "37",
    "record_time": "05.23"
}

# Specifica il percorso del file JSON in cui vuoi scrivere i dati
percorso_file_json = "./data/game_status.json"

# Usa la funzione `json.dump()` per scrivere il dizionario nel file JSON
with open(percorso_file_json, "w") as file_json:
    json.dump(data, file_json)

print("Dati scritti con successo nel file JSON.")
