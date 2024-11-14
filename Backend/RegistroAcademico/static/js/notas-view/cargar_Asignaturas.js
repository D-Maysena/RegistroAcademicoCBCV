const asignaturaSelect = document.getElementById("id_Asignatura");

// Crear y agregar la opción por defecto una vez
if (!document.querySelector("#id_Asignatura option[value='']")) {
  const optiondefault = document.createElement("option");
  optiondefault.value = ""; // Opción vacía, sin valor
  optiondefault.textContent = "Seleccione una asignatura"; // Texto visible
  optiondefault.selected = true;
  asignaturaSelect.appendChild(optiondefault);
}

document.getElementById("id_estudiante").addEventListener("change", async function () {
  const estudianteid = this.value;

  // Asegúrate de que el estudianteid no esté vacío
  if (estudianteid) {
    try {
      const response = await fetch(`/cargarAsignaturas/?estudiante=${estudianteid}`);
      const data = await response.json();

      // Eliminar solo las opciones dinámicas (sin borrar la opción predeterminada)
      Array.from(asignaturaSelect.options).forEach((option) => {
        if (option.value !== "") {
          option.remove();
        }
      });

      data.forEach((asignaturas) => {
        const option = document.createElement("option");
        option.value = asignaturas.codigoasignatura;
        option.textContent = `${asignaturas.Nombre} - ${asignaturas.codestudiante}`;
        asignaturaSelect.append(option);
      });

      asignaturaSelect.value = "";
      asignaturaSelect.dispatchEvent(new Event("change")); // Disparar el evento 'change' manualmente

      if (data.length === 1) {
        asignaturaSelect.value = data[0].codigoasignatura;
        asignaturaSelect.dispatchEvent(new Event("change")); // Disparar el evento 'change' para cargar las notas
      }

    } catch (error) {
      console.error("Error al cargar las asignaturas:", error);
    }
  }
});

// Definir la función crearInputSiNoHayNota
const crearInputSiNoHayNota = (container, nota, parcialNumber) => {
  container.innerHTML = ""; // Limpiar cualquier contenido previo
  const input = document.createElement("input");
  input.type = "text";
  input.maxLength = "3";
  input.className = "input-nota";
  input.placeholder = "Sin nota";
  if (parcialNumber == "notafinal"){

    input.name = `${parcialNumber}`;
  }
  else{
    input.name = `parcial${parcialNumber}`;
    }
  if (nota === null || nota === undefined || nota === "") {
    container.appendChild(input); // Si no hay nota, agregar el input vacío
  } else {
    input.value = nota; // Si hay una nota, colocarla en el input
    container.appendChild(input);
  }
};

// Definir la función notas para cargar notas en contenedores específicos
const notas = async (asignatura, estudianteid) => {
  const containerp1 = document.querySelector(".parcial1-content");
  const containerp2 = document.querySelector(".parcial2-content");
  const containerp3 = document.querySelector(".parcial3-content");
  const containerp4 = document.querySelector(".parcial4-content");
  const containerFinal = document.querySelector(".notafinal-content");

  try {
    const responseNotas = await fetch(
      `/cargarNotas/?estudiante=${estudianteid}&asignatura=${asignatura}`
    );
    const dataNotas = await responseNotas.json();

    if (dataNotas.length > 0) {
      const notas = dataNotas[0];
      crearInputSiNoHayNota(containerp1, notas.parcial1, 1);
      crearInputSiNoHayNota(containerp2, notas.parcial2, 2);
      crearInputSiNoHayNota(containerp3, notas.parcial3, 3);
      crearInputSiNoHayNota(containerp4, notas.parcial4, 4);
      crearInputSiNoHayNota(containerFinal, notas.notafinal, "notafinal");
    } else {
      console.log("No se encontraron notas para el estudiante y asignatura seleccionados.");
      crearInputSiNoHayNota(containerp1, "", 1);
      crearInputSiNoHayNota(containerp2, "", 2);
      crearInputSiNoHayNota(containerp3, "", 3);
      crearInputSiNoHayNota(containerp4, "", 4);
      crearInputSiNoHayNota(containerFinal, "", 5);
    }
  } catch (error) {
    console.log("Error al cargar las notas:", error);
  }
};

// Agregar evento de cambio al select de asignatura
asignaturaSelect.addEventListener("change", function () {
  const estudianteid = document.getElementById("id_estudiante").value;
  const asignaturaSeleccionada = asignaturaSelect.value;

  if (asignaturaSeleccionada) {
    notas(asignaturaSeleccionada, estudianteid);
  }
});

// Detectar cuando el usuario selecciona de nuevo la misma opción en asignaturaSelect
asignaturaSelect.addEventListener("click", function () {
  const estudianteid = document.getElementById("id_estudiante").value;
  if (asignaturaSelect.value === "") {
    notas(asignaturaSelect.value, estudianteid);
  }
});
