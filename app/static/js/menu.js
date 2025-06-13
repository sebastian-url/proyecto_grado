const toggleBtn = document.getElementById("toggleMenu");
const sidebar = document.getElementById("sidebarMenu");

// Mostrar u ocultar el menú al hacer clic en el botón ☰
toggleBtn.addEventListener("click", function (e) {
  e.stopPropagation(); // Evita que el clic se propague y dispare el cierre
  sidebar.classList.toggle("active");
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
// Cierra el menú si se hace clic fuera de él
document.addEventListener("click", function () {
  if (sidebar.classList.contains("active")) {
    sidebar.classList.remove("active");
  }
});

    (async () => {
      try {
        const res = await fetch('/api/pedidos-pendientes');
        if (res.ok) {
          const { cantidad } = await res.json();
          if (cantidad > 0) {
            document.getElementById('cantidad-pedidos').textContent = cantidad;
            document.getElementById('alerta-pedidos').style.display = 'block';
          }
        }
      } catch (err) {
        console.error('Error al consultar pedidos pendientes:', err);
      }
    })();



    const logoutBtn = document.getElementById("logout");
    window.addEventListener('DOMContentLoaded', async () => {
      const res = await fetch('/api/usuario-logueado');
      if (res.ok) {
        const usuario = await res.json();
        document.getElementById("nombre-usuario").textContent = usuario.nombre;
      } else {
        window.location.href = "/login";
      }
    });
    
    window.addEventListener('DOMContentLoaded', async () => {
      const esAdmin = await fetch('/api/admin-only');
      if (!esAdmin.ok) {
        window.location.href = "/catalogo";
      }
    });

    logoutBtn.addEventListener('click', async () => {
      const res = await fetch('/logout',{            
          method: "POST",
          headers: { "Content-Type": "application/json" }
      });
    });

function abrirModalCambio() {
  document.getElementById("modalCambio").style.display = "flex";
}

function cerrarModalCambio() {
  document.getElementById("modalCambio").style.display = "none";
}

async function enviarCambio(e) {
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

  await fetch("/cambiar_password", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ actual, nueva, confirmar })
  })
    .then(res => res.json())
    .then(data => {
      cerrarModalCambio();
      mostrarModalMensaje(data.mensaje, !data.exito);
      if (data.exito) {
        form.reset();
      }
      setTimeout(cerrarModalMensaje, 2000);
    })
    .catch(err => {
      cerrarModalCambio();
      mostrarModalMensaje("Error al cambiar contraseña", true);
      setTimeout(cerrarModalMensaje, 2000);
    });
}
