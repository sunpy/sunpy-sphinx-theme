$.getJSON('https://pypi.org/pypi/sunpy/json', function(data) {
	ver= 'Current Version: ' + data.info.version;
	$('.version').html(ver);
});
