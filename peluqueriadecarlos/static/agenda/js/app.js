document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('citaForm');

    // Función para agregar una nueva fila a la tabla
    function agregarFilaCita(nombre, fecha, hora, estado, id) {
        const citasContainer = document.getElementById('citasContainer');
        const fila = document.createElement('tr');
        const estadoClase = estado === "en-proceso" ? "estado-proceso" : "estado-pendiente";
        fila.classList.add(estadoClase); // Aplica el color a toda la fila
        fila.innerHTML = `
            <td>${id}</td>
            <td>${nombre}</td>
            <td>${fecha}</td>
            <td>${hora}</td>
            <td>${estado}</td>
        `;
        citasContainer.appendChild(fila);
    }

    // Evento del formulario
    form.addEventListener('submit', function (e) {
        e.preventDefault();

        // Obtener los valores del formulario
        const nombre = document.getElementById('nombre').value;
        const telefono = document.getElementById('telefono').value;
        const fecha = document.getElementById('fecha').value;
        const hora = document.getElementById('hora').value;

        if (nombre && telefono && fecha && hora) {
            // Enviar los datos al servidor
            fetch('/agregar_cita/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    nombre: nombre,
                    telefono: telefono,
                    fecha: fecha,
                    hora: hora,
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Si se guardó correctamente, actualizar la tabla
                    agregarFilaCita(data.nombre, data.fecha, data.hora, data.estado, data.id);
                    form.reset();  // Limpiar los campos del formulario
                } else {
                    console.error('Error al guardar la cita');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });

    // Renderizar las citas que vienen desde Django (en modo inicial)
    const citas = JSON.parse('{{ citas_json|safe }}'); // Asegúrate de pasar las citas como JSON desde Django
    citas.forEach((cita, index) => {
        agregarFilaCita(cita.nombre, cita.fecha, cita.hora, cita.estado, index + 1);
    });
});
