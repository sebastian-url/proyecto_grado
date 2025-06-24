from flask import Flask, jsonify, send_from_directory,request,session,redirect,render_template, url_for
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from config import config
from models.usuarioModelo import ModeloUsuario
from models.productoModelo import ProductoModelo
from models.compraModelo import CompraModelo
import threading
import os
from werkzeug.utils import secure_filename
import random
import string
import datetime
from werkzeug.security import generate_password_hash,check_password_hash 
from flask_mysqldb import MySQL

# --- Configurar la app de Flask ---
app = Flask(__name__)
CORS(app)  # Permite solicitudes desde el frontend



#para la base de datos
db = MySQL(app)

# Configuración del servidor SMTP (ejemplo con Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'jcardenasoyola@gmail.com'
app.config['MAIL_PASSWORD'] = 'twby hewg ahuz qxjr'
app.config['MAIL_DEFAULT_SENDER'] = 'jcardenasoyola@gmail.com'

mail = Mail(app)

def enviar_correo_async(app, msg):
    with app.app_context():
        mail.send(msg)


#ruta principal
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        correo = data.get('correo')
        contrasena = data.get('contrasena')

        if not correo or not contrasena:
            return jsonify({'mensaje': 'Correo y contraseña requeridos'}), 400

        res = ModeloUsuario.iniciarSesion(db, correo, contrasena)

        if isinstance(res, dict):
            # Guardar el usuario en la sesión (sin contraseña)
            session['usuario'] = {
                'id': res['id'],
                'nombre': res['nombre'],
                'apellido': res['apellido'],
                'celular': res['celular'],
                'correo': res['correo'],
                'rol': res['rol'],
                'direccion': res['direccion']
            }
            return jsonify({'mensaje': 'Inicio de sesión exitoso', 'rol': res['rol']}), 200

        elif isinstance(res, str) and res.startswith("Error"):
            return jsonify({'mensaje': res}), 500

        else:
            return jsonify({'mensaje': 'Error al iniciar sesión, verifique sus credenciales'}), 401

    # Si es GET, renderiza HTML
    return render_template('index.html')


@app.route('/menu')
def menu():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    rol = session['usuario']['rol']

    if rol == 1:
        return render_template('menu.html')  # Vista para administradores
    elif rol == 2:
        return redirect(url_for('catalogo'))  # Vista para clientes
    else:
        return redirect(url_for('login'))  # Rol no permitido

@app.route('/catalogo',methods=['GET'])
def catalogo():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    rol = session['usuario']['rol']

    if rol == 1:
        return redirect(url_for('menu'))  # Vista para administradores
    elif rol == 2:
        return render_template('catalogo.html')  # Vista para clientes
    else:
        return redirect(url_for('login'))  # Rol no permitido

@app.route('/historial')
def historial():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    rol = session['usuario']['rol']

    if rol == 1:
        return render_template('historial.html')  # Vista para administradores
    elif rol == 2:
        return redirect(url_for('catalogo'))  # Vista para clientes
    else:
        return redirect(url_for('login'))  # Rol no permitido

@app.route('/usuarios')
def usuarios():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    rol = session['usuario']['rol']

    if rol == 1:
        return render_template('usuarios.html')  # Vista para administradores
    elif rol == 2:
        return redirect(url_for('catalogo'))  # Vista para clientes
    else:
        return redirect(url_for('login'))  # Rol no permitido

@app.route('/pedidos')
def pedidos():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    rol = session['usuario']['rol']

    if rol == 1:
        return render_template('pedidos.html')  # Vista para administradores
    elif rol == 2:
        return redirect(url_for('catalogo'))  # Vista para clientes
    else:
        return redirect(url_for('login'))  # Rol no permitido

@app.route('/productos')
def productos():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    rol = session['usuario']['rol']

    if rol == 1:
        return render_template('productos.html')  # Vista para administradores
    elif rol == 2:
        return redirect(url_for('catalogo'))  # Vista para clientes
    else:
        return redirect(url_for('login'))  # Rol no permitido

@app.route('/compra')
def compra():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    rol = session['usuario']['rol']

    if rol == 1:
        return redirect(url_for('menu'))  # Vista para administradores
    elif rol == 2:
        return render_template('compra.html')  # Vista para clientes
    else:
        return redirect(url_for('login'))  # Rol no permitido

@app.route('/api/usuario-logueado', methods=['GET'])
def usuario_logueado():
    if 'usuario' in session:
        return jsonify(session['usuario'])  # Asegúrate que 'nombre' esté en session['usuario']
    else:
        return jsonify({'error': 'No ha iniciado sesión'}), 401

#validar el rol
@app.route('/api/admin-only', methods=['GET'])
def solo_admin():
    usuario = session.get('usuario')
    if not usuario:
        return jsonify({'error': 'No autenticado'}), 401
    if usuario['rol'] != 1:
        return jsonify({'error': 'Acceso denegado'}), 403
    return jsonify({'mensaje': 'Bienvenido admin'})
  
#ruta del registro
@app.route('/registro',methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        data = request.get_json()
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        celular = data.get('celular')
        correo = data.get('correo')
        contrasena = data.get('contrasena')
        direccion =data.get('direccion')
        res = ModeloUsuario.registrar(db,nombre,apellido,celular,correo,direccion,contrasena)
        if isinstance(res, int) and res > 0:
            return jsonify({'mensaje': 'Usuario registrado exitosamente'})
        elif res is None:
            return jsonify({'mensaje': 'El usuario ya existe'})
        elif isinstance(res, str) and res.startswith("Error al registrar"):
            return jsonify({'mensaje': res})
        else:
            return jsonify({'mensaje': 'Error desconocido al registrar'})

    return render_template('registro.html')

#ruta para obtener los usuarios
@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    if 'usuario' not in session or session['usuario']['rol'] != 1:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    try:
        usuarios = ModeloUsuario.obtenerUsuarios(db)
        return jsonify(usuarios)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#ruta para bloquear usuarios
@app.route('/api/bloquear-usuario/<int:id_usuario>', methods=['PUT'])
def bloquear_usuario(id_usuario):
    respuesta = ModeloUsuario.bloquearUsuarios(db, id_usuario)
    if int(respuesta) > 0:
        return jsonify({'mensaje': 'Usuario bloqueado exitosamente'}), 200
    else:
        return jsonify({'error': 'No se pudo bloquear el usuario'}), 500

    
@app.route('/api/activar-usuario/<int:id_usuario>', methods=['PUT'])
def activar_usuario(id_usuario):
    respuesta = ModeloUsuario.desbloquearUsuarios(db, id_usuario)
    if int(respuesta) > 0:
        return jsonify({"mensaje": "Usuario activado correctamente"}), 200
    else:
        return jsonify({"error": "No se pudo activar el usuario"}), 500



@app.route('/api/eliminar-usuario/<int:id_usuario>', methods=['PUT'])
def eliminar_usuario(id_usuario):
    if 'usuario' not in session or session['usuario']['rol'] != 1:
        return jsonify({'error': 'Acceso denegado'}), 403

    respuesta = ModeloUsuario.eliminarUsuario(db, id_usuario)

    if isinstance(respuesta, int) and respuesta == 0:
        return jsonify({'error': 'Error al eliminar el usuario'}), 500

    return jsonify({'mensaje': 'Usuario eliminado exitosamente'})



@app.route('/api/desbloquear-usuario/<int:id_usuario>', methods=['PUT'])
def desbloquear_usuario(id_usuario):
    if 'usuario' not in session or session['usuario']['rol'] != 1:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    respuesta = ModeloUsuario.desbloqueraUsuarios(db, id_usuario)
    
    if isinstance(respuesta, int) and respuesta == 0:
        return jsonify({'error': 'Error al desbloquear el usuario'}), 500
    
    return jsonify({'mensaje': 'Usuario desbloqueado exitosamente'})



@app.route('/api/registrar-producto', methods=['POST'])
def registrar_producto():
    if 'usuario' not in session or session['usuario']['rol'] != 1:
        return jsonify({'error': 'Acceso denegado'}), 403

    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    imagen = request.files.get('imagen')

    # Carpeta absoluta a static/img
    ruta_carpeta = os.path.join(app.root_path, 'static', 'img')
    os.makedirs(ruta_carpeta, exist_ok=True)  # Asegura que la carpeta existe

    if imagen:
        nombre_seguro = secure_filename(imagen.filename)  # Evita nombres peligrosos
        ruta_imagen = os.path.join(ruta_carpeta, nombre_seguro)
        imagen.save(ruta_imagen)
        nombre_imagen = nombre_seguro
    else:
        nombre_imagen = 'default.jpg'

    respuesta = ProductoModelo.registrar_producto(db, nombre, descripcion, precio, nombre_imagen)

    if respuesta is None:
        return jsonify({'error': 'Error al registrar el producto'}), 500

    return jsonify({'mensaje': 'Producto registrado exitosamente'})


#ruta para obtener los productos
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    try:
        productos = ProductoModelo.obtener_productos(db)
        return jsonify(productos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#ruta para obtener pedidos de usuario
@app.route('/api/pedidos-usuario', methods=['GET'])
def obtener_pedidos_usuario():
    if 'usuario' not in session:
        return jsonify({'error': 'No ha iniciado sesión'}), 401
    
    id_usuario = session['usuario']['id']
    
    try:
        pedidos = CompraModelo.obtener_pedidos_usuario(db, id_usuario)
        return jsonify(pedidos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#ruta para obtener pedidos
@app.route('/api/pedidos/actualizar/<int:id>', methods=['PUT'])
def actualizar_pedido(id):
    if 'usuario' not in session or session['usuario']['rol'] != 1:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    estado = request.json.get('estado')
    id_usuario = request.json.get('id_usuario')
    
    respuesta = CompraModelo.actualizarPedido(db, id,estado)

    if estado == 'terminado':
        return jsonify({'mensaje': 'Pedido actualizado exitosamente'})

    if respuesta is None:
        return jsonify({'error': 'Error al actualizar el pedido'}), 500
    else:    
        usuario = ModeloUsuario.obtenerUsuarioPorId(db, id_usuario)

        color_estado = "#28a745" if estado == "aceptado" else "#dc3545"
        mensaje_estado = "¡Tu pedido ha sido aceptado!" if estado == "aceptado" else "Lamentamos informarte que tu pedido ha sido rechazado."

        msg = Message('Estado de tu pedido', recipients=[usuario[4]])

        msg.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .container {{
                    font-family: Arial, sans-serif;
                    max-width: 600px;
                    margin: auto;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    background-color: #f9f9f9;
                }}
                .header {{
                    background-color: {color_estado};
                    color: white;
                    padding: 15px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .body {{
                    padding: 20px;
                    text-align: center;
                }}
                .footer {{
                    margin-top: 30px;
                    font-size: 0.9em;
                    color: #555;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Estado de tu Pedido</h2>
                </div>
                <div class="body">
                    <p style="font-size: 18px;">{mensaje_estado}</p>
                    <p>Gracias por confiar en nosotros.</p>
                </div>
                <div class="footer">
                    <p>Este mensaje fue generado automáticamente. No respondas a este correo.</p>
                </div>
            </div>
        </body>
        </html>
        """

        try:
            threading.Thread(target=enviar_correo_async, args=(app, msg)).start()
            return jsonify({'mensaje': 'Pedido actualizado exitosamente'})
        except Exception as e:
            return jsonify({'error': 'No se pudo enviar el correo'}), 500

#ruta para eliminar productos
@app.route('/api/eliminar-producto/<int:id>', methods=['PUT'])
def eliminar_producto(id):
    if 'usuario' not in session or session['usuario']['rol'] != 1:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    respuesta = ProductoModelo.eliminar_producto(db, id)
    
    if respuesta is None:
        return jsonify({'error': 'Error al eliminar el producto'}), 500
    
    return jsonify({'mensaje': 'Producto eliminado exitosamente'})

#ruta para recuperar contraseña
@app.route('/recuperar-contraseña',methods=['POST'])
def recuperar_contra():
    correo = request.json.get('correo')

    if not correo:
        return jsonify({'error': 'El correo es obligatorio'}), 400

    usuario_encontrado = ModeloUsuario.obtenerUsuarioPorCorreo(db,correo)
    if usuario_encontrado is None:
        return jsonify({'error':'El correo ingresado no aceptado'}), 404
    
    
    id_usuario = usuario_encontrado[0]

    contraseña = ModeloUsuario.generarContraseña()

    contra_actualizada = ModeloUsuario.actualizar_contraseña(db,id_usuario,contraseña)
    if contra_actualizada == 0:
        return jsonify({'error':'No se pudo cambiar la contraseña'}) , 400
    else:
        print(contra_actualizada)
        msg = Message('Recuperación de Contraseña', recipients=[usuario_encontrado[4]])

        msg.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f4f6f8;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    background-color: #ffffff;
                    max-width: 600px;
                    margin: 30px auto;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }}
                .header {{
                    background-color: #007bff;
                    padding: 20px;
                    color: white;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    padding: 20px;
                    text-align: center;
                }}
                .content p {{
                    font-size: 16px;
                    color: #333;
                }}
                .password-box {{
                    font-size: 22px;
                    font-weight: bold;
                    color: #007bff;
                    background-color: #e9f2ff;
                    padding: 10px;
                    margin: 20px auto;
                    border-radius: 5px;
                    display: inline-block;
                }}
                .footer {{
                    text-align: center;
                    font-size: 13px;
                    color: #777;
                    margin-top: 30px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Recuperación de Contraseña</h2>
                </div>
                <div class="content">
                    <p>Hola, hemos generado una nueva contraseña para tu cuenta en AvenaCorp.</p>
                    <p>Tu nueva contraseña es:</p>
                    <div class="password-box">{contraseña}</div>
                </div>
                <div class="footer">
                    <p>Este mensaje fue enviado automáticamente. No respondas a este correo.</p>
                </div>
            </div>
        </body>
        </html>
        """


        try:
            threading.Thread(target=enviar_correo_async, args=(app, msg)).start()
            return jsonify({'mensaje': 'Contraseña enviada exitosamente'})
        except Exception as e:
            return jsonify({'error': 'No se pudo enviar el correo'}), 500
        
@app.route('/cambiar_password', methods=['POST'])
def cambiar_password():
    data = request.get_json()
    actual = data.get('actual')
    nueva = data.get('nueva')
    confirmar = data.get('confirmar')

    if nueva != confirmar:
        return jsonify({'exito': False, 'mensaje': 'Las contraseñas no coinciden'})

    correo = session['usuario']['correo']

    if not correo:
        return jsonify({'exito': False, 'mensaje': 'Usuario no autenticado'})

    resultado = ModeloUsuario.obtenerContrasena(db,correo)
    if resultado and check_password_hash(resultado[0], actual):

        usuario_encontrado = ModeloUsuario.obtenerUsuarioPorCorreo(db,correo)
        if usuario_encontrado is None:
            return jsonify({'error':'El correo ingresado no aceptado'}), 404
        
        
        id_usuario = usuario_encontrado[0]

        actualizada = ModeloUsuario.actualizar_contraseña(db,id_usuario,nueva)

        if actualizada > 0:
            return jsonify({'exito': True, 'mensaje': 'Contraseña actualizada con éxito'})

        return jsonify({'exito': False, 'mensaje': 'Contraseña no se pudo modificar'})

    else:
        return jsonify({'exito': False, 'mensaje': 'Contraseña actual incorrecta'})
    
#ruta para obtener pedidos
@app.route('/api/pedidos', methods=['GET'])
def obtener_pedidos():
    if 'usuario' not in session or session['usuario']['rol'] != 1:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    try:
        pedidos = CompraModelo.obtener_pedidos(db)
        return jsonify(pedidos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#ruta para obtener historial de pedidos
@app.route('/api/historial', methods=['GET'])
def obtener_historial():
    if 'usuario' not in session or session['usuario']['rol'] != 1:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    try:
        historial= CompraModelo.obtener_historial(db)
        return jsonify(historial)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#ruta para los pedidos pendientes
@app.route('/api/pedidos-pendientes', methods=['GET'])
def pedidos_pendientes():
    if 'usuario' not in session or session['usuario']['rol'] != 1:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    try:
        pendientes = CompraModelo.obtener_pendientes(db)
        return jsonify({'cantidad': pendientes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#ruta para actualizar productos
@app.route('/api/actualizar-producto', methods=['POST'])
def actualizar_producto():
    if 'usuario' not in session or session['usuario']['rol'] != 1:
        return jsonify({'error': 'Acceso denegado'}), 403

    id = request.form.get('editar-id')
    nombre = request.form.get('editar-nombre')
    descripcion = request.form.get('editar-descripcion')
    precio = request.form.get('editar-precio')
    imagen = request.files.get('editar-imagen')

    # Procesar imagen si se envió
    if imagen:
        ruta_carpeta = os.path.join(app.root_path, 'static', 'img')
        os.makedirs(ruta_carpeta, exist_ok=True)

        nombre_seguro = secure_filename(imagen.filename)
        ruta_imagen_completa = os.path.join(ruta_carpeta, nombre_seguro)
        imagen.save(ruta_imagen_completa)
        nombre_imagen = nombre_seguro
    else:
        nombre_imagen = None  # Se mantiene la anterior (el modelo debe manejar esto)

    # Llamada al modelo para actualizar
    respuesta = ProductoModelo.actualizar_producto(
        db, id, nombre, descripcion, precio, nombre_imagen
    )

    if respuesta is None:
        print("Error al actualizar el producto")
        return jsonify({'error': 'Error al actualizar el producto'}), 500

    return jsonify({'mensaje': 'Producto actualizado exitosamente'})


#ruta para comprar productos
@app.route('/api/comprar-producto', methods=['POST'])
def comprar_producto():
    if 'usuario' not in session:
        return jsonify({'error': 'No ha iniciado sesión'}), 401
    
    usuario = session['usuario']
    id_producto = request.json.get('id_producto')
    cantidad = request.json.get('cantidad', 1)  # Por defecto, comprar 1 unidad
    fecha = request.json.get('fecha')
    total = request.json.get('total')

    compra_realizada = CompraModelo.registrar_compra(db, usuario['id'], id_producto, cantidad, fecha, total)
    if compra_realizada is None:
        return jsonify({'error': 'Error al realizar la compra'}), 500
    return jsonify({'mensaje': 'Producto comprado exitosamente'})


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

#manejo de errores
@app.errorhandler(404)
def fallback(e):
    return redirect(url_for('login'))

# --- Ejecutar servidor ---
if __name__ == "__main__":
    #trae la configuracion desde el archivo config.py
    app.config.from_object(config["development"]) 
    app.run()
