import crud_academico
db = crud_academico.crud()

class crud_materia:
    def consultar(self):
        #return db.consultar("SELECT * FROM materias WHERE nombre like '%" + buscar["buscar"] + "%'")
        return db.consultar("SELECT * FROM materias")
    
    def administrar(self, datos):
        if(datos["accion"] == "nuevo"):	
            sql = """
                INSERT INTO materias (codigo, nombre, uv)
                VALUES (%s, %s, %s) 
            """
            valores = (datos["codigo"], datos["nombre"], datos["uv"])
        elif(datos["accion"] == "modificar"):
            sql = """
                UPDATE materias
                    SET codigo = %s, nombre = %s, uv = %s
                WHERE idMateria = %s
            """
            valores = (datos["codigo"], datos["nombre"], datos["uv"], datos["idMateria"])
        elif(datos["accion"] == "eliminar"):
            sql = """
                DELETE FROM materias
                WHERE idMateria = %s
            """
            valores = (datos["idMateria"],)
        return db.procesar_consultas(sql, valores)