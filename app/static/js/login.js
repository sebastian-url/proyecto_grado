    function mostrarModalMensaje(mensaje, esError = false) {
      const modalTexto = document.getElementById("textoMensaje");
      modalTexto.textContent = mensaje;
      modalTexto.style.color = esError ? "red" : "green";
      document.getElementById("modalMensaje").style.display = "flex";
    }


    function cerrarModalMensaje() {
      document.getElementById("modalMensaje").style.display = "none";
    }

    // Mostrar mensaje de error si hay ?error=1 en la URL
    const params = new URLSearchParams(window.location.search);
    if (params.get("error") === "1") {
      document.getElementById("mensaje-error").style.display = "block";
    }
  document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const correo = document.getElementById("correo").value;
    const contrasena = document.getElementById("contrasena").value;

    const res = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ correo, contrasena })
    });

    const data = await res.json();

    if(res.ok){
      if (data.rol === 1) {
        window.location.href = "/menu";
      } else if (data.rol === 2) {
        window.location.href = "/catalogo";
      } else {
        alert("Rol desconocido: " + data.rol);
      }
    }else{
      mostrarModalMensaje("Usuario o contraseña incorrectos.",true);
      setTimeout(() => {
        cerrarModalMensaje();
      }, 2000);
    }

  });

  function abrirModal() {
    document.getElementById("modalRecuperar").style.display = "flex";
  }

  function cerrarModal() {
    document.getElementById("modalRecuperar").style.display = "none";
  }

  async function recuperarContraseña() {
    const correo = document.getElementById('correoRecuperar').value;
    cerrarModal();
    const res = await fetch(`/recuperar-contraseña`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ correo: correo})
    });
    if (res.ok) {
      mostrarModalMensaje("Se ha enviado un correo para recuperar tu contraseña.");
      setTimeout(() => {
        cerrarModalMensaje();
        window.location.reload();
      }, 2000);
    } else {
      mostrarModalMensaje("Error al enviar el correo de recuperación.",true);
      setTimeout(() => {
        cerrarModalMensaje();
      }, 2000);
    }
  }