document.getElementById('id_grupo').addEventListener('change', async function() {
    const grupoId = this.value;
    const estudianteSelect = document.getElementById('id_estudiante');

    // Crear y agregar la opción predeterminada si no existe
    if (!document.querySelector("#id_estudiante option[value='']")) {
        const optionDefault = document.createElement("option");
        optionDefault.value = ""; // Opción vacía, sin valor
        optionDefault.textContent = "Seleccione un estudiante"; // Texto visible
        optionDefault.selected = true;
        estudianteSelect.appendChild(optionDefault);
    }

    // Limpiar las opciones (excepto la predeterminada)
    Array.from(estudianteSelect.options).forEach((option) => {
        if (option.value !== "") {
            option.remove();
        }
    });

    try {
        const response = await fetch(`/cargarEstudiantes/?grupo=${grupoId}`);
        const data = await response.json();

        data.forEach(estudiante => {
            const option = document.createElement('option');
            option.value = estudiante.codestudiante;
            option.textContent = `${estudiante.nombre1} ${estudiante.nombre2} ${estudiante.apellido1} ${estudiante.apellido2}`;
            estudianteSelect.appendChild(option);
        });

        // Reiniciar el select al valor predeterminado
        estudianteSelect.value = "";
    } catch (error) {
        console.error('Error al cargar los estudiantes:', error);
    }
});
