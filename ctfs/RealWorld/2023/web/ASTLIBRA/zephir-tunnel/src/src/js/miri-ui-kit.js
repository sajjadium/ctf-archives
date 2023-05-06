/*!
    Miri UI Kit Free V1.0.0
    Developed by BootstrapDash(https://www.bootstrapdash.com/)
*/

function fixnavbaronScroll() {
    if ($('.fixed-on-scroll').length) {
        if ($(this).scrollTop() >= $('.fixed-on-scroll').height()) {
            $('.fixed-on-scroll').addClass('fixed-on-top');
            $('.fixed-on-scroll .navbar-brand img').prop('src','assets/images/logo-dark.svg')
        } else {
            $('.fixed-on-scroll').removeClass('fixed-on-top');
            $('.fixed-on-scroll .navbar-brand img').prop('src','assets/images/logo.svg')
        }
    }
}

// Select all links with hashes
$('a[href*="#"]')
// Remove links that don't actually link to anything
.not('[href="#"]')
.not('[href="#!"]')
.click(function (event) {
    // On-page links
    if (
        location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '')
        &&
        location.hostname == this.hostname
    ) {
        // Figure out element to scroll to
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        // Does a scroll target exist?
        if (target.length) {
            // Only prevent default if animation is actually gonna happen
            event.preventDefault();
            $('html, body').animate({
                scrollTop: target.offset().top
            }, 1000, function () {
                // Callback after animation
                // Must change focus!
                var $target = $(target);
                $target.focus();
                if ($target.is(":focus")) { // Checking if the target was focused
                    return false;
                } else {
                    $target.attr('tabindex', '-1'); // Adding tabindex for elements not focusable
                    $target.focus(); // Set focus again
                };
            });
        }
    }
});

$(document).ready(function () {

    fixnavbaronScroll();

    $(window).scroll(function () {

        fixnavbaronScroll();

    });

    $('[data-toggle="lightbox"]').on('click',function(){
        revealVideo($(this).data('target'));
    })

    $('[data-close="lightbox"]').on('click',function(){
        hideVideo($(this).parents('.lightbox'));
    })

    $('.lightbox').click(function() {
        hideVideo($(this));
    })
});

// Function to reveal lightbox and adding YouTube autoplay
function revealVideo(lightboxId) {
    $(lightboxId).fadeIn();
}

// Hiding the lightbox and removing YouTube autoplay
function hideVideo(lightboxId) {
    $(lightboxId).fadeOut();
}

