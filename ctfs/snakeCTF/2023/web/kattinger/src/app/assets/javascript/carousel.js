document.addEventListener('DOMContentLoaded', function() {
    var elems =document.querySelectorAll('.carousel');
    var instances =M.Carousel.init(elems, {padding: 300, fullWidth: true, numVisible: 3});
  });

setTimeout(() => {
    var imgs =document.getElementById("cat-img-carousel");
    var descs =document.getElementById("cat-desc-carousel");
    var imgs_instance =M.Carousel.getInstance(imgs);
    var descs_instance =M.Carousel.getInstance(descs);
    // Go on or restart if on error
    if(! (imgs_instance && descs_instance)) {
      location.reload(0); // Fugging sheet not working aint it
    }
},  300);

setInterval(() => {
    var imgs =document.getElementById("cat-img-carousel");
    var descs =document.getElementById("cat-desc-carousel");
    var imgs_instance =M.Carousel.getInstance(imgs);
    var descs_instance =M.Carousel.getInstance(descs);
    
    // Resync if user moved it
    if(imgs_instance.center !=descs_instance.center)
      descs_instance.set(imgs_instance.center)
    else {
      imgs_instance.next();
      descs_instance.next();
      imgs.remove
    }
}, 2000);