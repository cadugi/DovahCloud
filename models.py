from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# Relación muchos-a-muchos
archivo_etiqueta = db.Table('archivo_etiqueta',
    db.Column('archivo_id', db.Integer, db.ForeignKey('archivo.id'), primary_key=True),
    db.Column('etiqueta_id', db.Integer, db.ForeignKey('etiqueta.id'), primary_key=True)
)

# Tabla de favoritos
favoritos = db.Table('favoritos',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id')),
    db.Column('archivo_id', db.Integer, db.ForeignKey('archivo.id'))
)

# Tabla de playlist
playlist_archivo = db.Table('playlist_archivo',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')),
    db.Column('archivo_id', db.Integer, db.ForeignKey('archivo.id'))
)

bloc_compartido = db.Table('bloc_compartido',
    db.Column('bloc_id', db.Integer, db.ForeignKey('bloc.id')),
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'))
)

# Tabla de archivos
class Archivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    ruta = db.Column(db.Text)
    tipo = db.Column(db.String(100))
    tamaño = db.Column(db.BigInteger)
    fecha_subida = db.Column(db.DateTime, server_default=db.func.now())
    es_privado = db.Column(db.Boolean, default=False)
    descripcion = db.Column(db.Text, nullable=True)
    hash_archivo = db.Column(db.String(64), nullable=True)
    fecha_eliminado = db.Column(db.DateTime, nullable=True)  # 🗑️ Si tiene valor, está en papelera
    etiquetas = db.relationship('Etiqueta', secondary=archivo_etiqueta, back_populates='archivos')

# Tabla de etiquetas
class Etiqueta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), unique=True, nullable=False)
    es_privada = db.Column(db.Boolean, default=False)
    archivos = db.relationship('Archivo', secondary=archivo_etiqueta, back_populates='etiquetas')

# Tabla de usuarios
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(32), unique=True, nullable=False)
    contraseña_hash = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(128), default='default_avatar.png')  # archivo en /static/avatars/
    acceso_privado = db.Column(db.Boolean, default=False)
    favoritos = db.relationship('Archivo', secondary=favoritos, backref='usuarios_que_lo_favoritan')
    es_admin = db.Column(db.Boolean, default=False)

    def establecer_contraseña(self, contraseña_clara):
        self.contraseña_hash = generate_password_hash(contraseña_clara)

    def verificar_contraseña(self, contraseña_clara):
        return check_password_hash(self.contraseña_hash, contraseña_clara)


class CertificadoDigital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    numero_serie = db.Column(db.String(128), unique=True, nullable=False)
    alias = db.Column(db.String(128), nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = relationship('Usuario', backref=db.backref('certificados_digitales', lazy=True))

    def establecer_clave(self, clave_privada):
        self.password_hash = generate_password_hash(clave_privada)

    def verificar_clave(self, clave_privada):
        return check_password_hash(self.password_hash, clave_privada)

# Tabla de playlist
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    archivos = db.relationship('Archivo', secondary='playlist_archivo', backref='playlists')

# Tabla de Notas
class Bloc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.Text, default='')
    privado = db.Column(db.Boolean, default=True)
    publico = db.Column(db.Boolean, default=False)
    fecha_creado = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizado = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    autor = relationship('Usuario', backref='blocs')

    invitados = relationship('Usuario', secondary=bloc_compartido, backref='blocs_compartidos')

