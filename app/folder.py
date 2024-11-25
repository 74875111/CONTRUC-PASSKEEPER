import json
import os

FOLDER_FILE = "data/folders.json"

def load_folders():
    # Crear archivo vacío si no existe
    if not os.path.exists(FOLDER_FILE):
        with open(FOLDER_FILE, 'w') as file:
            json.dump({}, file)

    # Intentar cargar el JSON
    with open(FOLDER_FILE, 'r') as file:
        try:
            data = json.load(file)
            if not isinstance(data, dict):  # Verificar que sea un diccionario
                raise ValueError("Formato inválido en el archivo JSON de carpetas")
            return data
        except (json.JSONDecodeError, ValueError):
            return {}