function confirmar(descripcion) {
    var confirmado = confirm(descripcion);
    console.log(window.location);
    if (confirmado) {
	window.location += "/@@reset_list";
    }
}
