cargarUsuarios();

document.getElementById("filtro-estado").addEventListener("change", function () {
  cargarUsuarios(this.value);
});


function mostrarModalMensaje(mensaje, esError = false) {
  const modalTexto = document.getElementById("textoMensaje");
  modalTexto.textContent = mensaje;
  modalTexto.style.color = esError ? "red" : "green";
  document.getElementById("modalMensaje").style.display = "flex";
}

function cerrarModalMensaje() {
  document.getElementById("modalMensaje").style.display = "none";
}

const toggleBtn = document.getElementById("toggleMenu");
const sidebar = document.getElementById("sidebarMenu");

toggleBtn.addEventListener("click", e => {
  e.stopPropagation();
  sidebar.classList.toggle("active");
});

document.addEventListener("click", () => {
  sidebar.classList.remove("active");
});

sidebar.addEventListener("click", e => {
  e.stopPropagation();
});

let usuarioSeleccionado = null;

function abrirModal(id, nombre) {
  usuarioSeleccionado = id;
  document.getElementById("mensajeModal").textContent = `¿Estás seguro de que deseas bloquear a "${nombre}" (ID: ${id})?`;
  document.getElementById("modalConfirmacion").style.display = "flex";
}

function cerrarModal() {
  document.getElementById("modalConfirmacion").style.display = "none";
  usuarioSeleccionado = null;
}

async function confirmarBloqueo() {
  if (usuarioSeleccionado !== null) {
    const res = await fetch(`/api/bloquear-usuario/${usuarioSeleccionado}`, { method: 'PUT' });
    if (res.ok) {
      mostrarModalMensaje("Usuario bloqueado exitosamente.");
      setTimeout(() => cerrarModalMensaje(), 2000);
      cargarUsuarios();
    } else {
      mostrarModalMensaje("Error al bloquear el usuario.", true);
      setTimeout(() => cerrarModalMensaje(), 2000);
    }
    cerrarModal();
  }
}

async function activarUsuario(id) {
  if (!confirm("¿Deseas activar este usuario?")) return;
  const res = await fetch(`/api/activar-usuario/${id}`, { method: 'PUT' });
  const data = await res.json();

  if (res.ok) {
    mostrarModalMensaje("Usuario activado correctamente");
    cargarUsuarios();
  } else {
    mostrarModalMensaje(data.error || "Error al activar usuario", true);
  }

  setTimeout(() => cerrarModalMensaje(), 2000);
}

async function eliminarUsuario(id) {
  if (!confirm("¿Estás seguro de eliminar este usuario?")) return;
  const res = await fetch(`/api/eliminar-usuario/${id}`, { method: 'PUT' });
  const data = await res.json();

  if (res.ok) {
    mostrarModalMensaje("Usuario eliminado correctamente");
    cargarUsuarios();
  } else {
    mostrarModalMensaje(data.error || "Error al eliminar usuario", true);
  }

  setTimeout(() => cerrarModalMensaje(), 2000);
}

async function cargarUsuarios(filtroEstado = "") {
  const tabla = document.getElementById("tabla-usuarios");
  tabla.innerHTML = "";

  const res = await fetch("/api/usuarios");
  if (!res.ok) {
    mostrarModalMensaje("Error al cargar usuarios", true);
    return;
  }

  const usuarios = await res.json();
  const usuariosFiltrados = filtroEstado
    ? usuarios.filter(u => u.estado === filtroEstado)
    : usuarios;

  if (usuariosFiltrados.length === 0) {
    const fila = document.createElement("tr");
    fila.innerHTML = "<td colspan='7'>No hay usuarios disponibles</td>";
    tabla.appendChild(fila);
    return;
  }

  usuariosFiltrados.forEach(u => {
    const fila = document.createElement("tr");
    const estadoHTML = u.estado === 'activo'
      ? `<span class="estado estado-activo">Activo</span>`
      : u.estado === 'inactivo'
        ? `<span class="estado estado-bloqueado">Bloqueado</span>`
        : `<span class="estado estado-eliminado">Eliminado</span>`;

    let acciones = "";

    if (u.estado === 'activo') {
      acciones += `<button onclick="abrirModal(${u.id}, '${u.nombre}')">Bloquear</button>`;
    } else if (u.estado === 'inactivo') {
      acciones += `<button onclick="activarUsuario(${u.id})">Activar</button>`;
    }

    if (u.estado !== 'eliminado') {
      acciones += `<button onclick="eliminarUsuario(${u.id})">Eliminar</button>`;
    }

      fila.innerHTML = `
        <td>${u.id}</td>
        <td>${u.nombre}</td>
        <td>${u.apellido}</td>
        <td>${u.correo}</td>
        <td>${u.celular}</td>
        <td>${estadoHTML}</td>
        <td>${acciones}</td>
      `;
      tabla.appendChild(fila);
    });
  }

window.addEventListener('DOMContentLoaded', async () => {
  // Obtener y mostrar nombre del usuario
  try {
    const res = await fetch('/api/usuario-logueado');
    if (res.ok) {
      const usuario = await res.json();
      const nombre = usuario.nombre || "Invitado";
      document.getElementById("nombre-usuario").textContent = nombre;
    } else {
      document.getElementById("nombre-usuario").textContent = "Invitado";
    }
  } catch (err) {
    console.error("Error al obtener usuario logueado:", err);
    document.getElementById("nombre-usuario").textContent = "Invitado";
  }

  // Cargar usuarios al iniciar
  cargarUsuarios();
});


