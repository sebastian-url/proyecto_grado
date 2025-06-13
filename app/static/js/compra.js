    // Mostrar/Ocultar menú lateral
    document.getElementById('toggleMenu').addEventListener('click', () => {
      document.getElementById('sidebarMenu').classList.toggle('visible');
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

    // Obtener pedidos del backend
    document.addEventListener('DOMContentLoaded', async () => {
      try {
        const res = await fetch('/api/pedidos-usuario');
        const pedidos = await res.json();

        if (pedidos.length === 0) {
          const tbody = document.querySelector('#tablaPedidos tbody');
          tbody.innerHTML = '<tr><td colspan="7" style="text-align: center;">No hay pedidos realizados.</td></tr>';
          return;
        }
        const tbody = document.querySelector('#tablaPedidos tbody');

        pedidos.forEach(p => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${p.producto}</td>
            <td>${p.descripcion}</td>
            <td>$${p.precio.toFixed(2)}</td>
            <td>${p.cantidad}</td>
            <td>$${(p.precio * p.cantidad).toFixed(2)}</td>
            <td>${new Date(p.fecha).toLocaleDateString()}</td>
            <td class="estado ${p.estado === 'procesando' ? 'procesando' : 'aceptado'}">${p.estado}</td>
          `;
          tbody.appendChild(tr);
        });
      } catch (error) {
        console.error('Error al cargar pedidos:', error);
      }
    });

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
