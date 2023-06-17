<?php
    include("config.php");

    if(!is_login()) alert("login plz", "back");

    render_page("calculate");
?>