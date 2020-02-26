function coloring(){
    $("td").each(
	function(){
	    var texto = $(this).text();
	    if(texto.includes("borrador")){
		$(this).attr("style", "color:red;");
	    }
	    else if(texto.includes("revision_aprobador") || texto.includes("bosquejo")){
		$(this).attr("style", "color:#eb6123;");
	    }
	    else if(texto.includes("esperando_agencia") || texto.includes("revision_finanzas") || texto.includes("revision_implant")){
		$(this).attr("style", "color:blue;");
	    }
	    else if(texto.includes("anticipo_pendiente")){
		$(this).attr("style", "color:green;");
	    }
	    else if(texto.includes("transferencia_anticipo")){
		$(this).attr("style", "color:#32a8a0;");
	    }
	});
}

$(document).ready(function(){
    $("#viewlet-below-content").hide();
    coloring();
    
    var tabs = document.getElementById('icetab-container').children;
    var tabcontents = document.getElementById('icetab-content').children;
    $("#icetab-content").css("height",(($(".tab-active tr").length+4)*2)+"em");

    var myFunction = function() {
	var tabchange = this.mynum;
	for(var int=0;int<tabcontents.length;int++){
	    tabcontents[int].className = ' tabcontent';
	    tabs[int].className = ' icetab';
	}
	tabcontents[tabchange].classList.add('tab-active');
	this.classList.add('current-tab');
	$("#icetab-content").css("height",(($(".tab-active tr").length+4)*2.2)+"em");
    }	


    for(var index=0;index<tabs.length;index++){
	tabs[index].mynum=index;
	tabs[index].addEventListener('click', myFunction, false);
    }
})
