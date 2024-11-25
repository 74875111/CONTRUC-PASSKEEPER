from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Definición de la base
Base = declarative_base()

# Tabla de usuarios
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    language = Column(String, nullable=True)
    
    # Relación con contraseñas (uno-a-muchos)
    passwords = relationship("Password", back_populates="user")

# Tabla de categorías
class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    
    # Relación con contraseñas (uno-a-muchos)
    passwords = relationship("Password", back_populates="category")

# Tabla de contraseñas
class Password(Base):
    __tablename__ = 'passwords'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))  # Relación con usuarios
    category_id = Column(Integer, ForeignKey('categories.id'))  # Relación con categorías
    last_changed = Column(DateTime, default=datetime.utcnow)
    
    # Relación con usuarios y categorías
    user = relationship("User", back_populates="passwords")
    category = relationship("Category", back_populates="passwords")

# Tabla de historial de cambios de contraseñas
class PasswordChangeHistory(Base):
    __tablename__ = 'password_change_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    password_id = Column(Integer, ForeignKey('passwords.id'))  # Relación con contraseñas
    changed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación con contraseñas
    password = relationship("Password")

# Crear la base de datos
engine = create_engine('sqlite:///password_manager.db')
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

# Insertar datos
def insert_example_data():
    # Categorías
    category_social = Category(name="Redes Sociales")
    category_banks = Category(name="Cuentas Bancarias")
    category_emails = Category(name="Correos Electrónicos")

    # Usuarios
    users = [
        User(username="JuanPerez", email="juan.perez@example.com", language="es"),
        User(username="MariaLopez", email="maria.lopez@example.com", language="es"),
        User(username="CarlosGomez", email="carlos.gomez@example.com", language="es"),
        User(username="AnaMartinez", email="ana.martinez@example.com", language="es"),
        User(username="LuisTorres", email="luis.torres@example.com", language="es"),
        User(username="SofiaHernandez", email="sofia.hernandez@example.com", language="es"),
        User(username="PedroGarcia", email="pedro.garcia@example.com", language="es"),
        User(username="LuciaFernandez", email="lucia.fernandez@example.com", language="es"),
        User(username="MiguelDiaz", email="miguel.diaz@example.com", language="es"),
        User(username="ElenaRuiz", email="elena.ruiz@example.com", language="es"),
    ]

    # Contraseñas
    passwords = [
        Password(name="Facebook", password="JuanPerez123", user=users[0], category=category_social),
        Password(name="Gmail", password="Maria123Lopez", user=users[1], category=category_emails),
        Password(name="Banco Central", password="CarlosBank456", user=users[2], category=category_banks),
        Password(name="Instagram", password="AnaInsta789", user=users[3], category=category_social),
        Password(name="Twitter", password="LuisTw123", user=users[4], category=category_social),
        Password(name="Yahoo Mail", password="SofiaYahoo456", user=users[5], category=category_emails),
        Password(name="Banco Nacional", password="PedroBank789", user=users[6], category=category_banks),
        Password(name="Hotmail", password="LuciaHotmail123", user=users[7], category=category_emails),
        Password(name="LinkedIn", password="MiguelLinked456", user=users[8], category=category_social),
        Password(name="PayPal", password="ElenaPay789", user=users[9], category=category_banks),
    ]

    # Insertar datos en la base de datos
    session.add_all([category_social, category_banks, category_emails] + users + passwords)
    session.commit()

    print("10 usuarios y sus contraseñas insertados correctamente.")

insert_example_data()
