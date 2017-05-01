$( document ).ready(function() {
	if($(window).width() < 1200){
		$(".cajasContenido").css("margin-left","-50px");

	}	 	
	$(window).resize(function() {
		if($(window).width() < 1200){
			$(".cajasContenido").css("margin-left","-50px");

		}
		else{
			$(".cajasContenido").css("margin-left","0px");
		}								
	});
});