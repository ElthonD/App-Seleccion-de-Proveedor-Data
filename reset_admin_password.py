import sqlite3
import bcrypt

DB = "database.db"
usuario = "admin.app"
nueva_contra = "Admin2025!!"

hash_pw = bcrypt.hashpw(nueva_contra.encode(), bcrypt.gensalt()).decode()

conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute("UPDATE usuarios SET contraseña = ? WHERE usuario = ?", (hash_pw, usuario))
conn.commit()
conn.close()

print(f"Contraseña de {usuario} actualizada correctamente a: {nueva_contra}")
