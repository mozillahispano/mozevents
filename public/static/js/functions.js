$( document ).ready( function() {
	/* Autosubmit l10n form */
	$( '#lang-selector select' ).change( function() {
		$("#lang-selector").submit();
	});
});
