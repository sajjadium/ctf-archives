if (window.__SESSION__ && window.__SESSION__.username && window.__SESSION__.cereal) {
    let header = document.createElement('h2');
    header.innerText = "Welcome back, " + window.__SESSION__.username;
    let img = document.createElement('img');
    img.src = window.__SESSION__.cereal;
    document.body.appendChild(header);
    document.body.appendChild(img);
}

const fileUploadInput = document.getElementById('cereal');
const fileDataInput = document.getElementById('cereal-data');

fileUploadInput.addEventListener('change', async (event) => {
    let formData = new FormData();           
    formData.append("cereal", event.target.files[0]);
    const res = await fetch('/upload', {
      method: "POST", 
      body: formData
    });
    const data = await res.json();
    fileDataInput.value = data.url;
})