import json

file = "Config.json"

def leer(leer : str):
    with open(file, "r") as f:
        lista = json.load(f)
    return lista.get(leer, [])

def editar(c : str):
    with open(file, "r") as f:
        leer = json.load(f)
    with open(file, "w") as f:
        leer[c] = 1
        json.dump(leer, f, indent = 4, ensure_ascii = False)