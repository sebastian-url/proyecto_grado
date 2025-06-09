class CompraModelo:
    def __init__(self):
        pass

    @classmethod
    def registrar_compra(self, db, id_usuario, id_producto, cantidad,fecha,total):
        try:
            cursor = db.connection.cursor()
            # Insertar la compra en la tabla compra
            cursor.execute("INSERT INTO compra (id_usuario,fecha) VALUES (%s,%s)", (id_usuario,fecha))
            id_compra = cursor.lastrowid
            
            # Insertar el detalle de la compra en la tabla detalle_compra
            cursor.execute("INSERT INTO detalle_compra (id_compra, id_producto, cantidad,total) VALUES (%s, %s, %s,%s)",
                           (id_compra, id_producto, cantidad,total))
            
            db.connection.commit()
            return id_compra  # Retorna el ID de la compra registrada
        except Exception as e:
            db.connection.rollback()
            print(f"Error al registrar la compra: {e}")
            return None
        finally:
            cursor.close()

    @classmethod
    def obtener_pedidos(self, db):
        try:
            cursor = db.connection.cursor()
            sql= """
                SELECT 
                dc.id_detalle,
                u.id,
                u.nombre AS nombre_usuario,
                u.celular,
                p.nombre_producto,
                p.descripcion,
                p.precio_producto,
                c.fecha,
                c.estado,
                dc.cantidad,
                dc.total,
                dc.id_compra
                FROM detalle_compra dc
                JOIN compra c ON dc.id_compra = c.id_compra
                JOIN usuarios u ON c.id_usuario = u.id
                JOIN producto p ON dc.id_producto = p.id_producto
                WHERE c.estado = 'procesando' OR c.estado = 'aceptado'
                ORDER BY c.fecha DESC;

                """
            cursor.execute(sql)
            pedidos = cursor.fetchall()
            return [
                {
                    "id": pedido[0],
                    "id_usuario": pedido[1],
                    "usuario": pedido[2],
                    "celular": pedido[3],
                    "producto": pedido[4],
                    "descripcion": pedido[5],
                    "precio": pedido[6],
                    "fecha": pedido[7],
                    "estado": pedido[8],
                    "cantidad": pedido[9],
                    "total": pedido[10],
                    "id_compra": pedido[11]
                } for pedido in pedidos
            ]
        except Exception as e:
            return f"Error al obtener los pedidos: {e}"
        
    @classmethod
    def actualizarPedido(self, db, id_compra, estado):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE compra SET estado=%s WHERE id_compra=%s"
            cursor.execute(sql, (estado, id_compra))
            db.connection.commit()
            return cursor.rowcount
        except Exception as e:
            return None
        finally:
            cursor.close()

    @classmethod
    def obtener_historial(self, db):
        try:
            cursor = db.connection.cursor()
            sql= """
                SELECT 
                u.nombre AS nombre_usuario,
                u.celular,
                p.nombre_producto,
                p.descripcion,
                p.precio_producto,
                c.fecha,
                c.estado,
                dc.cantidad,
                dc.total
                FROM detalle_compra dc
                JOIN compra c ON dc.id_compra = c.id_compra
                JOIN usuarios u ON c.id_usuario = u.id
                JOIN producto p ON dc.id_producto = p.id_producto
                WHERE c.estado = 'terminado'
                ORDER BY c.fecha DESC;

                """
            cursor.execute(sql)
            pedidos = cursor.fetchall()
            return [
                {
                    "usuario": pedido[0],
                    "celular": pedido[1],
                    "producto": pedido[2],
                    "descripcion": pedido[3],
                    "precio": pedido[4],
                    "fecha": pedido[5],
                    "cantidad": pedido[7],
                    "total": pedido[8]
                } for pedido in pedidos
            ]
        except Exception as e:
            return f"Error al obtener los pedidos: {e}"
        
    @classmethod
    def obtener_pendientes(self,db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT COUNT(*) AS cantidad FROM compra WHERE estado = 'procesando'"
            cursor.execute(sql,)
            return cursor.fetchall()
        except Exception as e:
            return f"Error al actualizar el pedido: {e}"
        finally:
            cursor.close()

    @classmethod
    def obtener_pedidos_usuario(self,db,id_usuario):
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT 
                p.nombre_producto,
                p.descripcion,
                p.precio_producto,
                c.fecha,
                c.estado,
                dc.cantidad,
                dc.total
                FROM detalle_compra dc
                JOIN compra c ON dc.id_compra = c.id_compra
                JOIN usuarios u ON c.id_usuario = u.id
                JOIN producto p ON dc.id_producto = p.id_producto
                WHERE c.id_usuario = %s AND c.estado IN ('procesando', 'aceptado', 'terminado')
                ORDER BY c.fecha DESC;
            """
            cursor.execute(sql, (id_usuario,))
            pedidos = cursor.fetchall()
            return [
                {
                    "producto": pedido[0],
                    "descripcion": pedido[1],
                    "precio": pedido[2],
                    "fecha": pedido[3],
                    "estado": pedido[4],
                    "cantidad": pedido[5],
                    "total": pedido[6]
                } for pedido in pedidos
            ]
        except Exception as e:
            return f"Error al obtener los pedidos del usuario: {e}"
        finally:
            cursor.close()