import sqlite3

class ProyectoDB:
    def __init__(self, db_name="proyecto.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Crear tablas
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS rol (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_rol TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,   
            apellido TEXT,
            celular TEXT,
            correo TEXT,
            contrasena TEXT,
            rol_id INTEGER DEFAULT 2,
            FOREIGN KEY (rol_id) REFERENCES rol(id)
        );

        CREATE TABLE IF NOT EXISTS compra (
            cantidad INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            celular INTEGER NOT NULL
        );
        """)
        self.conn.commit()

    def registrar_usuario(self, nombre, apellido, celular, correo, contrasena, rol_id=2):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nombre, apellido, celular, correo, contrasena, rol_id)
            VALUES (?, ?, ?,   ?, ?, ?)
        """, (nombre, apellido, celular, correo, contrasena, rol_id))
        self.conn.commit()

    def registrar_compra(self, cantidad, nombre, apellido, celular):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO compra (cantidad, nombre, apellido, celular)
            VALUES (?, ?, ?, ?)
        """, (cantidad, nombre, apellido, celular))
        self.conn.commit()

    def obtener_usuarios(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT u.id, u.nombre, u.apellido, u.correo, r.nombre_rol
            FROM usuarios u
            JOIN rol r ON u.rol_id = r.id
        """)
        return cursor.fetchall()

    def obtener_compras(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM compra")
        return cursor.fetchall()

    def informe_compras_usuarios(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT u.nombre, u.apellido, u.correo, c.cantidad
            FROM usuarios u
            JOIN compra c ON u.nombre = c.nombre AND u.apellido = c.apellido
        """)
        return cursor.fetchall()

# Ejemplo de uso
if __name__ == "__main__":
    db = ProyectoDB()
    db.registrar_usuario("Juan", "Pérez", "123456789", "juan@example.com", "clave123", rol_id=2)
    db.registrar_compra(2, "Juan", "Pérez", 123456789)

    print("Usuarios:")
    for u in db.obtener_usuarios():
        print(u)

    print("\nCompras:")
    for c in db.obtener_compras():
        print(c)

    print("\nInforme de Compras por Usuario:")
    for i in db.informe_compras_usuarios():
        print(i)