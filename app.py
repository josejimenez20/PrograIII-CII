from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from difflib import SequenceMatcher

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
        {"pregunta": "Hola", "respuesta": "¡Hola! ¿En qué puedo ayudarte?"},
        {"pregunta": "Que servicios ofrecen?", "respuesta": "Ofrecemos cortes de cabello, manicura, pedicura y tratamientos faciales."},
        {"pregunta": "Cuales son los precios?", "respuesta": "Nuestros precios varían según el servicio. Puedes consultarlos en nuestra página web."},
        {"pregunta": "Donde estan ubicados?", "respuesta": "Estamos en la calle Principal, en el centro de la ciudad de Jiquilisco."},
        {"pregunta": "Cuales son los horarios de atencion?", "respuesta": "Abrimos de lunes a sábado de 7:00 AM a 5:00 PM."},
        {"pregunta": "Ofrecen servicios a domicilio?", "respuesta": "Sí, ofrecemos servicios a domicilio con un costo adicional dependiendo de la distancia."},
        {"pregunta": "Como puedo agendar una cita?", "respuesta": "Puedes agendar una cita llamándonos al 555-123-456 o a través de nuestra página web."},
        {"pregunta": "Aceptan pagos con tarjeta?", "respuesta": "Sí, aceptamos tarjetas de crédito, débito y también pagos en efectivo."},
        {"pregunta": "Tienen promociones?", "respuesta": "Sí, tenemos descuentos especiales los fines de semana. Por ejemplo, 20% en tratamientos faciales los viernes."},
        {"pregunta": "Cuanto cuesta una manicura?", "respuesta": "Una manicura básica cuesta $15. También ofrecemos paquetes premium."},
        {"pregunta": "Puedo cancelar o reprogramar mi cita?", "respuesta": "Sí, puedes cancelar o reprogramar tu cita llamándonos con al menos 24 horas de anticipación."},
        {"pregunta": "Que productos usan en el salón?", "respuesta": "Usamos productos de alta calidad como L'Oréal, Kerastase y OPI para asegurar los mejores resultados."},
        {"pregunta": "Hay servicios para niños?", "respuesta": "Sí, ofrecemos cortes de cabello para niños a un precio especial."},
        {"pregunta": "Tienen servicio de depilación?", "respuesta": "Sí, ofrecemos depilación con cera y láser."},
        {"pregunta": "Gracias", "respuesta": "Fue un placer ayudarte, si tienes alguna otra pregunta no dudes en preguntar."}
    ]

    try:
        # Aquí verificamos que no se repitan las preguntas en la base de datos antes de insertarlas
        for dato in datos:
            if not ChatbotRespuesta.query.filter_by(pregunta=dato["pregunta"]).first():
                nuevo = ChatbotRespuesta(pregunta=dato["pregunta"], respuesta=dato["respuesta"])
                db.session.add(nuevo)
        db.session.commit()  # Commit para guardar los cambios

        return "Preguntas y respuestas agregadas exitosamente."
    except Exception as e:
        db.session.rollback()  # En caso de error, deshacemos los cambios
        return f"Error al poblar la base de datos: {str(e)}"


# Ruta para procesar preguntas del chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    pregunta_usuario = data.get("pregunta", "").lower().strip()

    # Obtener todas las preguntas de la base de datos
    respuestas = ChatbotRespuesta.query.all()
    preguntas = [{"pregunta": r.pregunta.lower(), "respuesta": r.respuesta} for r in respuestas]

    # Buscar la pregunta más similar
    def encontrar_similar(pregunta_usuario, lista_preguntas):
        similaridad_max = 0
        mejor_respuesta = None
        for item in lista_preguntas:
            similaridad = SequenceMatcher(None, pregunta_usuario, item['pregunta']).ratio()
            if similaridad > similaridad_max:
                similaridad_max = similaridad
                mejor_respuesta = item
        return mejor_respuesta if similaridad_max > 0.6 else None  

    respuesta_similar = encontrar_similar(pregunta_usuario, preguntas)

    # Responder con la respuesta encontrada o un mensaje genérico
    if respuesta_similar:
        return jsonify({"respuesta": respuesta_similar['respuesta']})
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


@app.route('/citasservicios')
def citasservicio():
    return render_template('citasservicio.html')

# Ruta paraver servicio
@app.route('/serviccio')
def servicio():
    return render_template('servicio.html')

@app.route('/perfil')
def perfil():
    return "Página del perfil"


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True, port=5000)

        

