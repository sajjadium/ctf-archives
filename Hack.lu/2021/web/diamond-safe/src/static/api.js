function vault_show(id) {
    $.ajax({
        type: "POST",
        url: "/api.php",
        data: {"csrf_token":csrf_token,"action":"show","id":id},
        dataType: "json",
        success:function (data) {
            if (data["error"] === ''){
                $("#id_" + id).text(data["result"]);
            }
            else
                alert('Error: ' + data["error"]);
        }
    });
}
function vault_add() {
    data = [
        $('#name').val(),
        $('#password').val(),
        $('#email').val()
        ];
    $.ajax({
        type: "POST",
        url: "/api.php",
        data: {"csrf_token":csrf_token,"action":"add","data":data},
        dataType: "json",
        success:function (data) {
            if (data["error"] !== '')
                alert('Error: ' + data["error"]);
            else
                location.reload();
        }
    });
}
