console.log("Custom JS for comprobación loaded");
$(document).ready(function() {
    $("thead > tr > th > span").filter(
	function() {
	    return $(this).text() == "Importe" || $(this).text() == "Por anticipo";
	}
    ).parent().remove();
});
		  
