import sqlite3
import bcrypt

DB = "database.db"

usuarios = [
    ("Hector", "Vergara", "user"),
    ("Alex", "Revuelta", "user"),
    ("Jaime", "Grez", "user"),
    ("Jonathan", "Bravo", "user"),
    ("Jonathan", "Lozano", "user"),
    ("Carlos", "Perales", "user"),
    ("Elthon", "Rivas", "user"),
    ("Admin", "App", "admin"),
    ("Prueba", "Test", "user"),
]

# Generar usuarios y contraseñas seguras
import secrets
import string

def generar_contrasena(longitud=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(longitud))

conn = sqlite3.connect(DB)
c = conn.cursor()

# Crear tabla usuarios
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    usuario TEXT UNIQUE NOT NULL,
    contraseña TEXT NOT NULL,
    rol TEXT DEFAULT 'user'
)''')

# Crear tabla evaluacion
c.execute('''CREATE TABLE IF NOT EXISTS evaluacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    proveedor TEXT NOT NULL,
    bloque TEXT NOT NULL,
    pregunta TEXT NOT NULL,
    puntuacion_cuantitativa INTEGER NOT NULL,
    puntuacion_cualitativa TEXT NOT NULL
)''')


# Insertar usuarios
credenciales = []
for nombre, apellido, rol in usuarios:
    usuario = f"{nombre.lower()}.{apellido.lower()}"
    contrasena = generar_contrasena()
    hash_pw = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt()).decode()
    try:
        c.execute("INSERT INTO usuarios (nombre, apellido, usuario, contraseña, rol) VALUES (?, ?, ?, ?, ?)",
                  (nombre, apellido, usuario, hash_pw, rol))
        credenciales.append((usuario, nombre, apellido, rol, contrasena))
        print(f"Usuario: {usuario} | Contraseña: {contrasena} | Rol: {rol}")
    except sqlite3.IntegrityError:
        print(f"Usuario {usuario} ya existe.")

# Guardar credenciales en archivo
with open("USUARIOS_INICIALES.md", "w", encoding="utf-8") as f:
    f.write("# Usuarios iniciales y contraseñas\n\n")
    f.write("| Usuario         | Nombre   | Apellido   | Rol    | Contraseña           |\n")
    f.write("|----------------|----------|------------|--------|----------------------|\n")
    for usuario, nombre, apellido, rol, contrasena in credenciales:
        f.write(f"| {usuario:<14} | {nombre:<8} | {apellido:<10} | {rol:<6} | {contrasena:<20} |\n")
    f.write("\n> Este archivo se genera automáticamente al crear los usuarios iniciales.\n")

conn.commit()
conn.close()
print("Base de datos inicializada.")
