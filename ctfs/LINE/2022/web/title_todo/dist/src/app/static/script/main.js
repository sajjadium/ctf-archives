function previewAndUploadFile() {
    const imgFile = document.getElementById('imgInput').files[0];
    const preview = document.getElementById('preview');

    const img = document.createElement("img");
    img.src = URL.createObjectURL(imgFile)
    preview.appendChild(img);

    const formData = new FormData();
    formData.append("img_file", imgFile)

    fetch('/image/upload', {
        method: 'POST',
        body: formData
    }).then((res) => {
        return (res.json())
    }).then((data) => {
        console.log(data['img_url'])
        document.getElementById('img_url').value = data['img_url']
    })

    document.getElementById('create-submit').removeAttribute('disabled')
}


function share(){
    const imgId = document.getElementById('imgId').value;

    fetch('/share', {
        method: 'POST',
        body: JSON.stringify({path: `image/${imgId}`}),
        headers: {
            'Content-type': 'application/json'
        }
    }).then((res) => {
        if (res.status == 200) {
            shareButton = document.getElementById('shareButton')
            shareButton.setAttribute('disabled', true)
            shareButton.value = 'Shared'
            shareButton.innerText = 'Shared'
        } else {
            return res.json()
        }
    }).then((data) => {
        if (data['error']){
            alert(data['error'])
        }
    })
}

imgInput = document.getElementById('imgInput')
if (imgInput) { imgInput.onchange = previewAndUploadFile}
shareButton = document.getElementById('shareButton')
if (shareButton) { shareButton.onclick = share}