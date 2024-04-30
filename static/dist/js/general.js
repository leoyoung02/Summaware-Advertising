$(document).ready(function() {
	$('#settings-sidebar').click(function() {
		$('body').toggleClass('settings-sidebar-collapse');
	});
	$(document).on('click', '#search_button', function() {
		$('body').toggleClass('search');
	});
});

function showHideStepModal(select_show, select_hide)
{
	document.getElementById(select_show).style.display='block';
	document.getElementById(select_hide).style.display = 'none';
}