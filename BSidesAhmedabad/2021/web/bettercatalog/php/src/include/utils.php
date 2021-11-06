<?php

$nonce = base64_encode(random_bytes(24));
header("Content-Security-Policy: default-src 'nonce-$nonce'; img-src *; font-src 'self' fonts.gstatic.com; frame-src https://www.google.com/recaptcha/");

function die_404() {
	?>
	<h1>404 you nerd</h1>
	<?php
	make_footer();
	exit();
}

function send_to_referrer() {
	if (!isset($_SERVER["HTTP_REFERER"]) || $_SERVER["HTTP_REFERER"] == $_SERVER["REQUEST_URI"]) {
		header("Location: /");
	} else {
		header("Location: " . $_SERVER["HTTP_REFERER"]);
	}
	exit();
}
