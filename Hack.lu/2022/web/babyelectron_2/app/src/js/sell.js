sellListing = function(e){
    num = /.*(\d).*/.exec(e.path[0].id)[1] ?? null
    houseId = document.getElementById(`REL-${num}-houseId`).innerText
    message = document.getElementById(`REL-${num}-message`).innerText
    price = document.getElementById(`REL-${num}-price`).value
    
    fetch(RELapi + "/sell", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        houseId: houseId,
        token: token,
        message: message,
        price: price
      }),
    }).then(()=>{
      window.location.reload();
    })
}

update = function(num){
    document.getElementById(`REL-${num}-sell`).addEventListener("click", sellListing)
}