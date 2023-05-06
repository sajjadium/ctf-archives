const HTML = document.getElementById("REL-content")
const RELattr = ["image", "name", "sqm", "message", "price", "houseId"]
let RELapi = localStorage.getItem("api");
let token = localStorage.getItem("token");

const replace = (selector , value) => {
    const element = document.getElementById(selector);
    if(element){
        if (/image/.test(selector)) {
            element.src = "../" + value;
        }else if (/sqm/.test(selector)){
            element.innerHTML = value + " sqm";
        }
        else if (/price/.test(selector)){
            element.innerHTML = value + "$";
        }
        else{
            element.innerHTML = value
        }
    }
  };

buyListing = function(e){
    num = /.*(\d).*/.exec(e.path[0].id)[1] ?? null
    houseId = document.getElementById(`REL-${num}-houseId`).innerText
    
    fetch(RELapi + "/buy", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        houseId: houseId,
        token: token
      }),
    })
}


fetch(RELapi + `/listings?token=${encodeURIComponent(token)}`).then((data) => data.json()).then((data) =>{
  console.log(data)
  num = 0
  for (listing of data){
    listing.report = listing.houseId
    for (const type of RELattr) {
        replace(
          `REL-${num}-${type}`,
          listing[type] ?? "unknown"
        );
      }
    document.getElementById(`REL-${num}-report`).href = `./report.html?houseId=${listing.houseId}`
    document.getElementById(`REL-${num}-price`).addEventListener("click", buyListing);

    num += 1 
  }
})