from flask import Flask, request, jsonify
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)  # Habilitar CORS para toda la 

CORS(app, resources={
    r"*": {"origins": ["http://127.0.0.1:8000"]}  # Allow specific origins
})

# Base de datos ficticia de usuarios (solo para propósitos de demostración)
usuarios = {
    "usuario1": "password1",
    "usuario2": "password2"
}

# Base de datos ficticia de tokens de acceso (solo para propósitos de demostración)
tokens = {}

# Datos guardados en JSON (solo para propósitos de demostración)
datos_guardados = {}

# Método de inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    usuario = datos.get('usuario')
    contraseña = datos.get('contraseña')

    if usuario in usuarios and usuarios[usuario] == contraseña:
        # Generar token de acceso (puede usar bibliotecas como JWT para generar tokens más seguros)
        token = f"token_{usuario}"
        tokens[token] = usuario
        return jsonify({"token": token}), 200
    else:
        return jsonify({"mensaje": "Inicio de sesión fallido"}), 401

# Método para verificar el token de acceso
def verificar_token(token):
    return token in tokens

# Métodos protegidos que requieren autenticación
@app.route('/datos_privados', methods=['GET'])
def datos_privados():
    token = request.headers.get('Authorization')
    if verificar_token(token):
        # Lógica para mostrar los datos introducidos
        return jsonify({"mensaje": "Estos son los datos privados ..."}), 200
    else:
        return jsonify({"mensaje": "Acceso no autorizado"}), 403

@app.route('/actualizar_datos', methods=['PUT'])
def actualizar_datos():
    token = request.headers.get('Authorization')
    if verificar_token(token):
        # Lógica para actualizar los datos
        datos = request.get_json()
        datos_guardados.update(datos)  # Guardar los datos introducidos en el JSON
        return jsonify({"mensaje": "Datos actualizados correctamente ..."}), 200
    else:
        return jsonify({"mensaje": "Acceso no autorizado"}), 403

@app.route('/eliminar_cuenta', methods=['DELETE'])
def eliminar_cuenta():
    token = request.headers.get('Authorization')
    if verificar_token(token):
        # Lógica para eliminar la cuenta
        return jsonify({"mensaje": "Cuenta eliminada correctamente ..."}), 200
    else:
        return jsonify({"mensaje": "Acceso no autorizado"}), 403

@app.route('/exportar_csv', methods=['POST'])
def exportar_csv():
    token = request.headers.get('Authorization')
    if verificar_token(token):
        # Guardar los datos en un archivo CSV
        with open('datos.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['clave', 'valor'])
            writer.writeheader()
            for clave, valor in datos_guardados.items():
                writer.writerow({'clave': clave, 'valor': valor})
        return jsonify({"mensaje": "Datos exportados correctamente ..."}), 200
    else:
        return jsonify({"mensaje": "Acceso no autorizado"}), 403

if __name__ == '__main__':
    app.run(port=8000)
    #app.run(debug=True)

