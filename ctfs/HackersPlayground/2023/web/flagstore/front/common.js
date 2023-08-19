$(document).ready(function() {
    $(".navbar-burger").click(function() {
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active")
    })
    
    $('#error .delete').click((e) => {
      e.preventDefault()
      $('#error').addClass('is-hidden')
    })


})
window.user = {}
fetch('/api/user/me')
    .then(async r=>{
        if(r.status === 200){
            const user = await r.json()
            window.user = user
            $('#username').text(user.name)
            $('#navbar-loggedin').removeClass('is-hidden')
            $('#navbar-nologin').addClass('is-hidden')
        } else {
            const error = r.json()
        }
    })
    .catch(() => {}) // does nothing

function logout(){
    document.cookie='jwt=; expires=Sat, 20 Jan 1980 12:00:00 UTC'
    location.href='/login.html'
}