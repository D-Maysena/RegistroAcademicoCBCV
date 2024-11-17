async function getDocentes() {
    const urlInfoDocente = document.getElementById('urlInfoDocente').value;
    const urlEditarDocente = document.getElementById('agregarDocenteEditar').value;
    const urlDocentesEliminar = document.getElementById('urlDocentesEliminar').value;
    const csrfToken = document.getElementById('csrf_token').value; 

    try {
        const response = await fetch('/docente'); // Solicitar los datos de los docentes
        const data = await response.json(); // Convertir la respuesta en JSON
        console.log(data); // Puedes ver los datos de los docentes en la consola
        const tbody = document.getElementById('container-docentes');

        // Limpiar el contenido previo del tbody
        tbody.innerHTML = '';

        // Iterar sobre cada docente y crear una fila separada
        data.forEach(info => {
            const tr = document.createElement('tr'); // Crear una nueva fila para cada docente

            // Crear celdas para cada propiedad del docente
            Object.values(info).forEach(value => {
                console.log(value)
                const td = document.createElement('td');
                td.textContent = value;
                tr.appendChild(td); // Agregar cada celda a la fila
            });

            const docenteId = info.ceduladocente; // Asegúrate de que esta es la clave correcta
            const accionesTd = document.createElement('td');
            const finalUrl = urlInfoDocente.replace('yepa', docenteId);
            const finalUrlEditar = urlEditarDocente.replace('yepa', docenteId);
            const finalUrlEliminar = urlDocentesEliminar.replace('yepa', docenteId);
            accionesTd.innerHTML = `
                <a class="btn btn-info btn-sm" href="${finalUrl}">Ver</a>
                <a class="btn btn-warning btn-sm" href="${finalUrlEditar}">Editar</a>
                <button class="btn btn-danger btn-sm" data-docente-id="${docenteId}" id="eliminar-btn-${docenteId}">Eliminar</button>
            `;
            tr.appendChild(accionesTd);
            tbody.appendChild(tr);

            const eliminarBtn = document.getElementById(`eliminar-btn-${docenteId}`);
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
                                    text: "El docente ha sido eliminado.",
                                    icon: "success"
                                }).then(() => {
                                    // Actualizar la lista de docentes
                                    getDocentes();
                                });
                            } else {
                                Swal.fire({
                                    title: "Error",
                                    text: "Hubo un problema al eliminar al docente.",
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

getDocentes();
