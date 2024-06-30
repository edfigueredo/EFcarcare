import mysql.connector
from mysql.connector import errorcode


#copie tal cual el proyecto

# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template

# Instalar con pip install flask-cors
from flask_cors import CORS
# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------
from datetime import datetime, timedelta
#------------------------------------------------------
#    funcion para tiem data a string
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

#creamos un objeto de flask para usar sus metodos

app = Flask(__name__) #podes llamar como quieras usamos app
CORS(app)             # Esto habilitará CORS para todas las rutas


class Turno:

#creo el constructor
    def __init__ (self,host, user, password,database):
        """
        Args
        host(str): direccion de servidor
        user(str): nombre de usurio
        password: contraseña
        database: el nombre de la bd
        """
        #establecemos la coneccion
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )  
    #creo el cursor
        self.cursor=self.conn.cursor()

    #creoamos o conectamos a la bd
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            #si el error es xq la bd no existe la creo
            if err.errno==errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
                self.conndatabase=database
            else:
                    raise err
            
        #creo la bd
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS `turnos`(
                                id_turno INT  PRIMARY KEY AUTO_INCREMENT,
                                nombre VARCHAR(40) NOT NULL,
                                celular VARCHAR(20) NOT NULL,
                                vehiculo VARCHAR(30) NOT NULL,
                                patente VARCHAR(10) NOT NULL,
                                servicio VARCHAR(60),
                                foto VARCHAR(60),
                                observaciones VARCHAR(60) NULL,
                                fecha DATE NOT NULL,
                                hora TIME NOT NULL);''')
        #guarda los cambios
        self.conn.commit()

        #cierra el cursor y abre uno nuevo con el parametro diccionario=true
        self.cursor.close()
        self.cursor=self.conn.cursor(dictionary=True)

    #----------------------------------
    #    Agregar Turno
    #----------------------------------

    def crear_turno(self, nombre,celular,vehiculo,patente,servicio,foto,fecha,hora):
        sql="INSERT INTO turnos (nombre,celular,vehiculo,patente,servicio,foto,fecha,hora) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        valores=(nombre,celular,vehiculo,patente,servicio,foto,fecha,hora)
        self.cursor.execute(sql,valores)#ejecuta
        self.conn.commit()
        return self.cursor.lastrowid #nos devuelve la ultima id creada

    #-----------------------------------
    #     Consultar turno
    #-----------------------------------

    def consulta_turno(self,id_turno):
        #consultamos un turno
        self.cursor.execute(f"SELECT * FROM turnos WHERE id_turno={id_turno}")
        return self.cursor.fetchone()   #devuelve el registro uno solo

    #-----------------------------------
    #     Modificar Turno
    #-----------------------------------   
    def modificar_turno(self, id_turno, nombre,celular,vehiculo,patente,servicio,foto,fecha,hora):
        sql="UPDATE turnos SET nombre=%s,celular=%s,vehiculo=%s,patente=%s,servicio=%s,foto=%s,fecha=%s,hora=%s WHERE id_turno=%s"
        valores=(nombre,celular,vehiculo,patente,servicio,foto,fecha,hora, id_turno)
        self.cursor.execute(sql,valores)#ejecuta
        self.conn.commit()
        return self.cursor.rowcount > 0 #cantidad de columnas cambiadas

    #-----------------------------------
    #     Listar Turnos
    #-----------------------------------   
    def listar_turnos(self):
        self.cursor.execute("SELECT * FROM turnos WHERE fecha >= CURDATE();")
        turnos=self.cursor.fetchall() #devuelve todos los resultados
        return turnos

    #-----------------------------------
    #     Listar Nuevas Solciitudes
    #-----------------------------------   
    def listar_solicitudes(self):
        self.cursor.execute("SELECT * FROM turnos WHERE fecha IS NULL;")
        turnos=self.cursor.fetchall() #devuelve todos los resultados
        return turnos

    #-----------------------------------
    #     eliminar Turno
    #-----------------------------------   

    def eliminar_turno(self, id_turno):
        self.cursor.execute(f"DELETE FROM turnos WHERE id_turno={id_turno}")
        self.conn.commit()
        return self.cursor.rowcount > 0 #si devuelve cero es que no borro nada



#-----------------------------------
#   cuerpo del programa"
#-----------------------------------

turno=Turno(host='localhost',user='admin',password='admin',database='efcarcare')

#-----------------------listado de turnos--------------
@app.route("/turnos", methods=["GET"])
def listar_turnos():
    listado = turno.listar_turnos()
    listado_convertido = convertir_a_serializable(listado)
    return jsonify(listado_convertido)

#-----------------------listado de solicitudes--------------
@app.route("/solicitudes", methods=["GET"])
def listar_solicitud():
    listado = turno.listar_solicitudes()
    listado_convertido = convertir_a_serializable(listado)
    return jsonify(listado_convertido)




#-----------------------
#cierre de flask
#-----------------------
if __name__ == "__main__":
    app.run(debug=True)
