    function mostrarModalMensaje(mensaje, esError = false) {
      const modalTexto = document.getElementById("textoMensaje");
      modalTexto.textContent = mensaje;
      modalTexto.style.color = esError ? "red" : "green";
      document.getElementById("modalMensaje").style.display = "flex";
    }

    function cerrarModalMensaje() {
      document.getElementById("modalMensaje").style.display = "none";
    }

    document.getElementById("registroForm").addEventListener("submit", async function(e) {
        e.preventDefault();

        const nombre = document.getElementById("nombre").value;
        const apellido = document.getElementById("apellido").value;
        const celular = document.getElementById("celular").value;
        const correo = document.getElementById("correo").value;
        const contrasena = document.getElementById("contrasena").value;

        const res = await fetch("/registro", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre, apellido, celular, correo, contrasena })
        });

        const data = await res.json();

        if (res.ok) {
            mostrarModalMensaje("Registro exitoso. Redirigiendo al login...", false);
            setTimeout(() => {
                window.location.href = "/login"; // Redirige al login si el registro fue exitoso
            }, 2000);
        } else {
            mostrarModalMensaje(data.error || "Error al registrar. Inténtalo de nuevo.", true);
            setTimeout(() => {
                cerrarModalMensaje(); // Cierra el modal después de mostrar el mensaje
            }, 2000);
        }
    });