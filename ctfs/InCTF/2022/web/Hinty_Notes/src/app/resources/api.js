function clear() {
  timeout = setTimeout(output, 4000);
}

function output() {
  document.getElementById("output").innerText="";
}

function requests(endpoint,data) {
  let out={}
  fetch(endpoint, {
  method: 'POST', 
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data),
})
  .then((response) => response.json())
  .then((d) => {
    console.log('Success:', d);
    document.getElementById("output").innerText="Successfull";
    clear()
    if(d["url"]){
      localStorage.setItem("hint", d["url"]);
    }
  })
  .catch((error) => {
    console.error('Error:', error);
  });
  return out
 }

 function hint(){
  if (localStorage.getItem("hint")==null){
    alert("Retrive Note First");
  }
  else{
    window.location.href=localStorage.getItem("hint");;
  }
 }

function addnote() {
    var username = document.getElementById("username").value 
    var password = document.getElementById("password").value 
    var key = document.getElementById("key").value 
    var note = document.getElementById("note").value 
    data={"username":username,"password":password,"note":note,"key":key}
    requests('/generate',data)
}

function retrivenote() {
  var username = document.getElementById("username1").value 
  var password = document.getElementById("password1").value 
  var key = document.getElementById("key1").value 
  data={"username":username,"password":password,"key":key}
  requests('/getnotes',data)
}
function search() {
  var search1 =document.getElementById("search").value
  if(localStorage.getItem("hint")!=null){
    var s = localStorage.getItem("hint")
    url="/search?query="+search1+"&hint="+localStorage.getItem("hint").slice(24,s.length)
    fetch(url)
  .then((response) => response.text())
  .then((data) => document.getElementById("searchout").innerText=data);

  }
  
}