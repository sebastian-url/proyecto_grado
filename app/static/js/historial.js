    const tbody = document.querySelector("table tbody");

    function mostrarModalMensaje(mensaje, esError = false) {
      const modalTexto = document.getElementById("textoMensaje");
      modalTexto.textContent = mensaje;
      modalTexto.style.color = esError ? "red" : "green";
      document.getElementById("modalMensaje").style.display = "flex";
    }


    function cerrarModalMensaje() {
      document.getElementById("modalMensaje").style.display = "none";
    }

    async function cargarHistorialDePedidos() {
      try {
        const res = await fetch('/api/historial');
        if (!res.ok) throw new Error('Error al obtener los pedidos');
        const pedidos = await res.json();

        if (pedidos.length === 0) {
          const fila = document.createElement("tr");
          fila.innerHTML = "<td colspan='4'>No hay pedidos terminados</td>";
          tbody.appendChild(fila);
          return;
        }
        tbody.innerHTML = ""; // Limpia contenido actual (si hay)

        pedidos.forEach(pedido => {
          const fila = document.createElement("tr");

          const fecha = document.createElement("td");
          fecha.textContent = new Date(pedido.fecha).toLocaleDateString('es-ES');

          const producto = document.createElement("td");
          producto.textContent = pedido.producto;

          const cantidad = document.createElement("td");
          cantidad.textContent = pedido.cantidad;

          const total = document.createElement("td");
          total.textContent = `$${pedido.total.toLocaleString('es-CO')}`;

          fila.appendChild(fecha);
          fila.appendChild(producto);
          fila.appendChild(cantidad);
          fila.appendChild(total);

          tbody.appendChild(fila);
        });
      } catch (error) {
        console.error("Error al cargar historial de pedidos:", error);
      }
    }

    window.addEventListener('DOMContentLoaded', async () => {
      // Mostrar nombre de usuario
      const res = await fetch('/api/usuario-logueado');
      if (res.ok) {
        const usuario = await res.json();
        document.getElementById("nombre-usuario").textContent = usuario.nombre;
      }else{
        window.location.href = '/index'
      }

      // Cargar pedidos
      await cargarHistorialDePedidos();
    });


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
