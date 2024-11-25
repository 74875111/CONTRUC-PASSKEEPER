import tkinter as tk
from tkinter import ttk, messagebox

# Datos ficticios para simular una base de datos
usuarios = [
    {"id": 1, "nombre": "Alice", "email": "alice@example.com"},
    {"id": 2, "nombre": "Bob", "email": "bob@example.com"},
]

# Función para mostrar los usuarios en la tabla
def mostrar_usuarios():
    for row in tabla_usuarios.get_children():
        tabla_usuarios.delete(row)
    for usuario in usuarios:
        tabla_usuarios.insert("", "end", values=(usuario["id"], usuario["nombre"], usuario["email"]))

# Función para agregar un nuevo usuario
def agregar_usuario():
    nombre = entry_nombre.get()
    email = entry_email.get()
    if nombre and email:
        nuevo_id = max([u["id"] for u in usuarios]) + 1 if usuarios else 1
        usuarios.append({"id": nuevo_id, "nombre": nombre, "email": email})
        mostrar_usuarios()
        entry_nombre.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        messagebox.showinfo("Éxito", "Usuario agregado correctamente.")
    else:
        messagebox.showerror("Error", "Debe completar todos los campos.")

# Función para eliminar un usuario
def eliminar_usuario():
    seleccion = tabla_usuarios.selection()
    if seleccion:
        valores = tabla_usuarios.item(seleccion[0], "values")
        usuario_id = int(valores[0])
        global usuarios
        usuarios = [u for u in usuarios if u["id"] != usuario_id]
        mostrar_usuarios()
        messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
    else:
        messagebox.showerror("Error", "Debe seleccionar un usuario para eliminar.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestión de Usuarios")
root.geometry("600x400")

# Frame para el formulario
frame_formulario = tk.Frame(root, padx=10, pady=10)
frame_formulario.pack(fill="x")

tk.Label(frame_formulario, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(frame_formulario)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_formulario, text="Email:").grid(row=1, column=0, padx=5, pady=5)
entry_email = tk.Entry(frame_formulario)
entry_email.grid(row=1, column=1, padx=5, pady=5)

tk.Button(frame_formulario, text="Agregar Usuario", command=agregar_usuario).grid(row=2, column=0, columnspan=2, pady=10)

# Tabla para mostrar usuarios
frame_tabla = tk.Frame(root, padx=10, pady=10)
frame_tabla.pack(fill="both", expand=True)

columnas = ("ID", "Nombre", "Email")
tabla_usuarios = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
tabla_usuarios.heading("ID", text="ID")
tabla_usuarios.heading("Nombre", text="Nombre")
tabla_usuarios.heading("Email", text="Email")
tabla_usuarios.pack(fill="both", expand=True)

# Botón para eliminar usuario
frame_botones = tk.Frame(root, padx=10, pady=10)
frame_botones.pack(fill="x")

tk.Button(frame_botones, text="Eliminar Usuario", command=eliminar_usuario).pack(side="right", padx=10)

# Mostrar datos iniciales
mostrar_usuarios()

# Ejecutar la aplicación
root.mainloop()
