from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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

# Crear el modelo de la tabla 'productos'
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Producto {self.nombre}>'

# Ruta para la página principal
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

# Ruta para la página principal después del inicio de sesión (ajusta según tu diseño)
@app.route('/pantallainicio')
def pantallainicio():
    return render_template('pantallainicio.html')  # Asegúrate de que este archivo exista

# Ruta para ver productos
@app.route('/productos')
def productos():
    return render_template('productos.html')

# Ruta para agregar un producto
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()  # Recibe los datos en formato JSON
    nombre = data['name']
    categoria = data['category']

    nuevo_producto = Producto(nombre=nombre, categoria=categoria)

    try:
        db.session.add(nuevo_producto)
        db.session.commit()
        return {'message': 'Producto agregado exitosamente'}, 201
    except Exception as e:
        db.session.rollback()
        return {'message': f'Error al agregar el producto: {str(e)}'}, 500

# Ruta para editar un producto
@app.route('/edit_product/<int:id>', methods=['PUT'])
def edit_product(id):
    data = request.get_json()
    nombre = data['name']
    categoria = data['category']

    producto = Producto.query.get(id)
    if producto:
        producto.nombre = nombre
        producto.categoria = categoria
        db.session.commit()
        return {'message': 'Producto actualizado exitosamente'}, 200
    return {'message': 'Producto no encontrado'}, 404

# Ruta para eliminar un producto
@app.route('/delete_product/<int:id>', methods=['DELETE'])
def delete_product(id):
    producto = Producto.query.get(id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
        return {'message': 'Producto eliminado exitosamente'}, 200
    return {'message': 'Producto no encontrado'}, 404

# Ruta para obtener todos los productos
@app.route('/get_products', methods=['GET'])
def get_products():
    productos = Producto.query.all()
    product_list = [{"id": p.id, "name": p.nombre, "category": p.categoria} for p in productos]
    return {"products": product_list}

# Iniciar la app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear las tablas en la base de datos si aún no existen
        app.run(debug=True, port=5000)

        

