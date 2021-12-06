const $seleccionArchivos = document.querySelector("#file"),
  $imagenPrevisualizacion = document.querySelector("#img-preview");

$seleccionArchivos.addEventListener("change", () => {

  const archivos = $seleccionArchivos.files;

  if (!archivos || !archivos.length) {
    $imagenPrevisualizacion.src = "";
    return;
  }

  const primerArchivo = archivos[0];

  const objectURL = URL.createObjectURL(primerArchivo);

  $imagenPrevisualizacion.src = objectURL;
});