let showLoginDialog = false;

function updateLoginDialog() {
	if (showLoginDialog) {
		$("header .login .dropdown").addClass("visible");
	} else {
		$("header .login .dropdown").removeClass("visible");
	}
}

$(document).ready(() => {
	$("body").click(() => {
		showLoginDialog = false;
		updateLoginDialog();
	});

	$("header .login").click((e) => {
		showLoginDialog = !showLoginDialog;		updateLoginDialog();
		e.stopPropagation();
	});

	$("header .login .dropdown").click((e) => e.stopPropagation());

	$("em").lettering();
	$("em").each(function() {
		let childCount = $(this).children().length;
		$(this).children().each(function(i) {
			let angle = (i - ((childCount - 1) / 2)) * .125;

			$(this).css({
				"transform": `
					translate(${10 * Math.sin(angle)}px, ${-4 * Math.cos(5 * angle) + 2}px)
					rotate(${angle}rad)
					matrix(
						${Math.random() * 0.15 + 1 + (i === 0 ? 0.05 : 0)},
						${Math.random() * 0.1},
						${Math.random() * 0.1},
						${Math.random() * 0.15 + 1 + (i === 0 ? 0.05 : 0)},
						${Math.random()},
						${Math.random()}
					)
				`,
				"z-index": i === childCount - 1 ? 102 : Math.floor(2 + 100 * Math.random())
			});
		});
	});

	$("h1 .edit").click(() => {
		let url = new URL(window.location.href);
		url.pathname = "/edit.php";
		window.location = url.toString();
	});

	$("button.report").click(() => {
		grecaptcha.ready(async () => {
			console.log("here");
			let token = await grecaptcha.execute("6LejJMscAAAAAH38ZmF1iIpcKD94XjjGqJzidaYu", { action: "report" });
			console.log("token", token);
			$("#report-form [name=token]").val(token);
			$("#report-form").submit();
		});
	})
});
