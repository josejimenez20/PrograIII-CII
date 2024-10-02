#pip install mysql-connector-python
import mysql.connector
from mysql.connector import Error

class crud:
    def __init__(self):
        print("Conectando a la base de datos...")
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_academica"
        )
        if self.conexion.is_connected():
            print("Conectado")
        else:
            print("No se ha podido conectar")
    def consultar(self, sql):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()
    
    def procesar_consultas(self, sql, valores):
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql, valores)
            self.conexion.commit()
            return "ok"
        except Error as e:
            return str(e)