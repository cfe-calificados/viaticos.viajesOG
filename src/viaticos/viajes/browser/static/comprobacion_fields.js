console.log("Custom JS for comprobación loaded");
$(document).ready(function() {
    console.log("removing ommited");
    if ($("input[name='form.widgets.grupo_comprobacion.0.widgets.importe']").attr("type") == "hidden") {
	console.log("importe");
	$("thead > tr > th > span").filter(
	    function() {
		return $(this).text() == "Importe";
	    }
	).parent().remove();
    }
    if (!$("input[name='form.widgets.grupo_comprobacion.0.widgets.anticipo-empty-marker']").length) {
	console.log("tipo");
	$("thead > tr > th > span").filter(
	    function() {
		return $(this).text() == "Tipo";
	    }
	).parent().remove();
    }
    
});
