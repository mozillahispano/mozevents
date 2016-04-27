$( document ).ready( function() {
	/* Autosubmit l10n form */
	$( '#lang-selector select' ).change( function() {
		$("#lang-selector").submit();
	});

	
});

//Modal window for filter of events
var actionModal = function(is_show){
	if(is_show){
		$('#filter').show();
	}else{
		$('#filter').hide();
	} 
}
