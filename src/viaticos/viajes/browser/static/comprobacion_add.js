function handleDGFDelete() {
    console.log("removing row and updating grid");
    $(".insert-row").attr("style", "visibility:hidden;");
    $(".datagridfield-last-filled-row .insert-row").attr("style", "visibility:visible;");    
}

$(document).ready(function(){
    //$(".datagridwidget-body").removeClass('datagridwidget-body-auto-append');
    $("#formfield-form-widgets-grupo_comprobacion").ready(function() {
	console.log("removing undesired events");
	$("#formfield-form-widgets-grupo_comprobacion").find("*").each(function(){
	    $(this).off("blur");
	    //$(this).removeClass('auto-append');
	});
    });

    $(".pattern-pickadate-date").ready(function(){
	if($(window).width() < 1400) {
	    console.log("changing-size-on-start");
	    console.log($(".pattern-pickadate-date").length);
	    $(".pattern-pickadate-date").each(function(){$(this).attr("style","width:170px !important;")});
	    $(".container").attr("style", "width:100%; margin-left:0em;");
	}
    });

    /*
      $(".datagridwidget-manipulator.delete-row #btn-deleterow").ready(function(){
      var onclic = $(".datagridwidget-manipulator.delete-row #btn-deleterow").attr("onClick");
      console.log(onclic);
      var clic_arr = onclic.split(";");
      var clic_slice = clic_arr.slice(0,clic_arr.length-1);
      $(".datagridwidget-manipulator.delete-row #btn-deleterow").attr("onClick", clic_slice.join(";")+"; handleDGFDelete(); return false");
      });*/
});


$( window ).on('resize', function() {
    if($(window).width() > 1400) {
	console.log("deleting-size");
	$(".pattern-pickadate-date").each(function(){$(this).removeAttr("style")});
	$(".container").removeAttr("style");
    }
    else {
	console.log("changing-size");
	$(".pattern-pickadate-date").each(function(){$(this).attr("style","width:170px !important;")});
	$(".container").attr("style", "width:100%; margin-left:0em;");
    }
});


var handleDGFInsert = function(event, dgf, row) {
    console.log("setting add button");
    console.log("changing-size-on-start");
    console.log($(".pattern-pickadate-date").length);
    $(".pattern-pickadate-date").each(function(){$(this).attr("style","width:170px !important;")});
    //$(".insert-row").attr("style", "visibility:hidden;");
    //$(".datagridfield-last-filled-row .insert-row").attr("style", "visibility:visible;");
    $(".datagridfield-last-filled-row").last().remove();
};

$(document).on('afteraddrowauto', '.datagridwidget-table-view', handleDGFInsert);
//$(document).on('afterdatagridfieldinit', handleDGFInsert);

