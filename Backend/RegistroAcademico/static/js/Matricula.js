document.addEventListener('DOMContentLoaded', async () => {
    let numero_matricula = document.getElementById('numero-matricula');
    // Verificar si estamos en el formulario de agregar (es decir, si no hay un codestudiante)
    const url = window.location.href; // Obtener la URL actual
    // Solo realizar el incremento si estamos agregando un estudiante (sin codestudiante)
    
    console.log(url)
    
    if (!url.includes('agregarEstudianteEditar')) { // Si no está presente 'codestudiante' en la URL, es agregar
        console.log("heu")
            try {
                // Traer la lista de estudiantes para obtener el próximo número de matrícula
                const estudiantes = await fetch('/cargarEstudiantes');
                const estudiantesApi = await estudiantes.json();

                let numero = estudiantesApi.length;
                numero++; // Incrementamos el número de matrícula

                numero_matricula.value = numero; // Asignar el valor de matrícula incrementada

                console.log(estudiantesApi);
            } catch (error) {
                console.log(error);
            }
        }
});
