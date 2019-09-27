console.log("tptm");

$(document).ready(function() {
    if ($("input#form-widgets-req-0").is(":not(:checked)")){
	$("#form-widgets-notas_avion").hide();
	$("label[for='form-widgets-notas_avion']").hide();
    }
    if ($("input#form-widgets-req-1").is(":not(:checked)")){
	$("#form-widgets-notas_hospedaje").hide();
	$("label[for='form-widgets-notas_hospedaje']").hide();
    }

    if ($("input#form-widgets-req-3").is(":not(:checked)")){
	$("#form-widgets-notas_transporte").hide();
	$("label[for='form-widgets-notas_transporte']").hide();
    }

    if ($("input#form-widgets-req-4").is(":not(:checked)")){
	$("#form-widgets-notas_otro").hide();
	$("label[for='form-widgets-notas_otro']").hide();
    }
    
    $("input#form-widgets-req-0").on("change",function() {
	$("#form-widgets-notas_avion").toggle();
	$("label[for='form-widgets-notas_avion']").toggle();
	if ($("input#form-widgets-req-0").is(":checked")){
	    $("#form-widgets-notas_avion").addClass("required");
	} else {
	    $("#form-widgets-notas_avion").removeClass("required");
	}
    });
    $("input#form-widgets-req-1").on("change",function() {
	$("#form-widgets-notas_hospedaje").toggle();
	$("label[for='form-widgets-notas_hospedaje']").toggle();
    });

    //$("input#form-widgets-req-2").on("change",function() {});

    $("input#form-widgets-req-3").on("change",function() {
	$("#form-widgets-notas_transporte").toggle();
	$("label[for='form-widgets-notas_transporte']").toggle();
    });
    $("input#form-widgets-req-4").on("change",function() {
	$("#form-widgets-notas_otro").toggle();
	$("label[for='form-widgets-notas_otro']").toggle();
    });
});





//alert("alv")
var currentCities=[];
var BATTUTA_KEY="7e874777f3421691c58c62dd6bdfb483";
// Populate country select box from battuta API
url="https://geo-battuta.net/api/country/all/?key="+BATTUTA_KEY+"&callback=?";

function prueba_de_existencia() {
    alert('loasnakl');
};



var paises = null;
var loaded_states = false;
var intervalo = null;
var countryCode="";
var pais_selected = null;
var estado_selected = null;

function load_states(){
    $("input#form-widgets-pais").on("change",function() {
		
	if (pais_selected == $("#form-widgets-pais").val()) {return;}
	else {
	    console.log("it's happening!!!");
	    pais_selected = $("#form-widgets-pais").val();
	}
	
	//alert(paises[$("#form-widgets-pais").val()].code)
	countryCode="";
	$.each(paises, function(key, country) {
	    if (country.name == $("#form-widgets-pais").val()) {
		countryCode = country.code;
	    }
	});
	
	
	// Populate country select box from battuta API
	url="https://geo-battuta.net/api/region/"
	    +countryCode
	    +"/all/?key="+BATTUTA_KEY+"&callback=?";

	$.getJSON(url,function(regions) {
  	    $("#form-widgets-estado option").remove();
	    $("body").append('<datalist id="form-widgets-estado-list"></datalist>')
	    //loop through regions..				   
	    $.each(regions,function(key,region) {					      
		$("<option></option>")
		    .attr("value",region.region)
		    .append(region.region)
		    .appendTo($("#form-widgets-estado-list"));
	    });
	    $("input#form-widgets-estado").attr("list", "form-widgets-estado-list")
	    // trigger "change" to fire the #state section update process
	    //$("#region").material_select('update');
	    //$("#region").trigger("change");
	    
	}); 
	
    })}

function load_cities() {
    $("#form-widgets-estado").on("change",function() {
  	if (estado_selected == $("#form-widgets-estado").val()) {return;}
	else {
	    console.log("citieees!!!");
	    estado_selected = $("#form-widgets-estado").val();
	}
  	// Populate country select box from battuta API
  	//countryCode=$("#form-widgets-pais").val();
	region=$("#form-widgets-estado").val();
	url="http://geo-battuta.net/api/city/"
	    +countryCode
	    +"/search/?region="
	    +region
	    +"&key="
	    +BATTUTA_KEY
	    +"&callback=?";
  	console.log("getting:"+url);
  	$.getJSON(url,function(cities) {
  	    currentCities=cities;
            var i=0;
            $("#form-widgets-ciudad option").remove();
	    $("body").append('<datalist id="form-widgets-ciudad-list"></datalist>')
	    //loop through regions..
	    $.each(cities,function(key,city) {
		$("<option></option>")
		    .attr("value",city.city)
		    .append(city.city)
		    .appendTo($("#form-widgets-ciudad-list"));
	    });
	    $("input#form-widgets-ciudad").attr("list", "form-widgets-ciudad-list")
	    // trigger "change" to fire the #state section update process
	    //$("#city").material_select('update');
	    //$("#city").trigger("change");
	    
	}); 
	
    })}

$.getJSON(url,function(countries) {
    console.log(countries);
    paises = countries;
    //$('#country').material_select();
    //loop through countries..
    $("body").append('<datalist id="form-widgets-pais-list"></datalist>')
    $.each(countries,function(key,country) {
	$("<option></option>")
	    .attr("value",country.name)			     
	    .append(country.name+" ("+country.code+") ")
	    .appendTo($("#form-widgets-pais-list"));//#country
	
    });
    $("input#form-widgets-pais").attr("list", "form-widgets-pais-list")
    // trigger "change" to fire the #state section update process
    //$("#country").material_select('update');
    //$("#country").trigger("change");
    

});

//$("#form-widgets-pais").on("change", alert("alv"));
intervalo = self.setInterval(load_states,3000);
intervalo = self.setInterval(load_cities,3000);		  

/*
$("#form-widgets-ciudad").on("change",function()
  	      {
		  currentIndex=$("#form-widgets-ciudad").val();
		  currentCity=currentCities[currentIndex];
		  city=currentCity.city;
		  region=currentCity.region;
		  country=currentCity.country;
		  lat=currentCity.latitude;
		  lng=currentCity.longitude;
		  $("#location").html('<i class="fa fa-map-marker"></i> <strong> '+city+"/"+region+"</strong>("+lat+","+lng+")");
	      });
*/
