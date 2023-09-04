const urlParams = new URLSearchParams(window.location.search);
var auto_download = urlParams.get('auto_download') ? 1 : 0
if(auto_download) {
	setTimeout(download, 2000);
}