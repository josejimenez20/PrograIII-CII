from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

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

# Modelo para las preguntas y respuestas del chatbot
class ChatbotRespuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.String(255), unique=True, nullable=False)
    respuesta = db.Column(db.Text, nullable=False)

# Modelo de la tabla 'Servicios'
class Servicio(db.Model):
    id_servicio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Numeric(10, 2), nullable=False)

# Modelo de la tabla 'Empleados'
class Empleado(db.Model):
    id_empleado = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    apellido = db.Column(db.String(200), nullable=False)
    cargo = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)

# Modelo de la tabla 'Citas'
class Cita(db.Model):
    id_cita = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_empleado = db.Column(db.Integer, db.ForeignKey('empleado.id_empleado'), nullable=False)
    id_servicio = db.Column(db.Integer, db.ForeignKey('servicio.id_servicio'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    campo = db.Column(db.String(200))  # Campo adicional si lo necesitas

# Modelo de la tabla 'Facturas'
class Factura(db.Model):
    id_factura = db.Column(db.Integer, primary_key=True)
    id_cita = db.Column(db.Integer, db.ForeignKey('cita.id_cita'), nullable=False)
    fecha_emision = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)

# Crear el modelo de la tabla 'Producto'
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)

# Modelo de la tabla 'VentaProducto'
class VentaProducto(db.Model):
    id_venta = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_total = db.Column(db.Numeric(10, 2), nullable=False)

# Modelo de la tabla 'Horarios'
class Horario(db.Model):
    id_horario = db.Column(db.Integer, primary_key=True)
    id_empleado = db.Column(db.Integer, db.ForeignKey('empleado.id_empleado'), nullable=False)
    dia_semana = db.Column(db.Enum('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'), nullable=False)
    hora_ini = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)


# Ruta para la página principal
@app.route('/')
def index():
    return render_template('inicio.html')

# Ruta para poblar la tabla del chatbot con datos iniciales
@app.route('/populate_chatbot', methods=['GET'])
def populate_chatbot():
    datos = [
        {"pregunta": "¿Qué servicios ofrecen?", "respuesta": "Ofrecemos cortes de cabello, manicura, pedicura y tratamientos faciales."},
        {"pregunta": "¿Cuáles son los precios?", "respuesta": "Nuestros precios varían según el servicio. Por ejemplo, un corte de cabello cuesta $20."},
        {"pregunta": "¿Dónde están ubicados?", "respuesta": "Estamos en la calle Principal #123, en el centro de la ciudad."}
    ]

    try:
        for dato in datos:
            nuevo = ChatbotRespuesta(pregunta=dato["pregunta"], respuesta=dato["respuesta"])
            db.session.add(nuevo)
        db.session.commit()
        return "Preguntas y respuestas agregadas exitosamente."
    except Exception as e:
        db.session.rollback()
        return f"Error al poblar la base de datos: {str(e)}"

# Ruta para procesar preguntas del chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    pregunta_usuario = data.get("pregunta", "").lower()

    respuesta = ChatbotRespuesta.query.filter(ChatbotRespuesta.pregunta.ilike(f"%{pregunta_usuario}%")).first()
    
    if respuesta:
        return jsonify({"respuesta": respuesta.respuesta})
    else:
        return jsonify({"respuesta": "Lo siento, no entiendo tu pregunta. ¿Puedes reformularla?"})


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
            flash('Inicio de sesión exitoso', 'success')  # Notificación de éxito
            return redirect(url_for('pantallainicio'))  # Redirige al usuario a la página de inicio
        else:
            flash('Correo o contraseña incorrectos', 'danger')  # Notificación de error

    return render_template('login.html')


# Ruta para la página principal después del inicio de sesión (ajusta según tu diseño)
@app.route('/pantallainicio')
def pantallainicio():
    return render_template('pantallainicio.html')  # Asegúrate de que este archivo exista

# Ruta para ver productos
@app.route('/productos')
def productos():
    return render_template('productos.html')

# Ruta paraver citasservicio
@app.route('/citasservicios')
def citasservicio():
    return render_template('citasservicio.html')

# Ruta paraver servicio
@app.route('/serviccio')
def servicio():
    return render_template('servicio.html')

# Ruta para agregar un producto
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()   
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
    productos = Producto.query.all()  # Consulta todos los productos
    product_list = [{"id": p.id, "name": p.nombre, "category": p.categoria} for p in productos]
    return {"products": product_list}  # Devuelve la lista en formato JSON

@app.route('/carrito')
def carrito():
    return "Página del carrito"

@app.route('/perfil')
def perfil():
    return "Página del perfil"


# Iniciar la app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear las tablas en la base de datos si aún no existen
        app.run(debug=True, port=5000)

        

