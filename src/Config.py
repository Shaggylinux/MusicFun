import json
import os

def obtener_ruta_config():
    data_dir = os.environ.get("FLET_APP_DATA_DIR", ".") 
    return os.path.join(data_dir, "Config.json")

def leer(clave : str):
    ruta = obtener_ruta_config()
    if not os.path.exists(ruta):
        base = {"Version": "0.0.4", "Path": "", "Aceptar": 0, "Changelog": ["Alerta de descarga completa"]}
        with open(ruta, "w") as f:
            json.dump(base, f)
        return base.get(clave)
    
    with open(ruta, "r") as f:
        lista = json.load(f)
    return lista.get(clave, [])

def editar(clave : str, valor):
    ruta = obtener_ruta_config()
    linea = {}
    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            linea = json.load(f)
    
    with open(ruta, "w") as f:
        linea[clave] = valor
        json.dump(linea, f, indent=4, ensure_ascii=False)