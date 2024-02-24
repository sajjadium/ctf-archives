
const galleryDiv = document.querySelector('.gallery');

  document.addEventListener('DOMContentLoaded', function () {

    const gallery = document.querySelector('.gallery');

    gallery.addEventListener('click', function (e) {
      if (e.target.tagName === 'IMG') {
        const modal = new bootstrap.Modal(document.getElementById('imageModal'));
        const modalImage = document.getElementById('modalImage');
        const deletebtn = document.getElementById("delete")
        modalImage.src = e.target.src;
        deletebtn.addEventListener('click',() => window.location=`/delete?file=${e.target.src.split('/').pop()}`)
        modal.show();
      }
    });
  });

    if(fileNames){
        for(i=0;i<fileNames.length;i++){
          fileName = fileNames[i]
          const imgElement = document.createElement('img');
          imgElement.src = `/static/${id}/${fileName}`;

          imgElement.alt = `Image: ${fileName}`;

          galleryDiv.appendChild(imgElement);
        }

    } 