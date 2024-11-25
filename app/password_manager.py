import json
import os
import uuid
from datetime import datetime
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import secrets
import pyperclip
import re

def password_strength(password):
    score = 0
    recommendations = []

    # Longitud de la contraseña
    if len(password) >= 8:
        score += 1
    else:
        recommendations.append("La contraseña debe tener al menos 8 caracteres.")

    # Uso de mayúsculas
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        recommendations.append("La contraseña debe incluir al menos una letra mayúscula.")

    # Uso de minúsculas
    if re.search(r'[a-z]', password):
        score += 1
    else:
        recommendations.append("La contraseña debe incluir al menos una letra minúscula.")

    # Uso de números
    if re.search(r'[0-9]', password):
        score += 1
    else:
        recommendations.append("La contraseña debe incluir al menos un número.")

    # Uso de caracteres especiales
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        recommendations.append("La contraseña debe incluir al menos un carácter especial.")

    return score, recommendations

def suggest_password():
    return generate_secure_password()

def view_password_strength(session, localization, folder, entry):
    passwords = load_passwords()
    if session not in passwords:
        print(localization.translate("no_passwords_saved"))
        return

    decrypted_password = cipher.decrypt(entry['password'].encode()).decode()
    score, recommendations = password_strength(decrypted_password)
    stars = '★' * score + '☆' * (5 - score)
    print(f"{localization.translate('password_strength')}: {stars}")
    if recommendations:
        print(localization.translate('recommendations'))
        for recommendation in recommendations:
            print(f"- {recommendation}")
    print(f"{localization.translate('suggested_password')}: {suggest_password()}")
    input(localization.translate("press_enter"))
    
PASSWORD_FILE = "data/passwords.json"
DEFAULT_FOLDER = "No categorizado"

# Cargar la semilla desde el archivo .env
load_dotenv()
seed = os.getenv("AES_KEY").encode()
cipher = Fernet(seed)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_passwords():
    if not os.path.exists(PASSWORD_FILE):
        # Crear el archivo si no existe
        with open(PASSWORD_FILE, 'w') as file:
            json.dump({}, file)

    # Manejar archivo vacío
    with open(PASSWORD_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}  # Retornar un diccionario vacío si el archivo no tiene contenido válido

def save_passwords(passwords):
    with open(PASSWORD_FILE, "w") as file:
        json.dump(passwords, file, indent=4)

def generate_secure_password(length=12):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+"
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def add_password(session, localization):
    passwords = load_passwords()
    
    if session not in passwords:
        passwords[session] = {"folders": {}}

    folders = list(passwords[session]["folders"].keys())
    
    if folders:
        print(localization.translate("available_folders"))
        for i, folder in enumerate(folders, 1):
            print(f"{i}. {folder}")
        
        folder_option = input(localization.translate("select_folder"))
        
        if folder_option.isdigit() and 1 <= int(folder_option) <= len(folders):
            folder = folders[int(folder_option) - 1]
        else:
            print(localization.translate("invalid_option_using_default"))
            folder = DEFAULT_FOLDER
    else:
        print(localization.translate("no_folders_using_default"))
        folder = DEFAULT_FOLDER

    name = input(localization.translate("enter_service_name"))
    username = input(localization.translate("enter_username"))
    password = input(localization.translate("enter_password_or_generate"))

    if not password:
        password = generate_secure_password()
        print(localization.translate("generated_password"), password)

    # Cifrar la contraseña usando AES
    encrypted_password = cipher.encrypt(password.encode()).decode()

    if folder not in passwords[session]["folders"]:
        passwords[session]["folders"][folder] = []

    # Generar un UUID para la nueva contraseña
    password_id = str(uuid.uuid4())

    passwords[session]["folders"][folder].append({
        "id": password_id,
        "name": name,
        "username": username,
        "password": encrypted_password,
        "updated_at": datetime.now().isoformat()
    })

    save_passwords(passwords)
    print(localization.translate("password_added_success"))
    input(localization.translate("press_enter"))  # Pausa para mostrar el mensaje de éxito

def view_password(session_id, localization, folder_name):
    passwords = load_passwords()
    if session_id not in passwords or folder_name not in passwords[session_id]['folders']:
        print(localization.translate('no_passwords_saved'))
        return

    folder = passwords[session_id]['folders'][folder_name]
    if not folder:
        print(localization.translate('no_passwords_saved'))
        return

    for entry in folder:
        print(f"{entry['id']}: {entry['name']} ({entry['username']})")

    option = input(localization.translate('select_password'))
    selected_entry = next((e for e in folder if e['id'] == option), None)

    if selected_entry:
        decrypted_password = cipher.decrypt(selected_entry['password'].encode()).decode()
        print(f"password: {decrypted_password}")
    else:
        print(localization.translate('invalid_option'))

def delete_password(session, localization, folder):
    passwords = load_passwords()
    if session not in passwords:
        print(localization.translate("no_passwords_saved"))
        return

    entries = passwords[session]["folders"].get(folder, [])
    if not entries:
        print(localization.translate("no_passwords_saved"))
        return

    for idx, entry in enumerate(entries, 1):
        print(f"{idx}. ID: {entry['id']} - {entry['name']} - {localization.translate('username')}: {entry['username']}")

    entry_option = input(localization.translate("select_password_to_delete"))
    if entry_option.isdigit() and 1 <= int(entry_option) <= len(entries):
        del passwords[session]["folders"][folder][int(entry_option) - 1]
        save_passwords(passwords)
        print(localization.translate("password_deleted_success"))
    else:
        print(localization.translate("invalid_option"))
    input(localization.translate("press_enter"))

def edit_password(session, localization, folder, entry):
    passwords = load_passwords()
    if session not in passwords:
        print(localization.translate("no_passwords_saved"))
        return

    entries = passwords[session]["folders"].get(folder, [])
    if not entries:
        print(localization.translate("no_passwords_saved"))
        return

    clear_screen()
    print(f"{localization.translate('selected_password')}: {entry['name']} - {localization.translate('username')}: {entry['username']}")
    new_password = input(localization.translate("enter_new_password"))
    encrypted_password = cipher.encrypt(new_password.encode()).decode()
    entry["password"] = encrypted_password
    entry["updated_at"] = datetime.now().isoformat()
    save_passwords(passwords)
    print(localization.translate("password_updated_success"))
    input(localization.translate("press_enter"))

def copy_password(session, localization, folder):
    passwords = load_passwords()
    if session not in passwords:
        print(localization.translate("no_passwords_saved"))
        return

    entries = passwords[session]["folders"].get(folder, [])
    if not entries:
        print(localization.translate("no_passwords_saved"))
        return

    for idx, entry in enumerate(entries, 1):
        print(f"{idx}. ID: {entry['id']} - {entry['name']} - {localization.translate('username')}: {entry['username']}")

    entry_option = input(localization.translate("select_password_to_copy"))
    if entry_option.isdigit() and 1 <= int(entry_option) <= len(entries):
        entry = passwords[session]["folders"][folder][int(entry_option) - 1]
        decrypted_password = cipher.decrypt(entry['password'].encode()).decode()
        pyperclip.copy(decrypted_password)
        print(localization.translate("password_copied"))
    else:
        print(localization.translate("invalid_option"))
    input(localization.translate("press_enter"))

def copy_username(session, localization, folder):
    passwords = load_passwords()
    if session not in passwords:
        print(localization.translate("no_passwords_saved"))
        return

    entries = passwords[session]["folders"].get(folder, [])
    if not entries:
        print(localization.translate("no_passwords_saved"))
        return

    for idx, entry in enumerate(entries, 1):
        print(f"{idx}. ID: {entry['id']} - {entry['name']} - {localization.translate('username')}: {entry['username']}")

    entry_option = input(localization.translate("select_username_to_copy"))
    if entry_option.isdigit() and 1 <= int(entry_option) <= len(entries):
        entry = passwords[session]["folders"][folder][int(entry_option) - 1]
        pyperclip.copy(entry['username'])
        print(localization.translate("username_copied"))
    else:
        print(localization.translate("invalid_option"))
    input(localization.translate("press_enter"))

def view_password(session_id, localization, folder_name):
    passwords = load_passwords()
    if session_id not in passwords or folder_name not in passwords[session_id]['folders']:
        print(localization.translate('no_passwords_saved'))
        return

    folder = passwords[session_id]['folders'][folder_name]
    if not folder:
        print(localization.translate('no_passwords_saved'))
        return

    for index, entry in enumerate(folder):
        print(f"{index + 1}: {entry['name']} ({entry['username']})")

    try:
        option = int(input(localization.translate('select_password'))) - 1
        if option < 0 or option >= len(folder):
            raise ValueError
    except ValueError:
        print(localization.translate('invalid_option'))
        return

    selected_entry = folder[option]

    decrypted_password = cipher.decrypt(selected_entry['password'].encode())
    if isinstance(decrypted_password, bytes):
        decrypted_password = decrypted_password.decode()
    print(f"password: {decrypted_password}")

    # Esperar a que el usuario presione una tecla para continuar
    input(localization.translate('press_any_key_to_continue'))



def count_passwords(session):
    passwords = load_passwords().get(session, {"folders": {}})
    total_passwords = 0
    for folder, entries in passwords["folders"].items():
        total_passwords += len(entries)
    return total_passwords