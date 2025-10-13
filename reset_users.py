from app import app
from models import db, Usuario
from dotenv import load_dotenv
import os

load_dotenv("credenciales.env")

def reset_users():
    with app.app_context():
        # Elimina todos los usuarios
        Usuario.query.delete()
        db.session.commit()
        print("🗑️ Todos los usuarios eliminados.")

        # Crea de nuevo desde .env
        for i in [("USER1","PASS1"),("USER2","PASS2")]:
            username, password = os.getenv(i[0]), os.getenv(i[1])
            if username and password:
                user = Usuario(nombre=username.lower())
                user.establecer_contraseña(password)
                db.session.add(user)
                print(f"✅ Usuario '{username}' creado.")
        db.session.commit()

if __name__ == "__main__":
    reset_users()
