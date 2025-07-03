class ProductoModelo:
    def __init__(self):
        pass

    @classmethod
    def registrar_producto(cls, db, nombre, descripcion, precio, rutaImagen):
        try:
            cursor = db.connection.cursor()

            # Validación: verificar si ya existe el producto
            cursor.execute(
    "SELECT * FROM producto WHERE nombre_producto = %s AND descripcion = %s AND precio_producto = %s AND imagen = %s",
    (nombre, descripcion, precio, rutaImagen)
)

            existente = cursor.fetchone()
            if existente:
                return {"error": "El producto ya existe"}

            # Insertar nuevo producto
            sql = "INSERT INTO producto (nombre_producto, descripcion, precio_producto, imagen) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nombre, descripcion, precio, rutaImagen))
            db.connection.commit()

            return {"success": True, "id": cursor.lastrowid}
        
        except Exception as e:
            return {"error": f"Error al registrar el producto: {e}"}

        
    @classmethod
    def obtener_productos(self, db):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM producto WHERE estado = 1")
            productos = cursor.fetchall()
            return [
                {
                    #"id": producto[0],
                    "nombre_producto": producto[1],
                    "descripcion": producto[2],
                    "precio_producto": producto[3],
                    "imagen": producto[4]
                } for producto in productos
            ]
        except Exception as e:
            return f"Error al obtener los productos: {e}"
        
    @classmethod
    def actualizar_producto(self, db, id_producto, nombre, descripcion, precio, rutaImagen):
        try:
            cursor = db.connection.cursor()
            if rutaImagen is None:
                sql = "UPDATE producto SET nombre_producto=%s, descripcion=%s, precio_producto=%s WHERE id_producto=%s"
                cursor.execute(sql, (nombre, descripcion, precio, id_producto))
            else:
                sql = "UPDATE producto SET nombre_producto=%s, descripcion=%s, precio_producto=%s, imagen=%s WHERE id_producto=%s"
                cursor.execute(sql, (nombre, descripcion, precio, rutaImagen, id_producto))

            db.connection.commit()
            return cursor.rowcount
        except Exception as e:
            return f"Error al actualizar el producto: {e}"
        
    @classmethod
    def eliminar_producto(cls, db, id_producto):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT id_producto FROM producto WHERE id_producto = %s", (id_producto,))
            producto = cursor.fetchone()
            if not producto:
                return "El producto no existe"

            # Verificar que la columna 'estado' exista en la tabla producto
            cursor.execute("DELETE FROM producto WHERE id_producto = %s", (id_producto,))
            db.connection.commit()
            return cursor.rowcount

        except Exception as e:
            print(f"Error al eliminar el producto: {e}")
            return f"Error al eliminar el producto: {e}"



        