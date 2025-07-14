function mostrarModalMensaje(mensaje, esError = false) {
  const modalTexto = document.getElementById("textoMensaje");
  modalTexto.textContent = mensaje;
  modalTexto.style.color = esError ? "red" : "green";
  document.getElementById("modalMensaje").style.display = "flex";
}

function cerrarModalMensaje() {
  document.getElementById("modalMensaje").style.display = "none";
}

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registroForm");

  form.addEventListener("submit", async function(e) {
    e.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const apellido = document.getElementById("apellido").value.trim();
    const celular = document.getElementById("celular").value.trim();
    const direccion = document.getElementById("direccion").value.trim();
    const correo = document.getElementById("correo").value.trim();
    const contrasena = document.getElementById("contrasena").value;

    if (contrasena.length < 8) {
      mostrarModalMensaje("La contraseña debe tener al menos 8 caracteres.", true);
      return;
    }

    const datos = { nombre, apellido, celular, direccion, correo, contrasena };

    try {
      const res = await fetch('/registro', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos)
      });

      let data;
      const contentType = res.headers.get('Content-Type');

      if (contentType && contentType.includes('application/json')) {
        data = await res.json();
      } else {
        const texto = await res.text();
        console.error('Respuesta inesperada del servidor:\n', texto);
        mostrarModalMensaje('Respuesta inesperada del servidor', true);
        return;
      }

      if (res.ok) {
        mostrarModalMensaje(data.mensaje || 'Usuario registrado exitosamente');
        setTimeout(() => window.location.href = "/login", 1500);
      } else {
        mostrarModalMensaje(data.mensaje || 'Error al registrar usuario', true);
      }

    } catch (err) {
      console.error('Error procesando respuesta:', err);
      mostrarModalMensaje('Error al registrar el usuario', true);
    }
  });
});
