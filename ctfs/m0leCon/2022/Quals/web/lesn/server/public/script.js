
function redirect_error_image() {
    document.location = document.location.toString().replace('post', 'edit') + '?err=Invalid+image,+please+change+url'
}

function redirect_home(err) {
    document.location = '/?err=' + err
}

function redirect_to(url) {
    document.location = url
}

