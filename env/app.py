from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

# Configurar la conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gabineteambar"
)
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Se utiliza para firmar las sesiones

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"]
    contrasena = request.form["contrasena"]

    # Verificar si las credenciales son válidas en la tabla admingeneral
    cursor = db.cursor()
    cursor.execute("SELECT * FROM admingeneral WHERE usuarioAdmin = %s AND password = %s", (usuario, contrasena))
    admin = cursor.fetchone()
    cursor.close()

    # Verificar si las credenciales son válidas en la tabla usuarios
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nombreUsuario = %s AND password = %s", (usuario, contrasena))
    usuario_normal = cursor.fetchone()
    cursor.close()

    # Si las credenciales son válidas, redirigir a la página de bienvenida y establecer la sesión
    if admin:
        session['logged_in'] = True
        session['tipo_usuario'] = 'admin'  # Establecer el tipo de usuario como admin
        return redirect(url_for("welcome"))
    elif usuario_normal:
        session['logged_in'] = True
        session['tipo_usuario'] = 'usuario_normal'  # Establecer el tipo de usuario como usuario normal
        return redirect(url_for("welcome"))
    else:
        # Credenciales inválidas, volver a cargar la página de inicio de sesión con un mensaje de error
        return render_template("index.html", mensaje_error="Usuario o contraseña incorrectos")



@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route("/welcome")
@login_required
def welcome():
    tipo_usuario = session.get('tipo_usuario')
    return render_template("welcome.html", tipo_usuario=tipo_usuario)


@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "GET":
        return render_template("contacto.html")
    else:
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        mensaje = request.form["mensaje"]

        # Procesar la información del formulario

        return render_template("contacto.html", mensaje_enviado=True)

@app.route("/blog")
def blog():
    entradas_blog = [
        {"titulo": "Entrada 1", "contenido": "Texto de la entrada 1"},
        {"titulo": "Entrada 2", "contenido": "Texto de la entrada 2"},
    ]

    return render_template("blog.html", entradas_blog=entradas_blog)

@app.route("/historial")
@login_required
def historial():
    return render_template("historialMedico.html")

@app.route("/pacientes")
@login_required
def pacientes():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM paciente")
    pacientes = cursor.fetchall()
    cursor.close()
    return render_template("pacientes.html", pacientes=pacientes)

@app.route("/contratar")
@login_required
def contratar():
    tipo_usuario = session.get('tipo_usuario')
    cursor = db.cursor(dictionary=True)  # Usar dictionary=True para obtener un diccionario por fila
    cursor.execute("SELECT * FROM personal")
    personales = cursor.fetchall()
    cursor.close()
    return render_template("contratarPersonal.html", personales=personales, tipo_usuario=tipo_usuario)


@app.route("/consultas")
@login_required
def consultas():
    return render_template("consultasEvaluaciones.html")

@app.route("/capacitacion")
@login_required
def capacitacion():
    return render_template("planificarCapacitacion.html")

@app.route("/gestioAdmin")
def gestioAdmin():
    return render_template("gestionAdministrativa.html")
