    // Mostrar/Ocultar menú lateral
    document.getElementById('toggleMenu').addEventListener('click', () => {
      document.getElementById('sidebarMenu').classList.toggle('visible');
    });

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