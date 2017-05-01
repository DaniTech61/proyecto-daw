$( document ).ready(function() {
	if($(window).width() <= 450){
		$("#mensaje").html("Invenit Madrid");
		$("#mensajeTurismo").html("Turismo");
		$("#mensajeGastro").html("Gastronom&#237;a");
	}
	else{
		$("#mensaje").html("InvenitMadrid");
		$("#mensajeTurismo").html("Descubre las mejores vistas y lugares que te dejar&#225;n con la boca abierta");
		$("#mensajeGastro").html("&#191;Tienes hambre? Aqu&#237; encontrar&#225;s una gran variedad de locales");
	}	 	
	$(window).resize(function() {
		if($(window).width() < 450){
			$("#mensaje").html("Invenit Madrid");
			$("#mensajeTurismo").html("Turismo");
			$("#mensajeGastro").html("Gastronom&#237;a");
		}
		else{
			$("#mensaje").html("InvenitMadrid");
			$("#mensajeTurismo").html("Descubre las mejores vistas y lugares que te dejar&#225;n con la boca abierta");
		$("#mensajeGastro").html("&#191;Tienes hambre? Aqu&#237; encontrar&#225;s una gran variedad de locales");
		}								
	});
});