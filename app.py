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

# Función utilizada para iniciar la aplicación en la pantalla de bienvenida
@app.route('/')
def inicio():
    return render_template('bienvenida.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """
    DocString: Función utilizada para manejar la pantalla de registro, con sus métodos GET y POST,

    """

    if request.method == 'POST': # Verificar que el tipo de método utilizado en la pantalla especificamente en el formulario sea POST
        # Sección para extraer los datos del formulario
        nombre = request.form.get('username')  
        correo = request.form.get('email')
        password = request.form.get('password')

        # Sección para comprobar si el correo ya existe, ya que solo se puede tener una única cuenta
        if Usuario.query.filter_by(email=correo).first():
            flash('El correo ya existe.')
            return redirect(url_for('registro'))
        
        pw_hash = generate_password_hash(password) # Generar contraseña segura con Werkzeug
        nuevo_user = Usuario(username=nombre,email=correo, password_hash=pw_hash) # Para crear un nuevo usuario en la base de datos usando la clase Usuario
        db.session.add(nuevo_user)
        db.session.commit()

        flash('¡Registro exitoso! Ya puedes ingresar')
        return redirect(url_for('login'))
    return render_template('registro.html') # Renderiza todo el HTML que se encuentra en registro.htmls

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Docstring: Función utilizada para renderizar 
    y mantener la lógica de la funcionalidad login 
    o inicio de sesión.
    """
    if request.method == 'POST': # Comprobar el tipo de método HTTP.
        correo = request.form.get('email') # Extraer del formulario de inicio de sesión los datos correo y password que ingresa el usuario
        password = request.form.get('password')
        user = Usuario.query.filter_by(email=correo).first() # se utiliza esta funcionalidad para extraer este dato de la base de datos

        if user and check_password_hash(user.password_hash, password): # Verificación de contraseña
            return f"<h1>Bienvenido, {user.username} </h1><a href='/'>Volver</a>"
        
        flash('Correo o contraseña incorrectos') # Si la contraseña o el inicio de sesión son incorrectos entonces se mandará este mensaje a la plantilla base.html para que lo renderice y así generar un mensaje de error.
    return render_template('login.html')

if __name__ == '__main__': # Esto se utiliza para correr la aplicación llamando el método principal y además, sirve para que cada vez que se corra se cree lo de la base de datos
    with app.app_context():
        db.create_all()
    app.run(debug=True)

