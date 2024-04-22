from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

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
def historial():
    return render_template("historialMedico.html")

@app.route("/consultas")
def consultas():
    return render_template("consultasEvaluaciones.html")