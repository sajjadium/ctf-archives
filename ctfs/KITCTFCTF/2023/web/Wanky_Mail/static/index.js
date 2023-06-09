var emails = document.querySelectorAll('tr');
for (var i = 1; i < emails.length; i++) {
    var email = emails[i];
    var id = email.getAttribute('id');
    var overlay = document.getElementById("overlay-" + id)

    email.addEventListener('click', function(event) {
        overlay.style.display = 'flex';
    });
}

document.body.addEventListener("click", function(event) {
    var clickedElement = event.target;
    var overlays = document.getElementsByClassName('overlay');
    for (var i = 0; i < overlays.length; i++) {
        var overlay = overlays[i];
        var email = overlay.children[0];
        if (overlay === clickedElement
            && email !== clickedElement && !email.contains(clickedElement)) {
            overlay.style.display = 'none';
        }
    }
});

setInterval( () => {
    var overlays = document.getElementsByClassName('overlay');
    for (var i = 0; i < overlays.length; i++) {
        if (overlay.style.display !== 'none') return;
    }
    location.reload();
}, 5000)