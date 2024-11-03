import mysql.connector
from mysql.connector import errorcode

# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template

# Instalar con pip install flask-cors
from flask_cors import CORS

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time

from datetime import datetime, timedelta

#------------------------------------------------------
#    Función para convertir datos a string
#------------------------------------------------------
def convertir_a_serializable(obj):
    if isinstance(obj, (datetime, timedelta)):
        return str(obj)
    elif isinstance(obj, dict):
        return {k: convertir_a_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convertir_a_serializable(i) for i in obj]
    else:
        return obj

# Creamos un objeto de Flask para usar sus métodos
app = Flask(__name__)  # Podes llamar como quieras, usamos app
CORS(app)  # Esto habilitará CORS para todas las rutas

class Turno:
    # Creo el constructor
    def __init__(self, host, user, password, database):
        """
        Args:
        host (str): dirección del servidor
        user (str): nombre de usuario
        password: contraseña
        database: el nombre de la BD
        """
        # Establecemos la conexión
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        # Creo el cursor
        self.cursor = self.conn.cursor()

        # Intentamos usar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si el error es porque la BD no existe, la creo
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
                self.cursor.execute(f"USE {database}")
            else:
                raise err

        # Creación de la tabla
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS `turnos`(
                                id_turno INT PRIMARY KEY AUTO_INCREMENT,
                                nombre VARCHAR(40) NOT NULL,
                                celular VARCHAR(20) NOT NULL,
                                vehiculo VARCHAR(30) NOT NULL,
                                patente VARCHAR(10) NOT NULL,
                                servicio VARCHAR(200),
                                foto VARCHAR(60),
                                observaciones VARCHAR(60) NULL,
                                fecha DATE NULL,
                                hora TIME NULL);''')
        # Guarda los cambios
        self.conn.commit()

        # Cierra el cursor y abre uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    #----------------------------------
    #    Agregar Turno
    #----------------------------------
    def crear_turno(self, nombre, celular, vehiculo, patente, servicio, foto, observaciones, fecha, hora):
        
        # Convertimos valores de fecha y hora a NULL si son cero
        if fecha == '0' or fecha == '':
            fecha = None
        if hora == '0' or hora == '':
            hora = None

        sql = "INSERT INTO turnos (nombre, celular, vehiculo, patente, servicio, foto, observaciones, fecha, hora) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (nombre, celular, vehiculo, patente, servicio, foto, observaciones, fecha, hora)
        self.cursor.execute(sql, valores)  # Ejecuta
        self.conn.commit()
        return self.cursor.lastrowid  # Nos devuelve la última ID creada

    #-----------------------------------
    #     Consultar Turno
    #-----------------------------------
    def consulta_turno(self, id_turno):
        # Consultamos un turno
        self.cursor.execute(f"SELECT * FROM turnos WHERE id_turno={id_turno}")
        return self.cursor.fetchone()  # Devuelve el registro uno solo

    #-----------------------------------
    #     Modificar Turno
    #-----------------------------------   
    def modificar_turno(self, id_turno, observaciones, fecha, hora):
        sql = "UPDATE turnos SET observaciones=%s, fecha=%s, hora=%s WHERE id_turno=%s"
        valores = (observaciones, fecha, hora, id_turno)
        self.cursor.execute(sql, valores)  # Ejecuta
        self.conn.commit()
        return self.cursor.rowcount > 0  # Cantidad de columnas cambiadas

    #-----------------------------------
    #     Listar Turnos
    #-----------------------------------   
    def listar_turnos(self):
        self.cursor.execute("SELECT id_turno, nombre, celular, vehiculo, patente, servicio, foto, observaciones, DATE_FORMAT(fecha, '%d-%m') AS fecha, hora FROM turnos WHERE fecha >= CURDATE();")
        turnos = self.cursor.fetchall()  # Devuelve todos los resultados
        return turnos

    #-----------------------------------
    #     Listar Nuevas Solicitudes
    #-----------------------------------   
    def listar_solicitudes(self):
        self.cursor.execute("SELECT * FROM turnos WHERE fecha IS NULL;")
        turnos = self.cursor.fetchall()  # Devuelve todos los resultados
        return turnos

    #-----------------------------------
    #     Eliminar Turno
    #-----------------------------------   
    def eliminar_turno(self, id_turno):
        self.cursor.execute(f"DELETE FROM turnos WHERE id_turno={id_turno}")
        self.conn.commit()
        return self.cursor.rowcount > 0  # Si devuelve cero es que no borró nada

#-----------------------------------
#   Cuerpo del programa
#-----------------------------------

<<<<<<< HEAD
#turno = Turno(host='localhost', user='admin', password='admin', database='efcarcare')
turno = Turno(host='edfigueredo.mysql.pythonanywhere-services.com', user='admin', password='admin', database='edfigueredo$efcarcare')

#Ruta_destino='./img/'
Ruta_destino='/home/edfigueredo/mysite/img'
=======
turno = Turno(host='cinthia92.mysql.pythonanywhere-services.com', user='cinthia92', password='codoacodo24', database='cinthia92$efcarcare')
>>>>>>> 94b49f1376dc551e3141c74c7d50f92d99282061

#-----------------------Listado de turnos----------------
@app.route("/turnos", methods=["GET"])
def listar_turnos():
    listado = turno.listar_turnos()
    listado_convertido = convertir_a_serializable(listado)
    return jsonify(listado_convertido)

#-----------------------Listado de solicitudes--------------
@app.route("/solicitudes", methods=["GET"])
def listar_solicitud():
    listado = turno.listar_solicitudes()
    listado_convertido = convertir_a_serializable(listado)
    return jsonify(listado_convertido)

#---------------------- Buscar turno ------------------------
@app.route("/buscar/<int:id_turno>", methods=["GET"])
def buscar_turno(id_turno):
    busqueda = turno.consulta_turno(id_turno)
    listado_convertido = convertir_a_serializable(busqueda)
    return jsonify(listado_convertido)

#---------------------- Agregar turno ---------------------------
@app.route("/turnos", methods=["POST"])
def agregar_turno():
    nombre = request.form['nombre']
    celular = request.form['celular']
    vehiculo = request.form['vehiculo']
    patente = request.form['patente']
    servicios = ", ".join(request.form.getlist('servicios[]'))  # Convertimos la lista a una cadena
    archivo = request.files['archivo']
    observaciones = request.form['observaciones']
    fecha = request.form['fecha']
    hora = request.form['hora']

    # Creo un nombre de imagen que no se repita y lo guardo en la carpeta img
    nombre_foto = secure_filename(archivo.filename)
    nombre_base, extension = os.path.splitext(nombre_foto)  # Divido el nombre en su nombre y extensión
    nombre_foto = f"{nombre_base}_{int(time.time())}{extension}"  # Rearmo el nombre: nombre base, fechahora y extensión
<<<<<<< HEAD
    ruta_foto = os.path.join(Ruta_destino, nombre_foto)  # En esa ruta guarda la foto con ese nombre
=======
    ruta_foto = os.path.join('/home/cinthia92/mysite/crud/img', nombre_foto)  # En esa ruta guarda la foto con ese nombre
>>>>>>> 94b49f1376dc551e3141c74c7d50f92d99282061
    
    try:
        archivo.save(ruta_foto)
    except Exception as e:
        return jsonify({"mensaje": "Error al guardar el archivo.", "error": str(e)}), 500
    
    # Doy el alta
    nuevo_id = turno.crear_turno(nombre, celular, vehiculo, patente, servicios, nombre_foto, observaciones, fecha, hora)
    
    # Me comunica si funcionó o no
    if nuevo_id:
        return jsonify({"mensaje": "Turno creado correctamente.", "id_turno": nuevo_id, "al cliente": nombre}), 201
    else:
        return jsonify({"mensaje": "Error al crear el turno."}), 500
    
#-----------------------------------------------
# Modificar turno
#-----------------------------------------------
@app.route("/turnos/<int:id_turno>", methods=["PUT"]) 
# Solo permitimos modificar las observaciones, agregar algún servicio, 
# fecha y hora para asignar o modificar turno
def modificar_turno(id_turno):
    nueva_observaciones = request.form.get('observaciones')
    nueva_fecha = request.form.get('fecha')
    nueva_hora = request.form.get('hora')
    
    if turno.modificar_turno(id_turno, nueva_observaciones, nueva_fecha, nueva_hora):
        return jsonify({"mensaje": "Turno modificado"}), 200
    else:
        return jsonify({"mensaje": "No se pudo modificar el turno"}), 500
    
#--------------------------------------------------
#     Eliminar
#--------------------------------------------------
@app.route("/turnos/<int:id_turno>", methods=["DELETE"])
def eliminar_turno(id_turno):
    if turno.eliminar_turno(id_turno):
        return jsonify({"mensaje": "Turno eliminado correctamente."}), 200
    else:
        return jsonify({"mensaje": "Error al eliminar el turno."}), 500

#-----------------------
# Cierre de Flask
#-----------------------
if __name__ == "__main__":
    app.run(debug=True)