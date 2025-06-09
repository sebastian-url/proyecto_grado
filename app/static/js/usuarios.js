    cargarUsuarios();

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
          setTimeout(() => {
            cerrarModalMensaje();
          }, 2000);
          cargarUsuarios();
        } else {
          mostrarModalMensaje("Error al bloquear el usuario.", true);
          setTimeout(() => {
            cerrarModalMensaje();
          }, 2000);
        }
        cerrarModal();
      }
    }

    async function cargarUsuarios() {
      const tabla = document.getElementById("tabla-usuarios");
      tabla.innerHTML = "";
      const res = await fetch("/api/usuarios");
      if (res.ok) {
        const usuarios = await res.json();
        if (usuarios.length === 0) {
          const fila = document.createElement("tr");
          fila.innerHTML = "<td colspan='6'>No hay usuarios disponibles</td>";
          tabla.appendChild(fila);
          return;
        }
        usuarios.forEach(u => {
          const fila = document.createElement("tr");
          fila.innerHTML = `
            <td>${u.id}</td>
            <td>${u.nombre}</td>
            <td>${u.apellido}</td>
            <td>${u.correo}</td>
            <td>${u.celular}</td>
            <td><button class="btn-bloquear" onclick="abrirModal(${u.id}, '${u.nombre}')">Bloquear</button></td>
          `;
          tabla.appendChild(fila);
        });
      }
    }

    window.addEventListener('DOMContentLoaded', async () => {
      const res = await fetch('/api/usuario-logueado');
      if (res.ok) {
        const usuario = await res.json();
        document.getElementById("nombre-usuario").textContent = usuario.nombre;
      }
    });