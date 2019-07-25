function coloring(){
    $("td").each(
	function(){
	    var texto = $(this).text();
	    if(texto.includes("borrador")){
		$(this).attr("style", "color:red;");
	    }
	    else if(texto.includes("pendiente") || texto.includes("bosquejo")){
		$(this).attr("style", "color:#eb6123;");
	    }
	    else if(texto.includes("esperando") || texto.includes("revision")){
		$(this).attr("style", "color:green;");
	    }
	});
}

$(document).ready(function(){
    $("#viewlet-below-content").hide();
    coloring();
    
    var tabs = document.getElementById('icetab-container').children;
    var tabcontents = document.getElementById('icetab-content').children;

    var myFunction = function() {
	var tabchange = this.mynum;
	for(var int=0;int<tabcontents.length;int++){
	    tabcontents[int].className = ' tabcontent';
	    tabs[int].className = ' icetab';
	}
	tabcontents[tabchange].classList.add('tab-active');
	this.classList.add('current-tab');
    }	


    for(var index=0;index<tabs.length;index++){
	tabs[index].mynum=index;
	tabs[index].addEventListener('click', myFunction, false);
    }
})
