document.getElementById('id_grupo').addEventListener('change', async function() {
    const grupoId = this.value;
    const estudianteSelect = document.getElementById('id_estudiante');
    estudianteSelect.innerHTML = ''; // Limpiar el select antes de llenarlo

    try {
        const response = await fetch(`/cargarEstudiantes/?grupo=${grupoId}`);
        const data = await response.json();

        data.forEach(estudiante => {
            const option = document.createElement('option');
            option.value = estudiante.codestudiante;
            option.textContent = `${estudiante.nombre1} ${estudiante.nombre2} ${estudiante.apellido1} ${estudiante.apellido2}`;
            estudianteSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error al cargar los estudiantes:', error);
    }
});
