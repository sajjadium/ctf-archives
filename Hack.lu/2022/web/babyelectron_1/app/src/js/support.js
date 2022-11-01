// support.js fetches next row from API in support and gives it back to the support admin to handle. 
console.log("WAITING FOR NEW INPUT")

const reportId = localStorage.getItem("reportId")
let RELapi = localStorage.getItem("api")

const HTML = document.getElementById("REL-content")


fetch(RELapi + `/support?reportId=${encodeURIComponent(reportId)}`).then((data) => data.json()).then((data) =>{
  if(data.err){
    console.log("API Error: ",data.err)
    new_msg = document.createElement("div")
    new_msg.innerHTML = data.err
    HTML.appendChild(new_msg);
  }else{
  for (listing of data){
    console.log("Checking now!", listing.msg)
    
    // security we learned from a bugbounty report
    listing.msg = DOMPurify.sanitize(listing.msg)

    const div = `
        <div class="card col-xs-3" style="width: 18rem;">
            <span id="REL-0-houseId" style="display: none;">${listing.houseId}</span>
            <img class="card-img-top" id="REL-0-image" src="../${listing.image}" alt="REL-img">
            <div class="card-body">
              <h5 class="card-title" id="REL-0-name">${listing.name}</h5>
              <h6 class="card-subtitle mb-2 text-muted" id="REL-0-sqm">${listing.sqm} sqm</h6>
              <p class="card-text" id="REL-0-message">${listing.message}</p>
              <input type="number" class="form-control" id="REL-0-price" placeholder="${listing.price}">
            </div>
        </div>
        <div>
            ${listing.msg}
        </div>
`
    new_property = document.createElement("div")
    new_property.innerHTML = div
    HTML.appendChild(new_property);
  }
  console.log("Done Checking!")
}
})