# Llamado a librerías de Python, como Flask, SQLAlchemy y parte de werkzeug

from flask import Flask, render_template, request, redirect, url_for, flash # Esta librería la utilizo para desarrollar la aplicación en términos generales
from flask_sqlalchemy import SQLAlchemy # Esta me sirve para conectar y hacer todo con la base de datos
from werkzeug.security import generate_password_hash, check_password_hash # Esta me sirve para la seguridad con las contraseñas DOCUMENTACIÓN EN: https://werkzeug.palletsprojects.com/en/stable/ 

app = Flask(__name__) # Instancia de la librería principal 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:' # Para desarrollar la conexión con la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mi_clave_secrecta'

db=SQLAlchemy(app) #Instanciamos para la base de datos pasando como parametro la instancia de la librería principal


class Usuario(db.Model):
    """
    Docstring: clase para desarrollar 
    la estructura que tiene la base 
    de datos en MySQL Workbench.
    """
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email= db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255),nullable=False)

    def __repr__(self):
        return f'<Usuerio {self.username}>'

@app.route('/')
def inicio():
    return render_template('base.html')

