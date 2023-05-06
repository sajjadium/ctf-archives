const HTML = document.getElementById("REL-content")
 

const RELattr = ["image", "name", "sqm", "message", "price", "houseId"]
let RELapi = localStorage.getItem("api");
let token = localStorage.getItem("token");

const replace = (selector , value) => {
  const element = document.getElementById(selector);
  if(element){
      if (/image/.test(selector)) {
          element.src = "../" + value;
      }else{
          element.innerHTML = value;
      }
  }
};


fetch(RELapi + `/portfolio?token=${encodeURIComponent(token)}`).then((data) => data.json()).then((data) =>{
  num = 0
  for (listing of data){
    const div = `
            <span id="REL-${num}-houseId" style="display: none;">${listing.houseId}</span>
            <img class="card-img-top" id="REL-${num}-image" src="../${listing.image}" alt="REL-img" width="290" height="180">
            <div class="card-body d-flex flex-column">
              <h5 class="card-title" id="REL-${num}-name">${listing.name}</h5>
              <h6 class="card-subtitle mb-2 text-muted" id="REL-${num}-sqm">${listing.sqm} sqm</h6>
              <p class="card-text" id="REL-${num}-message">${listing.message}</p>
              <input type="number" class="form-control mt-auto" id="REL-${num}-price" placeholder="${listing.price}">
              <a href="#" class="btn btn-primary mt-auto" id="REL-${num}-sell">Sell</a>
            </div>
`
    new_property = document.createElement("div")
    new_property.className = 'card col-xs-3'
    new_property.style = "width: 18rem;"
    new_property.innerHTML = div
    HTML.appendChild(new_property); update(num);
    num += 1
  }
})
