$( function() {
    /*
	try {
		//var pkBaseURL = (("https:" == document.location.protocol) ? "https://monitor.argonemyth.com/" : "http://monitor.argonemyth.com/");
		var pkBaseURL = "http://monitor.argonemyth.com/";
		var piwikTracker = Piwik.getTracker(pkBaseURL + "piwik.php", 2);
		piwikTracker.trackPageView();
		piwikTracker.enableLinkTracking();
	} catch( err ) {}
    */
	
	var $scrollerWindow = $("#main");
	var $speed = 800;

	$('.clickscroll').live('click', function() {
			$('#quoteform').validationEngine('hide');
			//$scrollerWindow.scrollTo( $(this).attr("href"), $speed, {axis:'x',offset:{left: -60, top:0 }} );
			$scrollerWindow.scrollTo( $(this).attr("href"), $speed, {axis:'x',offset:{left: -5, top:0 }} );
			return false;
	});

	$("[title]").tooltip({position: "bottom right", offset: [-20, -20]});
	$(".thumbnail").tooltip({position: "bottom right", offset: [-40, -20], tipClass: "fullview",});
	
	// for the popup forms in the page.
	$('a.popup').fancybox({
		'transitionIn'	:	'elastic',
		'transitionOut'	:	'elastic',
		'speedIn'		:	600, 
		'speedOut'		:	200, 
		'overlayShow'	:	false,
		'onComplete'	:	form_validation,
		'onCleanup'		:	hide_errors 
	});
	
	// valicate quote form & bind fancybox feedback to quote form
	$("#quoteform").validationEngine('attach', {
		onValidationComplete: function(form, validation_result) {
			if ( validation_result ) {
				// if the form is good
				$.ajax({
					type	:"POST",
					cache	:false,
					url		:"/getquote/",
					data	:form.serializeArray(),
					success: function(data) {
						$.fancybox(data, {'overlayShow':false, });
					}
				});
				return false;
			} 
		  }
	});

	/*
	$("form#search").live('submit', search_site);
	$("a.link_anchor").click( function(e) {
		// block the normal href link
		e.preventDefault();
		e.stopPropagation();
		//$(this).addClass('ajaxized');
		// get the normal href link
		var link = $(this).attr('href');
		$('#post').load(
			link
		)
	}); 
	*/
});

function form_validation(){
	// Form validation and response
	$("#freeform").bind("submit", function() {
		$.ajax({
			type	:"POST",
			cache	:false,
			url		:"/get-freesite/",
			data	:$(this).serializeArray(),
			success: function(data) {
				$.fancybox(data, {'overlayShow':false, });
			}
		});

		return false;
	}).validationEngine('attach');
}

function hide_errors() {
	$('#freeform').validationEngine('hide');
}
