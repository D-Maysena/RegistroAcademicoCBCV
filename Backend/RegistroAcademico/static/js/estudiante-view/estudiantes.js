async function getEstudiantes() {
    const urlInfoEstudiante = document.getElementById('urlInfoEstudiante').value;
    const urlEditarEstud = document.getElementById('agregarEstudianteEditar').value;
    const urlEstudiantesEliminar = document.getElementById('urlEstudiantesEliminar').value;
    const csrfToken = document.getElementById('csrf_token').value;  // Obtén el token CSRF

    try {
        const response = await fetch('/estudiante'); // Espera la respuesta
        const data = await response.json(); // Espera a que se convierta en JSON
        console.log(data); // Ahora puedes acceder a los datos
        const tbody = document.getElementById('container-estudiantes');

        // Limpiar el contenido previo del tbody
        tbody.innerHTML = '';

        // Iterar sobre cada estudiante y crear una fila separada
        data.forEach(info => {
            const tr = document.createElement('tr'); // Crear una nueva fila para cada estudiante

            // Crear celdas para cada propiedad del estudiante
            Object.values(info).forEach(value => {
                const td = document.createElement('td');
                td.textContent = value;
                tr.appendChild(td); // Agregar cada celda a la fila
            });

            const estudianteId = info.codestudiante; // Asegúrate de que esta es la clave correcta
            // Crear celdas de acciones
            const accionesTd = document.createElement('td');
            const finalUrl = urlInfoEstudiante.replace('yepa', estudianteId);
            const finalUrlEditar = urlEditarEstud.replace('yepa', estudianteId);
            const finalUrlEliminar = urlEstudiantesEliminar.replace('yepa', estudianteId);
            accionesTd.innerHTML = `
                <a class="btn btn-info btn-sm" href="${finalUrl}">Ver</a>
                <a class="btn btn-warning btn-sm" href="${finalUrlEditar}">Editar</a>
                <button class="btn btn-danger btn-sm" data-estudiante-id="${estudianteId}" id="eliminar-btn-${estudianteId}">Eliminar</button>
            `;
            tr.appendChild(accionesTd);
            tbody.appendChild(tr);

            const eliminarBtn = document.getElementById(`eliminar-btn-${estudianteId}`);
            eliminarBtn.addEventListener('click', function () {
                Swal.fire({
                    title: "¿Estás seguro?",
                    text: "¡No podrás revertir esta acción!",
                    icon: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#3085d6",
                    cancelButtonColor: "#d33",
                    confirmButtonText: "¡Sí, eliminarlo!"
                }).then((result) => {
                    if (result.isConfirmed) {
                        // Realizar la eliminación con un POST
                        fetch(finalUrlEliminar, {
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrfToken  // Enviar el token CSRF en el encabezado
                            }
                        }).then(response => {
                            if (response.ok) {
                                Swal.fire({
                                    title: "¡Eliminado!",
                                    text: "El estudiante ha sido eliminado.",
                                    icon: "success"
                                }).then(() => {
                                    // Actualizar la lista de estudiantes
                                    getEstudiantes();
                                });
                            } else {
                                Swal.fire({
                                    title: "Error",
                                    text: "Hubo un problema al eliminar al estudiante.",
                                    icon: "error"
                                });
                            }
                        });
                    }
                });
            });
        });
    } catch (error) {
        console.error('Error:', error); 
    }
}

getEstudiantes();
