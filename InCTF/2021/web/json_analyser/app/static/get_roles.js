function get_roles(){
    const role=document.getElementById("role").value
    fetch('http://127.0.0.1:5555/verify_roles?role='+role).then(response=>
        response.text()
    ).then(data =>{
        document.getElementById("output").innerHTML=data;
    })
}
