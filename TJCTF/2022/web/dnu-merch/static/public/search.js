const searchElement = document.getElementById('search-results-subhead')
const resultCardsElement = document.getElementById('result-cards')
const search = new URLSearchParams(window.location.search).get('search') ?? ""

const cookies = {};
document.cookie.split(";").forEach((s) => {
  if (s) {
    const [key, val] = s.split("=");
    cookies[key] = JSON.parse(decodeURIComponent(val))
  }
})

function searchForItem(keyword) {
  return cookies["items"].filter(({title}) => title.startsWith(keyword))
}
let filteredSearch = search.split(", ").map(keyword => searchForItem(keyword)).reduce((a, b) => a.concat(b))

searchElement.innerHTML = filteredSearch && filteredSearch.length ? `Results for: "${search}"` : "Results not found."

filteredSearch.forEach(({title, cost, img}) => {
  resultCardsElement.innerHTML += `<div class="result-card"><div class="img-bg"><img class="img-merch" src="${img}" /></div><h3 class="result-card-title">${title}</h3><h5 class="result-card-cost">$${cost}</h5></div>`
})
