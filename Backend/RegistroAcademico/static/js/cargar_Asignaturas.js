document
  .getElementById("id_estudiante")
  .addEventListener("change", async function () {
    const estudianteid = this.value;
    const asignaturaSelect = document.getElementById("id_Asignatura");
    asignaturaSelect.innerHTML = ""; // Limpiar el select de asignaturas antes de llenarlo



    // Asegúrate de que el estudianteid no esté vacío
    if (estudianteid) {
      try {
        const response = await fetch(
          `/cargarAsignaturas/?estudiante=${estudianteid}`
        );
        const data = await response.json();

        // Rellenar el select de asignaturas con los datos obtenidos
        data.forEach((asignaturas) => {
          const option = document.createElement("option");
          option.value = asignaturas.codigoasignatura;
          option.selected = false
          option.textContent = `${asignaturas.Nombre} - ${asignaturas.codestudiante}`;
          asignaturaSelect.appendChild(option);
          
          
        });
        const optionEmpty = document.createElement("option");
        optionEmpty.value = "";  // Opción vacía, sin valor
        optionEmpty.textContent = "Seleccione una asignatura";  // Texto visible
        optionEmpty.selected = true
        asignaturaSelect.appendChild(optionEmpty);
        console.log(data.length)
        if (data.length >= 2) {
          asignaturaSelect.value = data[0].codigoasignatura; // Seleccionar la única opción
          // Disparar el evento 'change' para cargar las notas
          asignaturaSelect.dispatchEvent(new Event("change"));
        }

        // Definir la función antes de usarla en cualquier parte
        const crearInputSiNoHayNota = (container, nota, parcialNumber) => {
          container.innerHTML = ""; // Limpiar cualquier contenido previo
          const input = document.createElement("input");
          input.type = "text";
          input.maxLength = "3";
          input.className = "input-nota";
          input.placeholder = "Sin nota";
          input.name = `parcial${parcialNumber}`;

          if (nota === null || nota === undefined || nota === "") {
            container.appendChild(input); // Si no hay nota, agregar el input vacío
          } else {
            input.value = nota; // Si hay una nota, colocarla en el input
            container.appendChild(input);
          }
        };

        // Asegúrate de que el select de asignaturas tenga un evento de cambio
        asignaturaSelect.addEventListener("change", async function () {
          const asignaturaSeleccionada = asignaturaSelect.value;
          console.log(asignaturaSeleccionada)
          // Elementos donde se mostrarán las notas
          const containerp1 = document.querySelector(".parcial1-content");
          const containerp2 = document.querySelector(".parcial2-content");
          const containerp3 = document.querySelector(".parcial3-content");
          const containerp4 = document.querySelector(".parcial4-content");
          const containerFinal = document.querySelector(".notafinal-content");

          try {
            const responseNotas = await fetch(
              `/cargarNotas/?estudiante=${estudianteid}&asignatura=${asignaturaSeleccionada}`
            );
            const dataNotas = await responseNotas.json();

            // Verificar si dataNotas contiene datos antes de acceder a ellos
            if (dataNotas.length > 0) {
              const notas = dataNotas[0];

              // Usar la función para cada contenedor de notas
              crearInputSiNoHayNota(containerp1, notas.parcial1, 1);
              crearInputSiNoHayNota(containerp2, notas.parcial2, 2);
              crearInputSiNoHayNota(containerp3, notas.parcial3, 3);
              crearInputSiNoHayNota(containerp4, notas.parcial4, 4);
              crearInputSiNoHayNota(containerFinal, notas.notafinal);
            } else {
              console.log("No se encontraron notas para el estudiante y asignatura seleccionados.");
              // Crear inputs vacíos si no hay datos de notas
              crearInputSiNoHayNota(containerp1, "", 1);
              crearInputSiNoHayNota(containerp2, "", 2);
              crearInputSiNoHayNota(containerp3, "", 3);
              crearInputSiNoHayNota(containerp4, "", 4);
              crearInputSiNoHayNota(containerFinal, "", 5);
            }
          } catch (error) {
            console.log("Error al cargar las notas:", error);
          }
        });
      } catch (error) {
        console.error("Error al cargar las asignaturas:", error);
      }
    }
  });
