from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
from werkzeug.security import check_password_hash 
from config import config
 
app = Flask(__name__)
app.config.from_object(config['development'])
CORS(app, origins=["http://localhost:4200"])

CORS(app, resources={r"/admin/*": {"origins": "http://localhost:4200"}})
CORS(app, resources={r"/usuariosr/*": {"origins": "http://localhost:4200"}})
CORS(app, resources={r"/login/*": {"origins": "http://localhost:4200"}})

conexion = MySQL(app)

#--------------------------usuarios------------------------------------
@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM admin ORDER BY nombre ASC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = []
        for fila in datos:
            usuario = {
                "id": fila[0], 
                "nombre": fila[1], 
                "correo": fila[2], 
                "contrasena": fila[3],
                "rol": fila[4]
            }
            usuarios.append(usuario)
        return jsonify({'usuarios': usuarios, 'mensaje': 'Usuarios listados', "exito": True})
    except Exception as ex:
        return jsonify({"mensaje": "Error: {}".format(ex), 'exito': False})
 
def pagina_no_encontrada(error):
    return jsonify({"mensaje": "Error BD: {}".format(error), 'exito': False})
 
def leer_usuario_bd(id_usuario):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, nombre, correo, contrasena, rol FROM admin WHERE id = %s"
        cursor.execute(sql, (id_usuario,))
        datos = cursor.fetchone()
        if datos != None:
            usuario = {
                'id': datos[0], 
                'nombre': datos[1], 
                'correo': datos[2], 
                'contrasena': datos[3],
                'rol': datos[4]
            }
            return usuario
        else:
            return None
    except Exception as ex:
        raise ex
 
@app.route('/usuarios/<id_usuario>', methods=['GET'])
def leer_usuario(id_usuario):
    try:
        usuario = leer_usuario_bd(id_usuario)
        if usuario != None:
            return jsonify({'usuario': usuario, 'mensaje': "Usuario encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
 
@app.route('/usuarios', methods=['POST'])
def registrar_usuario():
    try:
        usuario = leer_usuario_bd(request.json['id'])
        if usuario != None:
            return jsonify({'mensaje': "Usuario ya existe, no se puede duplicar.", 'exito': False})
        else:
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO admin (id, nombre, correo, contrasena, rol)
            VALUES (%s, %s, %s, %s, %s)"""
            valores = (
                request.json['id'],
                request.json['nombre'],
                request.json['correo'],
                request.json['contrasena'],
                request.json['rol']
            )
            cursor.execute(sql, valores)
            conexion.connection.commit()
            return jsonify({'mensaje': "Usuario registrado.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error: {}".format(ex), 'exito': False})
 
#actualizar
@app.route('/usuarios/<id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    try:
        usuario = leer_usuario_bd(id_usuario)
        if usuario != None:
            cursor = conexion.connection.cursor()
            sql = """UPDATE admin SET nombre = %s, correo = %s, contrasena = %s, rol = %s
            WHERE id = %s"""
            valores = (
                request.json['nombre'],
                request.json['correo'],
                request.json['contrasena'],
                request.json['rol'],
                id_usuario
            )
            cursor.execute(sql, valores)
            conexion.connection.commit()
            return jsonify({'mensaje': "Usuario actualizado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error: {}".format(ex), 'exito': False})
 
@app.route('/usuarios/<id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    try:
        usuario = leer_usuario_bd(id_usuario)
        if usuario != None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM admin WHERE id = %s"
            cursor.execute(sql, (id_usuario,))
            conexion.connection.commit()
            return jsonify({'mensaje': "Usuario eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error: {}".format(ex), 'exito': False})
#-----------------------aqui finliza el de usuarios-------------------------

# login-------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()#codigo------------------------------------------------------------>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        correo = data['correo']
        contrasena = data['contrasena']
       
        cursor = conexion.connection.cursor()
        sql = "SELECT id, nombre, correo, contrasena, rol FROM admin WHERE correo = %s AND contrasena = %s"
        cursor.execute(sql, (correo, contrasena))
       
        datos = cursor.fetchone()
        if datos != None:
            usuario = {
                'id': datos[0],
                'nombre': datos[1],
                'correo': datos[2],
                'contrasena': datos[3],
                'rol': datos[4]
            }
            return jsonify({
                'usuario': usuario,
                'mensaje': "Login exitoso",
                'exito': True
            })
        else:
            return jsonify({
                'mensaje': "Usuario o contraseña incorrectos",
                'exito': False
            })
           
    except Exception as ex:
        return jsonify({
            'mensaje': "Error: {}".format(ex),
            'exito': False
        })

#------------------------------aqui finaliza login----------------------------------



#----------------------------usuario registrados------------------------------------
# Listar todos los usuarios
@app.route("/usuariosr", methods=["GET"])
def listar_usuariosr():
    try:
        cur = conexion.connection.cursor()
        cur.execute("USE game")
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM usuariosr ORDER BY userName ASC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuariosr = []
        for fila in datos:
            usuarior = {
                "userName": fila[0],
                "email": fila[1],
                "password": fila[2]
            }
            usuariosr.append(usuarior)
        return jsonify({'usuariosr': usuariosr, 'mensaje': 'Usuarios listados', "exito": True})
    except Exception as ex:
        return jsonify({"mensaje": "Error: {}".format(ex), 'exito': False})
 
# Función auxiliar para leer usuario
def leer_usuarior_bd(userName):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT userName, email, password FROM usuariosr WHERE userName = %s"
        cursor.execute(sql, (userName,))
        datos = cursor.fetchone()
        if datos != None:
            usuarior = {
                "userName": datos[0],
                "email": datos[1],
                "password": datos[2]
            }
            return usuarior
        else:
            return None
    except Exception as ex:
        raise ex
 
# Leer un usuario específico
@app.route('/usuariosr/<userName>', methods=['GET'])
def leer_usuarior(userName):
    try:
        usuarior = leer_usuarior_bd(userName)
        if usuarior != None:
            return jsonify({'usuarior': usuarior, 'mensaje': "Usuario encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
 
# Registrar nuevo usuario
@app.route('/usuariosr', methods=['POST'])
def registrar_usuarior():
    try:
        cur = conexion.connection.cursor()
        cur.execute("USE game")
        usuarior = leer_usuarior_bd(request.json['userName'])
        if usuarior != None:
            return jsonify({'mensaje': "Usuario ya existe, no se puede duplicar.", 'exito': False})
        else:
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO usuariosr (userName, email, password) 
                    VALUES (%s, %s, %s)"""
            valores = (
                request.json['userName'],
                request.json['email'],
                request.json['password']
            )
            cursor.execute(sql, valores)
            conexion.connection.commit()
            return jsonify({'mensaje': "Usuario registrado.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error: {}".format(ex), 'exito': False})
 
# Actualizar usuario
@app.route('/usuariosr/<userName>', methods=['PUT'])
def actualizar_usuarior(userName):
    try:
        cur = conexion.connection.cursor()
        cur.execute("USE game")
        usuarior = leer_usuarior_bd(userName)
        if usuarior != None:
            cursor = conexion.connection.cursor()
            sql = """UPDATE usuariosr 
                    SET email = %s, password = %s 
                    WHERE userName = %s"""
            valores = (
                request.json['email'],
                request.json['password'],
                userName
            )
            cursor.execute(sql, valores)
            conexion.connection.commit()
            return jsonify({'mensaje': "Usuario actualizado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error: {}".format(ex), 'exito': False})
 
# Eliminar usuario
# Eliminar usuario
@app.route('/usuariosr/<userName>', methods=['DELETE'])
def eliminar_usuarior(userName):
    try:
        cur = conexion.connection.cursor()
        cur.execute("USE game")
        # Verificar si el usuario existe
        usuarior = leer_usuarior_bd(userName)
        if usuarior is not None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM usuariosr WHERE userName = %s"
            cursor.execute(sql, (userName,))
            conexion.connection.commit()
            cursor.close()  # Cerrar el cursor después de usarlo
            return jsonify({'mensaje': "Usuario eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

# Manejador de errores
def pagina_no_encontrada(error):
    return jsonify({"mensaje": "Error BD: {}".format(error), 'exito': False})

#-----------------------------------------------------------------------------------



if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(400, pagina_no_encontrada)
    app.run()
