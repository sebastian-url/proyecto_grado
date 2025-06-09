class ProductoModelo:
    def __init__(self):
        pass

    @classmethod #<-- decorador para indicar que no se necesita instanciar la clase para usar el metodo
    def registrar_producto(self,db, nombre, descripcion, precio, rutaImagen):
        try:
            cursor = db.connection.cursor()
            sql = "INSERT INTO producto (nombre_producto, descripcion, precio_producto, imagen) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nombre, descripcion, precio, rutaImagen))
            db.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            return f"Error al registrar el producto: {e}"
        
    @classmethod
    def obtener_productos(self, db):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM producto WHERE estado = 1")
            productos = cursor.fetchall()
            return [
                {
                    "id": producto[0],
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
    def eliminar_producto(self, db, id_producto):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE producto SET estado = 0 WHERE id_producto=%s"
            cursor.execute(sql, (id_producto,))
            db.connection.commit()
            return cursor.rowcount
        except Exception as e:
            return f"Error al eliminar el producto: {e}"
        