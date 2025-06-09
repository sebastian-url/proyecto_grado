    cargarPedidos();

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

    async function cargarPedidos() {
      const tabla = document.getElementById("tabla-pedidos");
      tabla.innerHTML = "";
      const res = await fetch("/api/pedidos");
      if (res.ok) {
        const pedidos = await res.json();
        if (pedidos.length === 0) {
          const fila = document.createElement("tr");
          fila.innerHTML = "<td colspan='11'>No hay pedidos disponibles</td>";
          tabla.appendChild(fila);
          return;
        }
        pedidos.forEach(p => {
          const fila = document.createElement("tr");
          fila.innerHTML = `
            <td>${p.usuario}</td>
            <td>${p.celular}</td>
            <td>${p.producto}</td>
            <td>${p.descripcion}</td>
            <td>${p.cantidad}</td>
            <td>$${p.precio.toFixed(2)}</td>
            <td>${
                (() => {
                    const fecha = new Date(p.fecha);
                    const dia = String(fecha.getDate()).padStart(2, '0');
                    const mes = String(fecha.getMonth() + 1).padStart(2, '0');
                    const año = fecha.getFullYear();
                    return `${dia}-${mes}-${año}`;
                })()
            }</td>

            <td>${p.estado}</td>
            <td>$${p.total.toFixed(2)}</td>
            <td>
              <button class="btn-accion btn-aceptar" onclick="actualizarPedido(${p.id_compra}, 'aceptado',${p.id_usuario})">Aceptar</button>
              <button class="btn-accion btn-enviar" onclick="actualizarPedido(${p.id_compra}, 'cancelado',${p.id_usuario})">Rechazar</button>
              <button class="btn-accion btn-enviar" onclick="actualizarPedido(${p.id_compra}, 'terminado',${p.id_usuario})">Terminar</button>
            </td>
          `;
          tabla.appendChild(fila);
        });
      }
    }

    async function actualizarPedido(id, nuevoEstado,id_usuario) {
      const res = await fetch(`/api/pedidos/actualizar/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ estado: nuevoEstado , id_usuario: id_usuario })
      });

      if (res.ok) {
        mostrarModalMensaje(`Pedido ${nuevoEstado} correctamente.`);
        setTimeout(() => {
          cerrarModalMensaje();
        }, 2000);
        cargarPedidos();
      } else {
        mostrarModalMensaje("Error al actualizar el pedido.", true);
        setTimeout(() => {
          cerrarModalMensaje();
        }, 2000);
      }
    }

    window.addEventListener('DOMContentLoaded', async () => {
      const res = await fetch('/api/usuario-logueado');
      if (res.ok) {
        const usuario = await res.json();
        document.getElementById("nombre-usuario").textContent = usuario.nombre;
      }
    });