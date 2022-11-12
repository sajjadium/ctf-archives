$(document).ready(function() {
    var urlParams = new URLSearchParams(window.location.search);
    var query = urlParams.get('q');

    $('input[id=searchbartext]').val(query);
   
    $.ajax({
        type: "GET", 
        url: "querySearch", 
        data: {query: query},
        success: function(response){
            jQuery.each(response, function() {
                $("#searchresultsarea").append(
                    `<div class="searchresult">
                    <h2>
                        <a class='text-decoration-none' href="${this.site_link}">${this.site_name}</a>
                    </h2>
                    <a class='text-white text-decoration-none'>${this.site_link}</a>
                    <p>${this.site_meta}</p>
                    </div>`
                );
            });
        },
        dataType: "json" 
    })    
});