import mysql.connector
import mysql.connector.errorcode

#----------------------------------------------------------------
#copie tal cual el proyecto

# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template

from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS
# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------

#creamos un objeto de flask para usar sus metodos

app = Flask(__name__) #podes llamar como quieras usamos app
CORS(app)             # Esto habilitará CORS para todas las rutas


class Turno:

#creo el constructor
    def __init__ (self,host, user, password,database, port):
        """
        Args
        host(str): direccion de servidor
        user(str): nombre de usurio
        password: contraseña
        database: el nombre de la bd
        """
        #establecemos la coneccion en una variable, con esta variable estamos llamando siempre a la conexion que se crea
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )  
    #creo el cursor que traduce y podemos escribir comando de SQL
        self.cursor=self.conn.cursor()

    #creoamos o conectamos a la bd
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            #si el error es xq la bd no existe la creo
            if err.errno==mysql.connector.errorcode.ER_BAD_DB_ERROR:
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



        #-----------------------------------
#   cuerpo del programa"
#-----------------------------------

turno=Turno(host='localhost',user='root',password='root',database='efcarecar', port=3308)