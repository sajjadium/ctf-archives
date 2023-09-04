function load_the_monkes() {
    var total_monkes = 6;
    var total_columns = 5;
    var total_rows = 5;
    var monke_index = 0;

    for (var x=1; x <= total_rows + 1; x++) {
        for (var y=1; y <= total_columns; y++) {
            monke_index = Math.floor(Math.random() * total_monkes);
            $('#monke-bg').append($("<img />",{
                id : 'monke-img',
                style : "grid-row: " + x + + "; grid-column: " + y,
                src : "/images/background/monke" + monke_index + ".gif"
            }).delay(1000 + 500*(x*total_columns + y)).fadeTo(1000, 0.8));
        }
    }
}

$(() => {
    let getParams = new URLSearchParams(window.location.search);
    if (!getParams.has("nomonkes")) {load_the_monkes();}
    $('section').delay(500).fadeIn(500);
});