import crud_academico
db = crud_academico.crud()

class crud_docente:
    def consultar(self):
        #return db.consultar("SELECT * FROM docentes WHERE nombre like '%" + buscar["buscar"] + "%'")
        return db.consultar("SELECT * FROM docentes")
    
    def administrar(self, datos):
        if(datos["accion"] == "nuevo"):	
            sql = """
                INSERT INTO docentes (codigo, nombre, direccion, telefono, email, dui)
                VALUES (%s, %s, %s, %s, %s, %s) 
            """
            valores = (datos["codigo"], datos["nombre"], datos["direccion"], datos["telefono"], datos["correo"], datos["dui"])
        elif(datos["accion"] == "modificar"):
            sql = """
                UPDATE docentes
                    SET codigo = %s, nombre = %s, direccion = %s, telefono = %s, email = %s, dui = %s
                WHERE idDocente = %s
            """
            valores = (datos["codigo"], datos["nombre"], datos["direccion"], 
                       datos["telefono"], datos["correo"], datos["dui"], datos["idDocente"])
        elif(datos["accion"] == "eliminar"):
            sql = """
                DELETE FROM docentes
                WHERE idDocente = %s
            """
            valores = (datos["idDocente"],)
        return db.procesar_consultas(sql, valores)