from werkzeug.security import generate_password_hash,check_password_hash  # metodo para generar una contraseña hasheada
import random
import string

class ModeloUsuario():
    def __init__(self):
        pass
    
    @classmethod
    def obtenerUsuarioPorCorreo(self,db,correo):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE correo=%s AND estado = 'activo'", (correo,))
            usuario = cursor.fetchone()
            return usuario
        except Exception as e:
            return None
    
    @classmethod
    def iniciarSesion(self,db,correo,contrasena):
        try:
            usuario = self.obtenerUsuarioPorCorreo(db,correo)
            if usuario != None:
                if check_password_hash(usuario[5],contrasena):
                    # Si la contraseña es correcta, retornamos el usuario
                    return {
                        "id": usuario[0],
                        "nombre": usuario[1],
                        "apellido": usuario[2],
                        "celular": usuario[3],
                        "correo": usuario[4],
                        "rol": usuario[7]
                    }

            return None
        except Exception as e:
            return f"Error al iniciar sesion: {e}"
        
    @classmethod
    def registrar(self,db,nombre,apellido,celular,correo,contrasena):
        try:
            usuario = self.obtenerUsuarioPorCorreo(db,correo)
            if usuario == None:
                contrasena_hash = generate_password_hash(contrasena, method='pbkdf2:sha256', salt_length=8)
                cursor = db.connection.cursor()
                sql= "INSERT INTO usuarios (nombre, apellido, celular, correo, contrasena) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (nombre, apellido, celular, correo, contrasena_hash))
                cursor.connection.commit()
                return cursor.lastrowid
            
            return None

        except Exception as e:
            return f"Error al registrar: {e}"
        

    @staticmethod
    def bloquearUsuarios(db, id_usuario):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE usuarios SET estado = 'inactivo' WHERE id = %s"
            cursor.execute(sql, (id_usuario,))
            cursor.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Error al bloquear usuario: {e}")
            return 0

        
    @staticmethod
    def desbloquearUsuarios(db, id_usuario):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE usuarios SET estado = 'activo' WHERE id = %s"
            cursor.execute(sql, (id_usuario,))
            cursor.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Error al desbloquear usuario: {e}")
            return False


    
    @classmethod
    def eliminarUsuario(self, db, id_usuario):
        try:
            sql = 'UPDATE usuarios SET estado = "eliminado" WHERE id = %s'
            cursor = db.connection.cursor()
            cursor.execute(sql, (id_usuario,))
            cursor.connection.commit()
            return cursor.rowcount
        except Exception as e:
            return f"Error al eliminar el usuario: {e}"

            
        except Exception as e:
            return f"Error al intentar modificar: {e}"
    @classmethod
    def obtenerUsuarios(self, db):
        try:
            sql = 'SELECT * FROM usuarios WHERE rol_id = 2'
            cursor = db.connection.cursor()
            cursor.execute(sql)
            usuarios = cursor.fetchall()
            return [
                {
                    "id": usuario[0],
                    "nombre": usuario[1],
                    "apellido": usuario[2],
                    "celular": usuario[3],
                    "correo": usuario[4],
                    "estado": usuario[6]  # asumimos que 'estado' está en la columna 7
                } for usuario in usuarios
            ]
        except Exception as e:
            return f"Error al intentar modificar: {e}"

        
    @classmethod
    def obtenerUsuarioPorId(self,db,id_usuario):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id_usuario,))
            return cursor.fetchone()
        except Exception as e:
            return f"Error al obtener el usuario por ID: {e}"
        
    @classmethod
    def generarContraseña(self):
        longitud = 8
        caracteres = (
            string.ascii_uppercase +  # Letras mayúsculas
            string.ascii_lowercase +  # Letras minúsculas
            string.digits +           # Números
            string.punctuation        # Caracteres especiales
        )

        # Asegurar al menos un carácter de cada tipo
        password = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice(string.punctuation)
        ]

        # Completar con caracteres aleatorios
        password += random.choices(caracteres, k=longitud - 4)
        random.shuffle(password)

        return ''.join(password)
    

    @classmethod
    def actualizar_contraseña(self,db,id_usuario,contraseña):
        sql = "UPDATE usuarios SET contrasena = %s WHERE id = %s"
        try:
            contraseñaHasheada= generate_password_hash(contraseña, method='pbkdf2:sha256', salt_length=8)
            cursor = db.connection.cursor()
            cursor.execute(sql, (contraseñaHasheada,id_usuario))
            cursor.connection.commit()
            return cursor.rowcount
        except Exception as e:
            return f"Error al obtener el usuario por ID: {e}"
        
    @classmethod
    def obtenerContrasena(self,db,correo):
            cursor = db.connection.cursor()
            cursor.execute("SELECT contrasena FROM usuarios WHERE correo = %s", (correo,))
            resultado = cursor.fetchone()
            return resultado

