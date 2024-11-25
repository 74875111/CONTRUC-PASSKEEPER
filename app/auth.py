import json
import os
import uuid
from dotenv import load_dotenv

DATA_FILE = "data/users.json"

# Cargar las credenciales de correo electrónico desde el archivo .env
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    with open(DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def register_user(localization):
    try:
        users = load_users()
        email = input(localization.translate("enter_email"))
        password = input(localization.translate("enter_password"))
        username = input(localization.translate("enter_username"))

        user_id = str(uuid.uuid4())
        users[user_id] = {
            "password": password,
            "details": {
                "email": email,
                "username": username
            }
        }
        save_users(users)
        print(localization.translate("user_registered_success"))
    except Exception as e:
        print(localization.translate("registration_failed"), str(e))
        input(localization.translate("press_any_key_to_continue"))

def login(localization):
    try:
        users = load_users()
        email = input(localization.translate("enter_email"))
        password = input(localization.translate("enter_password"))

        for user_id, user in users.items():
            if user["details"]["email"] == email and user["password"] == password:
                print(localization.translate("login_success"))
                return user_id  # Devolver el ID del usuario como sesión

        print(localization.translate("login_failed"))
        input(localization.translate("press_any_key_to_continue"))
        return None
    except Exception as e:
        print(localization.translate("login_error"), str(e))
        input(localization.translate("press_any_key_to_continue"))
        return None