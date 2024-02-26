const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.onclick = function() {
	  container.classList.add("right-panel-active");
}

signInButton.onclick = function() {
	container.classList.remove("right-panel-active");
};

document.getElementById('log').onclick = function() {
	document.getElementById('login').submit();
}

document.getElementById('reg').onclick = function() {
	document.getElementById('register').submit();
}
