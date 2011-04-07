$( document ).ready( function() {
	/* Autosubmit l10n form */
        
	$( '#langSelector select' ).change( function() {
		$("#langSelector").submit();
	});
});