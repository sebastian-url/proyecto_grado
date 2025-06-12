    window.addEventListener('DOMContentLoaded', async () => {
      const res = await fetch('/api/usuario-logueado');
      if (res.ok) {
        const usuario = await res.json();
        document.getElementById("nombre-usuario").textContent = usuario.nombre;
      } else {
        window.location.href = "/login";
      }
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

    let productoSeleccionado = null;

    function toggleMenu() {
      const sidebar = document.getElementById('sidebar');
      sidebar.classList.toggle('visible');
    }

    async function cargarProductos() {
      try {
        const res = await fetch('/api/productos');
        const productos = await res.json();

        if (!Array.isArray(productos) || productos.length === 0) {
          document.getElementById('productos-container').innerHTML = '<p>No hay productos disponibles.</p>';
          return;
        }

        const contenedor = document.getElementById('productos-container');
        contenedor.innerHTML = '';

        productos.forEach(p => {
          const tarjeta = document.createElement('div');
          tarjeta.className = 'tarjeta';
          tarjeta.innerHTML = `
            <p><img class="imagenProducto" src="../static/img/${p.imagen}"></img></p>
            <h3>${p.nombre_producto}</h3>
            <p>${p.descripcion}</p>
            <p><strong>$${p.precio_producto}</strong></p>
            <button class="btn-comprar" onclick="abrirModal('${p.nombre_producto}','${p.descripcion}','${p.precio_producto}','${p.id}')">Comprar</button>
          `;
          contenedor.appendChild(tarjeta);
        });
      } catch (err) {
        console.error('Error al cargar productos:', err);
      }
    }

  function abrirModal(nombre, descripcion, precio, id) {
    productoSeleccionado = {id};
    // Mostrar la información del producto
    document.getElementById('nombreProducto').textContent = nombre;
    document.getElementById('descripcionProducto').textContent = descripcion;
    document.getElementById('precioProducto').textContent = precio;

    // Establecer cantidad por defecto
    const cantidadInput = document.getElementById('cantidad');
    cantidadInput.value = 1;

    // Calcular y mostrar el total inicial
    const totalInput = document.getElementById('total');
    totalInput.value = (precio * cantidadInput.value);

    // Agregar evento para actualizar el total cuando cambie la cantidad
    cantidadInput.oninput = function () {
      const nuevaCantidad = parseInt(this.value) || 0;
      totalInput.value = (precio * nuevaCantidad);
    };

    // Mostrar el modal
    document.getElementById('modalProducto').style.display = 'flex';
  }


    function cerrarModal() {
      document.getElementById('modalProducto').style.display = 'none';
      productoSeleccionado = null;
    }

  function comprarProducto() {
    const cantidad = parseInt(document.getElementById('cantidad').value);
    const fecha = document.getElementById('fecha').value;
    const total = parseFloat(document.getElementById('total').value);

    // Validaciones
    if (!productoSeleccionado) {
      cerrarModal();
      mostrarModalMensaje('Por favor selecciona un producto', true);
      setTimeout(() => {
        cerrarModalMensaje();
      }, 2000);
      return;
    }

    if (!cantidad || cantidad < 1) {
      cerrarModal();
      mostrarModalMensaje('Por favor ingresa una cantidad válida', true);
      setTimeout(() => {
        cerrarModalMensaje();
      }, 2000);
      return;
    }

    if (!fecha) {
      cerrarModal();
      mostrarModalMensaje('Por favor selecciona una fecha', true);
      setTimeout(() => {
        cerrarModalMensaje();
      }, 2000);
      return;
    }

    // Enviar compra
    fetch('/api/comprar-producto', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        id_producto: productoSeleccionado.id,
        cantidad: cantidad,
        fecha: fecha,
        total:total
      })
    })
    .then(res => res.json())
    .then(data => {
      cerrarModal();
      mostrarModalMensaje(`Compra realizada exitosamente`);
      setTimeout(() => {
        cerrarModalMensaje();
      }, 2000);
    })
    .catch(err => {
      cerrarModal();
      mostrarModalMensaje(`Error al realizar la compra: ${err.message}`, true);
      cerrarModal();
      setTimeout(() => {
        cerrarModalMensaje();
      }, 2000);

    });
  }

    window.addEventListener('DOMContentLoaded', cargarProductos());