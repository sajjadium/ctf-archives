<?php

session_start();

if (!@$_SESSION["isLoggedIn"]) {
	header("Location: /index.php");
	die();
}

if ($_SESSION["username"] !== "admin") {
	http_response_code(403);
	die(file_get_contents("403.html"));
}

?>



<!DOCTYPE html>
<html lang="en">

<head>
	<!-- Required meta tags -->
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<title>App - Update Role</title>

	<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css" integrity="sha384-UHRtZLI+pbxtHCWp1t77Bi1L4ZtiqrqD80Kn4Z8NTSRyMA2Fd33n5dQ8lWUE00s/" crossorigin="anonymous">

	<link rel="stylesheet" href="assets/css/bootstrap4-neon-glow.min.css">
	<link rel="stylesheet" href="assets/css/main.css">
	<link rel="stylesheet" href="assets/css/particles.css">

	<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
	<link rel='stylesheet' href='https://cdn.jsdelivr.net/font-hack/2.020/css/hack.min.css'>

</head>

<body>

	<div id="particles-js"></div>

	<div class="navbar-dark text-white">
		<div class="container">
			<nav class="navbar px-0 navbar-expand-lg navbar-dark">
				<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
					<span class="navbar-toggler-icon"></span>
				</button>
				<div class="collapse navbar-collapse" id="navbarNavAltMarkup">
					<div class="navbar-nav">
						<a href="index.php" class="pl-md-0 p-3 text-light">Home</a>
						<a href="admin.php" class="p-3 text-decoration-none text-light">Admin pannel</a>
						<a href="/api/logout.php" class="p-3 text-decoration-none text-light active">Logout</a>
					</div>
				</div>
			</nav>

		</div>
	</div>

	<div class="container py-5 mb-5">
		<h1 class="mb-5" style="text-align: center">Here you go<span class="vim-caret">&nbsp;&nbsp;</span></h1>
		<div class="row py-4">
			<div class="col-md-8 order-md-2">
				<h4 class="mb-3">Upload Your Favorite File</h4>
				<form class="needs-validation" novalidate action="/upload.php" method="POST" enctype="multipart/form-data">
					<div class="mb-3">
						<!-- File input -->
						<label for="file">Select a file:</label>
						<input type="file" class="form-control-file" id="file" name="file" required>
					</div>

					<!-- Removed the username and confirm fields -->

					<hr class="mb-4">
					<hr class="mb-4">
					<button class="btn btn-outline-success btn-shadow btn-lg btn-block" type="submit">Share</button>
				</form>
				<br>
				<div class="row justify-content-center" style="text-align: center">
					<p id="message"> </p>
				</div>
			</div>
			<div class="col-md-2 order-md-1"></div>
			<div class="col-md-2 order-md-3"></div>
		</div>
	</div>




	<!-- Optional JavaScript -->
	<!-- jQuery first, then Popper.js, then Bootstrap JS -->

	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>
	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>

	<script>
		$("input:checkbox").on('click', function() {
			// in the handler, 'this' refers to the box clicked on
			var $box = $(this);
			if ($box.is(":checked")) {
				// the name of the box is retrieved using the .attr() method
				// as it is assumed and expected to be immutable
				var group = "input:checkbox[name='" + $box.attr("name") + "']";
				// the checked state of the group/box on the other hand will change
				// and the current value is retrieved using .prop() method
				$(group).prop("checked", false);
				$box.prop("checked", true);
			} else {
				$box.prop("checked", false);
			}
		});
	</script>

	<script src="assets/js/particles.js"></script>
	<script src="assets/js/app.js"></script>
	<script type="text/javascript">
		function handleSubmit(event) {
			event.preventDefault();

			// Get the selected file from the input field
			const fileInput = document.querySelector('input[type="file"]');
			const file = fileInput.files[0];
			if (file) {
				const json_data = {
					filename: file.name,
					base64_content: "",
				};

				const reader = new FileReader();
				reader.onload = function(event) {
					const parts = event.target.result.split(',');
					if (parts.length === 2) {
						json_data.base64_content = parts[1];

						// Send the JSON data to the server
						const JSONdata = JSON.stringify(json_data);

						fetch("/api/file.php", {
								method: "POST",
								headers: {
									'Content-Type': 'application/json',
								},
								body: JSONdata,
							})
							.then(response => response.text())
							.then(r => {
								document.getElementById("message").innerText = r;
							})
							.catch(error => console.log(error))
					} else {
						console.log("Error: Invalid base64 data.");
					}
				};
				reader.readAsDataURL(file);
			}
		}

		const form = document.querySelector('form');
		form.addEventListener('submit', handleSubmit);
	</script>

</body>

</html>