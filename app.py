from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de SQLite como base de datos local
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///salon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Cargar página de inicio
@app.route('/')
def index():
    return render_template('registro.html')

# Crear el modelo de la tabla 'usuarios'
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)

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
            return "Usuario registrado exitosamente"
        except Exception as e:
            return f"Error al registrar el usuario: {str(e)}"

    return render_template('registro.html')

@app.route('/ver_usuarios')
def ver_usuarios():
    usuarios = Usuario.query.all()
    return render_template('ver_usuarios.html', usuarios=usuarios)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear las tablas en la base de datos si aún no existen
        app.run(debug=True, port=5000)


    
    
