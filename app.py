from flask import Flask, render_template, request, jsonify
from core.validador import Validador

app = Flask(__name__)
validador = Validador()

@app.route("/", methods=["GET"]) 
def index():
    return render_template("index.html")

@app.route("/normalizar", methods=["POST", "GET"])
def normalizar():
    if request.method == "GET":
        return jsonify({"error": "No se puede acceder a esta ruta con GET"}), 400
    nombre = request.form.get("nombre")
    apellido = request.form.get("apellido")
    nombre_normalizado = validador.normalizar_cadena(nombre)
    apellido_normalizado = validador.normalizar_cadena(apellido)
    return jsonify({ "apellido": apellido_normalizado, "nombre": nombre_normalizado})

@app.route("/normalizar/<cadena>", methods=["POST"])
def normalizarUrl(cadena):
    nombre = cadena.split(",")[0]
    apellido = cadena.split(",")[1]
    nombre_normalizado = validador.normalizar_cadena(nombre)
    apellido_normalizado = validador.normalizar_cadena(apellido)
    return jsonify({ "apellido": apellido_normalizado, "nombre": nombre_normalizado})

@app.route("/comparar", methods=["POST", "GET"])
def comparar():
    if request.method == "GET":
        return jsonify({"error": "No se puede acceder a esta ruta con GET"}), 400
    nombre = request.form.get("nombre")
    apellido = request.form.get("apellido")
    nombre_completo_nosis = request.form.get("nombre_completo_nosis")
    resultado = validador.comparador_final(nombre, apellido, nombre_completo_nosis)
    porcentaje = round(resultado, 2)
    resultado = True if resultado >= 85.0 else False
    return jsonify({"resultado": resultado, "indice_similitud": porcentaje })

if __name__ == "__main__":
    app.run(debug=True)