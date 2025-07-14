from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
import MySQLdb

hash_admin = generate_password_hash('sebas192410')
print(hash_admin)

class ModeloUsuario:

    @classmethod
    def iniciar_sesion(cls, db, correo, contrasena):
        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM usuarios WHERE correo = %s AND estado = 'activo'"
            cursor.execute(query, (correo,))
            usuario = cursor.fetchone()
            print('Usuario encontrado:', usuario)

            if usuario and check_password_hash(usuario['contrasena'], contrasena):
                print("Validación:", check_password_hash(usuario['contrasena'], contrasena))
                return {
                    'id': usuario['id'],
                    'nombre': usuario['nombre'],
                    'apellido': usuario['apellido'],
                    'celular': usuario['celular'],
                    'correo': usuario['correo'],
                    'rol': usuario['rol_id'],
                    'direccion': usuario['direccion']
                }

            return None
        except Exception as e:
            print("Error al iniciar sesión:", e)
            return f"Error al iniciar sesión: {e}"



    @classmethod
    def registrar(cls, db, nombre, apellido, celular, correo, direccion, contrasena):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
            if cursor.fetchone():
                return None  # Usuario ya existe

            contrasena_hash = generate_password_hash(contrasena)
            sql = """
                INSERT INTO usuarios (nombre, apellido, celular, correo, contrasena, estado, rol_id, direccion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre, apellido, celular, correo, contrasena_hash, 'activo', 2, direccion))
            db.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            db.connection.rollback()
            return f"Error al registrar: {e}"

    @classmethod
    def obtenerUsuarioPorDatos(cls, db, nombre, apellido, celular, correo):
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT * FROM usuarios 
                WHERE nombre = %s AND apellido = %s AND celular = %s AND correo = %s
            """
            cursor.execute(sql, (nombre, apellido, celular, correo))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al verificar usuario existente: {e}")
            return None

    @staticmethod
    def bloquearUsuarios(db, id_usuario):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE usuarios SET estado = 'inactivo' WHERE id = %s"
            cursor.execute(sql, (id_usuario,))
            db.connection.commit()
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
            db.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Error al desbloquear usuario: {e}")
            return 0

    @classmethod
    def eliminarUsuario(cls, db, id_usuario):
        try:
            sql = 'UPDATE usuarios SET estado = "eliminado" WHERE id = %s'
            cursor = db.connection.cursor()
            cursor.execute(sql, (id_usuario,))
            db.connection.commit()
            return cursor.rowcount
        except Exception as e:
            return f"Error al eliminar el usuario: {e}"

    @classmethod
    def obtenerUsuarios(cls, db):
        try:
            sql = 'SELECT * FROM usuarios WHERE rol_id = 2'
            cursor = db.connection.cursor()
            cursor.execute(sql)
            usuarios = cursor.fetchall()
            return [
                {
                    "id": u['id'],
                    "nombre": u['nombre'],
                    "apellido": u['apellido'],
                    "celular": u['celular'],
                    "correo": u['correo'],
                    "estado": u['estado'],
                } for u in usuarios
            ]
        except Exception as e:
            return f"Error al obtener usuarios: {e}"

    @classmethod
    def obtenerUsuarioPorId(cls, db, id_usuario):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id_usuario,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener usuario por ID: {e}")
            return None

    @classmethod
    def obtenerUsuarioPorCorreo(cls, db, correo):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener usuario por correo: {e}")
            return None

    @classmethod
    def actualizar_contraseña(cls, db, id_usuario, nueva_contrasena):
        try:
            nueva_hash = generate_password_hash(nueva_contrasena)
            sql = "UPDATE usuarios SET contrasena = %s WHERE id = %s"
            cursor = db.connection.cursor()
            cursor.execute(sql, (nueva_hash, id_usuario))
            db.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Error al actualizar contraseña: {e}")
            return 0

    @classmethod
    def obtenerContrasena(cls, db, correo):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT contrasena FROM usuarios WHERE correo = %s", (correo,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener contraseña: {e}")
            return None

    @classmethod
    def generarContraseña(cls):
        longitud = 8
        caracteres = string.ascii_letters + string.digits + string.punctuation
        while True:
            password = ''.join(random.choices(caracteres, k=longitud))
            if (any(c.isupper() for c in password) and
                any(c.islower() for c in password) and
                any(c.isdigit() for c in password)):
                return password
