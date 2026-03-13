# Llamado a librerías de Python, como Flask, SQLAlchemy y parte de werkzeug

from flask import Flask, render_template, request, redirect, url_for, flash # Esta librería la utilizo para desarrollar la aplicación en términos generales
from flask_sqlalchemy import SQLAlchemy # Esta me sirve para conectar y hacer todo con la base de datos
from werkzeug.security import generate_password_hash, check_password_hash # Esta me sirve para la seguridad con las contraseñas DOCUMENTACIÓN EN: https://werkzeug.palletsprojects.com/en/stable/ 

app = Flask(__name__) # Instancia de la librería principal 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:!Jalbrin4405@localhost/proyecto_flask' # Para desarrollar la conexión con la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hola_como_tan_muchachos'

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

# Función utilizada para
@app.route('/')
def inicio():
    return render_template('bienvenida.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('username')
        correo = request.form.get('email')
        password = request.form.get('password')

        if Usuario.query.filter_by(email=correo).first():
            flash('El correo ya existe.')
            return redirect(url_for('registro'))
        
        pw_hash = generate_password_hash(password)
        nuevo_user = Usuario(username=nombre,email=correo, password_hash=pw_hash)
        db.session.add(nuevo_user)
        db.session.commit()

        flash('¡Registro exitoso! Ya puedes ingresar')
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('email')
        password = request.form.get('password')
        user = Usuario.query.filter_by(email=correo).first()

        if user and check_password_hash(user.password_hash, password):
            return f"<h1>Bienvenido, {user.username} </h1><a href='/'>Volver</a>"
        
        flash('Correo o contraseña incorrectos')
    return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

