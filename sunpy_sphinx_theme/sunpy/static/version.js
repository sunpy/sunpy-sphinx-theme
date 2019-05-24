$.getJSON('https://pypi.org/pypi/sunpy/json', function(data) {
	ver=data.info.version;
	$('.version').html(ver);
});
