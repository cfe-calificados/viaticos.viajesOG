function confirmar(descripcion) {
    var confirmado = confirm(descripcion);
    console.log(window.location);
    if (confirmado) {
	var win_loc = window.location.toString();
	if(win_loc.includes("view")){
	    win_loc = win_loc.substring(0,win_loc.length-5);
	}
	window.location = win_loc+"/@@reset_list";
	//window.location += "/@@reset_list";
    }
}
