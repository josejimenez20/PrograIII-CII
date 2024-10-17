from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')

app.secret_key = 'mi_clave_secreta'  # Necesario para usar flash messages

# Configuración de SQLite como base de datos local
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///salon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Crear el modelo de la tabla 'usuarios'
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)


# Cargar página de inicio
@app.route('/')
def index():
    return render_template('inicio.html')

# Ruta para el formulario de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        email = request.form['email']
        contrasena = request.form['password']  

        nuevo_usuario = Usuario(nombre=nombre, apellido=apellido, telefono=telefono, direccion=direccion, email=email, contrasena=contrasena)

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('iniciar_sesion'))  # Redirigir a la página de inicio de sesión
        except Exception as e:
            flash(f'Error al registrar el usuario: {str(e)}', 'danger')

    return render_template('registro.html')

# Ruta para el inicio de sesión
@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['password']
        
        usuario = Usuario.query.filter_by(email=email, contrasena=contrasena).first()
        
        if usuario:
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('pantallainicio'))  # Redirigir a la página principal
        else:
            flash('Email o contraseña incorrectos', 'danger')

    return render_template('login.html')

# Ruta para ver usuarios
@app.route('/ver_usuarios')
def ver_usuarios():
    usuarios = Usuario.query.all()
    return render_template('ver_usuarios.html', usuarios=usuarios)

# Ruta para la página principal después del inicio de sesión (ajusta según tu diseño)
@app.route('/pantallainicio')
def pantallainicio():
    return render_template('pantallainicio.html')  # Asegúrate de que este archivo exista

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear las tablas en la base de datos si aún no existen
        app.run(debug=True, port=5000)
