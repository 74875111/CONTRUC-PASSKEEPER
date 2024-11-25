import sys
import os
import json
from dotenv import load_dotenv
from localization import Localization

# Asegurarse de que la carpeta raíz esté en el sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app.auth as auth
import app.password_manager as pm

SESSION_FILE = "session.json"
PREFERENCES_FILE = os.path.join("data", "preferences.json")

# Cargar la clave de cifrado desde el archivo .env
load_dotenv()

def load_preferences():
    if os.path.exists(PREFERENCES_FILE):
        with open(PREFERENCES_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {"language": "en"}
    return {"language": "en"}

def save_preferences(preferences):
    with open(PREFERENCES_FILE, 'w') as file:
        json.dump(preferences, file)

# Cargar las preferencias de idioma
preferences = load_preferences()
language = preferences.get("language", "en")
localization = Localization(language)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return None
    return None

def save_session(session):
    with open(SESSION_FILE, 'w') as file:
        json.dump(session, file)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def logout():
    global session
    session = None
    save_session(session)
    print(localization.translate("logout"))
    input(localization.translate("press_enter"))

def change_language():
    global localization
    clear_screen()
    print(f"1. {localization.translate('spanish')}\n2. {localization.translate('english')}")
    option = input(localization.translate("select_language"))
    if option == '1':
        localization.set_language('es')
    elif option == '2':
        localization.set_language('en')
    # Guardar la preferencia de idioma localmente
    preferences["language"] = localization.language
    save_preferences(preferences)
    clear_screen()

def display_menu():
    global session
    while True:
        clear_screen()
        total_passwords = pm.count_passwords(session)
        print(localization.translate("passwords_saved", total=total_passwords))
        print(f"\n1. {localization.translate('add_password')}\n2. {localization.translate('view_passwords')}\n3. {localization.translate('folders')}\n4. {localization.translate('settings')}\n5. {localization.translate('logout')}")
        option = input(localization.translate("enter_option"))
        clear_screen()
        if option == '1':
            pm.add_password(session, localization)
        elif option == '2':
            view_folders()
        elif option == '3':
            manage_folders()
        elif option == '4':
            change_language()
        elif option == '5':
            session = None
            save_session(session)
            break

def view_folders():
    global session
    while True:
        clear_screen()
        passwords = pm.load_passwords().get(session, {"folders": {}})
        folders = list(passwords["folders"].keys())
        
        if not folders:
            print(localization.translate("no_folders_available"))
            input(localization.translate("press_enter"))
            return

        print(localization.translate("available_folders"))
        for i, folder in enumerate(folders, 1):
            num_passwords = len(passwords["folders"][folder])
            print(f"{i}. {folder} ({localization.translate('passwords_saved2', total=num_passwords)})")
        print(f"{len(folders) + 1}. {localization.translate('back_to_menu')}")

        folder_option = input(localization.translate("select_folder"))
        if folder_option.isdigit() and 1 <= int(folder_option) <= len(folders):
            folder = folders[int(folder_option) - 1]
            view_passwords_in_folder(folder)
        elif folder_option == str(len(folders) + 1):
            return
        else:
            print(localization.translate("invalid_option"))
            input(localization.translate("press_enter"))

def view_passwords_in_folder(folder):
    global session
    while True:
        clear_screen()
        passwords = pm.load_passwords().get(session, {"folders": {}})
        entries = passwords["folders"].get(folder, [])

        if not entries:
            print(localization.translate("no_passwords_saved"))
            input(localization.translate("press_enter"))
            return

        print(f"{localization.translate('folder')}: {folder}")
        for idx, entry in enumerate(entries, 1):
            print(f"{idx}. {entry['name']} - {localization.translate('username')}: {entry['username']}")

        print(f"{len(entries) + 1}. {localization.translate('back_to_folders')}")
        password_option = input(localization.translate("enter_option"))
        clear_screen()
        if password_option.isdigit() and 1 <= int(password_option) <= len(entries):
            entry = entries[int(password_option) - 1]
            while True:
                clear_screen()
                print(f"{localization.translate('selected_password')}: {entry['name']} - {localization.translate('username')}: {entry['username']}")
                print(f"\n1. {localization.translate('delete_password')}\n2. {localization.translate('edit_password')}\n3. {localization.translate('copy_password')}\n4. {localization.translate('copy_username')}\n5. {localization.translate('view_password')}\n6. {localization.translate('check_password_strength')}\n7. {localization.translate('back_to_folders')}")
                option = input(localization.translate("enter_option"))
                clear_screen()
                if option == '1':
                    pm.delete_password(session, localization, folder)
                    break
                elif option == '2':
                    pm.edit_password(session, localization, folder, entry)
                    break
                elif option == '3':
                    pm.copy_password(session, localization, folder)
                    break
                elif option == '4':
                    pm.copy_username(session, localization, folder)
                    break
                elif option == '5':
                    pm.view_password(session, localization, folder)
                    break
                elif option == '6':
                    pm.view_password_strength(session, localization, folder, entry)
                    break
                elif option == '7':
                    break
                else:
                    print(localization.translate("invalid_option"))
                    input(localization.translate("press_enter"))
        elif password_option == str(len(entries) + 1):
            return
        else:
            print(localization.translate("invalid_option"))
            input(localization.translate("press_enter"))

def create_folder():
    global session
    passwords = pm.load_passwords()
    if session not in passwords:
        passwords[session] = {"folders": {}}
    
    folder_name = input(localization.translate("enter_new_folder_name"))
    if folder_name in passwords[session]["folders"]:
        print(localization.translate("folder_already_exists"))
    else:
        passwords[session]["folders"][folder_name] = []
        pm.save_passwords(passwords)
        print(localization.translate("folder_created_success"))
    input(localization.translate("press_enter"))

def edit_folder():
    global session
    passwords = pm.load_passwords()
    if session not in passwords:
        print(localization.translate("no_folders_available"))
        input(localization.translate("press_enter"))
        return

    folders = list(passwords[session]["folders"].keys())
    if not folders:
        print(localization.translate("no_folders_available"))
        input(localization.translate("press_enter"))
        return

    print(localization.translate("available_folders"))
    for i, folder in enumerate(folders, 1):
        print(f"{i}. {folder}")
    
    folder_option = input(localization.translate("select_folder"))
    if folder_option.isdigit() and 1 <= int(folder_option) <= len(folders):
        folder = folders[int(folder_option) - 1]
        new_name = input(localization.translate("enter_new_folder_name"))
        if new_name in passwords[session]["folders"]:
            print(localization.translate("folder_already_exists"))
        else:
            passwords[session]["folders"][new_name] = passwords[session]["folders"].pop(folder)
            pm.save_passwords(passwords)
            print(localization.translate("folder_renamed_success"))
    else:
        print(localization.translate("invalid_option"))
    input(localization.translate("press_enter"))

def delete_folder():
    global session
    passwords = pm.load_passwords()
    if session not in passwords:
        print(localization.translate("no_folders_available"))
        input(localization.translate("press_enter"))
        return

    folders = list(passwords[session]["folders"].keys())
    if not folders:
        print(localization.translate("no_folders_available"))
        input(localization.translate("press_enter"))
        return

    print(localization.translate("available_folders"))
    for i, folder in enumerate(folders, 1):
        print(f"{i}. {folder}")
    
    folder_option = input(localization.translate("select_folder"))
    if folder_option.isdigit() and 1 <= int(folder_option) <= len(folders):
        folder = folders[int(folder_option) - 1]
        confirm = input(localization.translate("confirm_delete_folder"))
        if confirm.lower() == 'y':
            del passwords[session]["folders"][folder]
            pm.save_passwords(passwords)
            print(localization.translate("folder_deleted_success"))
        else:
            print(localization.translate("delete_cancelled"))
    else:
        print(localization.translate("invalid_option"))
    input(localization.translate("press_enter"))

def manage_folders():
    global session
    while True:
        clear_screen()
        print(f"\n1. {localization.translate('create_folder')}\n2. {localization.translate('edit_folder')}\n3. {localization.translate('delete_folder')}\n4. {localization.translate('back_to_menu')}")
        option = input(localization.translate("enter_option"))
        clear_screen()
        if option == '1':
            create_folder()
        elif option == '2':
            edit_folder()
        elif option == '3':
            delete_folder()
        elif option == '4':
            return
        else:
            print(localization.translate("invalid_option"))
            input(localization.translate("press_enter"))

def main():
    global session
    global localization
    session = load_session()

    # Verificar si la sesión es válida
    users = auth.load_users()
    if session not in users:
        session = None

    while True:
        clear_screen()
        if not session:
            print(f"\n1. {localization.translate('register')}\n2. {localization.translate('login')}\n3. {localization.translate('settings')}\n4. {localization.translate('exit')}")
            option = input(localization.translate("enter_option"))
            clear_screen()
            if option == '1':
                auth.register_user(localization)
            elif option == '2':
                session = auth.login(localization)
                if session:
                    save_session(session)
                    display_menu()
            elif option == '3':
                change_language()
            elif option == '4':
                print(localization.translate("welcome"))
                break
        else:
            display_menu()

if __name__ == "__main__":
    main()