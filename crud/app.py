import mysql.connector
import mysql.connector.errorcode

#creo el constructor

class Turno:
    def __init__ (self,host, user, password,database):
        """
        Args
        host(str): direccion de servidor
        user(str): nombre de usurio
        password: contraseña
        database: el nombre de la bd
        """
        #establecemos la coneccion
        self.conn = mysql.connector.conect(
                host=host,
                user=user,
                password=password
        )  
        #creo el cursor
        self.curso=self.conn.cursor()

        #creoamos o conectamos a la bd
        try:
            self.cursor.execute(f"USE{database}")
        except mysql.connector.Error as err:
            #si el error es xq la bd no existe la creo
            if err.errno==mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
                self.conndatabase=database
            else:
                    raise err
            
        #creo la bd
        self.cursor.execute(''' CREATE TABLE `turnos`(
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
     sql="UPDATE turnos SET nombre=%S,celular=%S,vehiculo=%S,patente=%S,servicio=%S,foto=%S,fecha=%S,hora=%S WHERE id_turno=%S"
     valores=(nombre,celular,vehiculo,patente,servicio,foto,fecha,hora, id_turno)
     self.cursor.execute(sql,valores)#ejecuta
     self.conn.commit()
     return self.cursor.rowcount > 0 #cantidad de columnas cambiadas

#-----------------------------------
#     Modificar Turno
#-----------------------------------   
def listar_turnos(self):
     self.cursor.execute("SELECT * FROM turnos WHERE fecha >= CURDATE();")
     turnos=self.cursor.fetchall() #devuelve todos los resultados
     return turnos

#-----------------------------------
#     eliminar Turno
#-----------------------------------   

def eliminar_turno(self, id_turno):
     self.cursor.execute(f"DELETE FROM turnos WHERE id_turno={id_turno}")
     self.cursor.commit()
     return self.cursor.rowcount >0 #si devuelve cero es que no borro nada



#-----------------------------------
#   cuerpo del programa"
#-----------------------------------

turno=Turno(host='localhost',user='admin',password='admin',database='efcarecar')
