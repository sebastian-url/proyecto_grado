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

  cargarProductos();
});

// Menú lateral
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
  const modal = document.getElementById(id);
  if (!modal) {
    console.error("No se encontró el modal con id:", id);
    return;
  }
  modal.style.display = 'block';
}

function cerrarModal(idModal) {
  const modal = document.getElementById(idModal);
  if (modal) {
    modal.style.display = 'none';
  }
}

// Manejador para registrar producto (único y corregido)
document.getElementById("formAgregarProducto").addEventListener("submit", async function (e) {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);

  const res = await fetch("/api/registrar-producto", {
    method: "POST",
    body: formData
  });

  const data = await res.json();

  if (res.ok) {
    mostrarModalMensaje("Producto registrado exitosamente");
    cerrarModal("modalAgregar");
    form.reset(); // Limpia el formulario
    cargarProductos(); // Refresca la tabla
  } else {
    mostrarModalMensaje(data.error || "Error al registrar producto", true);
  }

  setTimeout(() => cerrarModalMensaje(), 2500);
});

// Manejador para editar producto
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
    cargarProductos();
  } else {
    cerrarModal('modalEditar');
    mostrarModalMensaje('Error al actualizar el producto', true);
  }

  setTimeout(() => cerrarModalMensaje(), 2000);
});

// Manejador para eliminar producto
const formularioEliminar = document.getElementById('formEliminarProducto');
formularioEliminar.addEventListener('submit', async (e) => {
  e.preventDefault();

  const id = document.getElementById('eliminar-id').value;

  if (!id || isNaN(id)) {
    console.error("ID inválido para eliminación:", id);
    mostrarModalMensaje('ID de producto no válido', true);
    return;
  }

  console.log("Eliminando producto ID:", id); // <-- Confirma que esté correcto

  const res = await fetch(`/api/eliminar-producto/${id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include'
  });

  if (res.ok) {
    cerrarModal('modalEliminar');
    mostrarModalMensaje('Producto eliminado exitosamente');
    cargarProductos();
  } else {
    mostrarModalMensaje('Error al eliminar el producto', true);
  }

  setTimeout(() => cerrarModalMensaje(), 2000);
});

// Función para cargar productos
async function cargarProductos() {
  const res = await fetch('/api/productos');

  if (!res.ok) {
    mostrarModalMensaje('Error al cargar productos', true);
    document.querySelector('.tabla-productos tbody').innerHTML = '<tr><td colspan="6">Error al cargar productos.</td></tr>';
    setTimeout(() => cerrarModalMensaje(), 2000);
    return;
  }

  const productos = await res.json();

  console.log("Respuesta productos:", productos);  // ✅ Línea agregada

  const tbody = document.querySelector('.tabla-productos tbody');
  tbody.innerHTML = '';

  if (!Array.isArray(productos) || productos.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6">No hay productos disponibles.</td></tr>';
    return;
  }

  productos.forEach((producto, index) => {
    const fila = document.createElement('tr');
    fila.innerHTML = `
      <td>${index + 1}</td>
      <td>${producto.nombre_producto}</td>
      <td>${producto.descripcion}</td>
      <td>${producto.precio_producto}</td>
      <td><img class="imagenProducto" src="../static/img/${producto.imagen}" width="80"></td>
      <td class="acciones">
          <button onclick="abrirModalEditar(${producto.id_producto}, '${producto.nombre_producto}', '${producto.descripcion}', ${producto.precio_producto})">Editar</button>
          <button onclick="abrirModalEliminar(${producto.id_producto}, '${producto.nombre_producto}', '${producto.descripcion}')">Eliminar</button>
      </td>
    `;
    tbody.appendChild(fila);
  });
}



// Modal editar producto
function abrirModalEditar(id, nombre, descripcion, precio) {
  document.getElementById('modalEditar').style.display = 'block';
  document.getElementById('editar-id').value = id;
  document.getElementById('editar-nombre').value = nombre;
  document.getElementById('editar-descripcion').value = descripcion;
  document.getElementById('editar-precio').value = precio;
}

// Modal eliminar producto
function abrirModalEliminar(id, nombre, descripcion) {
  document.getElementById('modalEliminar').style.display = 'block';
  document.getElementById('eliminar-id').value = id;
  document.getElementById('nombre_producto').textContent = `Nombre: ${nombre}`;
  document.getElementById('descripcion_producto').textContent = `Descripción: ${descripcion}`;
}


// Modal cambio de contraseña
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
