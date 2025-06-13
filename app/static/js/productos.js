    function mostrarModalMensaje(mensaje, esError = false) {
      const modalTexto = document.getElementById("textoMensaje");
      modalTexto.textContent = mensaje;
      modalTexto.style.color = esError ? "red" : "green";
      document.getElementById("modalMensaje").style.display = "flex";
    }

    function cerrarModalMensaje() {
      document.getElementById("modalMensaje").style.display = "none";
    }

    window.addEventListener('DOMContentLoaded', async () => {
      const res = await fetch('/api/usuario-logueado');
      if (res.ok) {
        const usuario = await res.json();
        document.getElementById("nombre-usuario").textContent = usuario.nombre;
      }
    });
    cargarProductos();
    const toggleBtn = document.getElementById("toggleMenu");
    const sidebar = document.getElementById("sidebarMenu");

    toggleBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      sidebar.classList.toggle("active");
    });


    sidebar.addEventListener("click", function (e) {
      e.stopPropagation();
    });

    document.addEventListener("click", function () {
      if (sidebar.classList.contains("active")) {
        sidebar.classList.remove("active");
      }
    });

    function abrirModal(id) {
        document.getElementById(id).style.display = 'block';
    }

    function cerrarModal(id) {
        document.getElementById(id).style.display = 'none';
    }



    const formulario = document.getElementById('formAgregarProducto');
    formulario.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(formulario);

        const res = await fetch('/api/registrar-producto', {
            method: 'POST',
            body: formData // No establezcas Content-Type, el navegador lo hará
        });

        if (res.ok) {
            formulario.reset();
            cerrarModal('modalAgregar');
            mostrarModalMensaje('Producto registrado exitosamente');
            setTimeout(() => {
                cerrarModalMensaje();
            }, 2000);
            cargarProductos();
        } else {
            mostrarModalMensaje('Error al registrar el producto', true);
            setTimeout(() => {
                cerrarModalMensaje();
            }, 2000);
        }
    });

    const formularioEditar = document.getElementById('formEditarProducto');
    formularioEditar.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formDataActualizar = new FormData(formularioEditar);

        const res = await fetch(`/api/actualizar-producto`, {
            method: 'POST',
            body: formDataActualizar
        });

        if (res.ok) {
            cerrarModal('modalEditar');
            mostrarModalMensaje('Producto actualizado exitosamente');
            setTimeout(() => {
                cerrarModalMensaje();
            }, 2000);
            cargarProductos();
        } else {
            cerrarModal('modalEditar');
            mostrarModalMensaje('Error al actualizar el producto', true);
            setTimeout(() => {
                cerrarModalMensaje();
            }, 2000);
        }
    })
    
    const formularioEliminar = document.getElementById('formEliminarProducto');
    formularioEliminar.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('eliminar-id').value;

        const res = await fetch(`/api/eliminar-producto/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        if (res.ok) {
            cerrarModal('modalEliminar');
            mostrarModalMensaje('Producto eliminado exitosamente');
            setTimeout(() => {
                cerrarModalMensaje();
            }, 2000);
            cargarProductos()
        } else {
            mostrarModalMensaje('Error al eliminar el producto', true);
            setTimeout(() => {
                cerrarModalMensaje();
            }, 2000);
        }
    });

    // Función para cargar productos al iniciar
    async function cargarProductos() {
        const res = await fetch('/api/productos');

        if (!res.ok) {
            mostrarModalMensaje('Error al cargar productos', true);
            setTimeout(() => {
                cerrarModalMensaje();
            }, 2000);
            document.querySelector('.tabla-productos tbody').innerHTML = '<tr><td colspan="6">Error al cargar productos.</td></tr>';
            return;
        }

        const productos = await res.json();

        if (!Array.isArray(productos) || productos.length === 0) {
            document.querySelector('.tabla-productos tbody').innerHTML = '<tr><td colspan="6">No hay productos disponibles.</td></tr>';
            return;
        }
        const tbody = document.querySelector('.tabla-productos tbody');
        tbody.innerHTML = ''; // Limpia antes de insertar

        productos.forEach(producto => {
        const fila = document.createElement('tr');
        fila.innerHTML = `
            <td>${producto.id}</td>
            <td>${producto.nombre_producto}</td>
            <td>${producto.descripcion}</td>
            <td>${producto.precio_producto}</td>
            <td><img class="imagenProducto" src="../static/img/${producto.imagen}"></img></td>
            <td class="acciones">
            <button onclick="abrirModalEditar(${producto.id}, '${producto.nombre_producto}', '${producto.descripcion}', ${producto.precio_producto})">Editar</button>
            <button onclick="abrirModalEliminar(${producto.id},'${producto.nombre_producto}', '${producto.descripcion}')">Eliminar</button>
            </td>
        `;
        tbody.appendChild(fila);
        });
    }

    // Rellenar modal de edición
    function abrirModalEditar(id, nombre, descripcion, precio) {
        document.getElementById('modalEditar').style.display = 'block';
        document.getElementById('editar-id').value = id;
        document.getElementById('editar-nombre').value = nombre;
        document.getElementById('editar-descripcion').value = descripcion;
        document.getElementById('editar-precio').value = precio;
    }

    // Rellenar modal de eliminación
    function abrirModalEliminar(id,nombre,descripcion) {
        document.getElementById('modalEliminar').style.display = 'block';
        document.getElementById('eliminar-id').value = id;
        document.getElementById('nombre_producto').textContent = `Nombre: ${nombre}`;
        document.getElementById('descripcion_producto').textContent = `Descripción: ${descripcion}`;

    }

    function abrirModalCambio() {
  document.getElementById("modalCambio").style.display = "flex";
}

function cerrarModalCambio() {
  document.getElementById("modalCambio").style.display = "none";
}

function enviarCambio(e) {
  e.preventDefault();

  const form = document.getElementById("formCambio");
  const actual = form.actual.value;
  const nueva = form.nueva.value;
  const confirmar = form.confirmar.value;

  if (nueva !== confirmar) {
    mostrarModalMensaje("Las contraseñas no coinciden", true);
    setTimeout(cerrarModalMensaje, 2000);
    return;
  }

  fetch("/cambiar_password", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ actual, nueva, confirmar })
  })
    .then(res => res.json())
    .then(data => {
      mostrarModalMensaje(data.mensaje, !data.exito);
      if (data.exito) {
        form.reset();
        cerrarModalCambio();
      }
      setTimeout(cerrarModalMensaje, 2000);
    })
    .catch(err => {
      mostrarModalMensaje("Error al cambiar contraseña", true);
      setTimeout(cerrarModalMensaje, 2000);
    });
}
