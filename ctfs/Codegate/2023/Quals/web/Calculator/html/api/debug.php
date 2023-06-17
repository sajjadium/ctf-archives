<?php
    include("../config.php");

    if(!is_login()) alert("login plz", "back");

    $query = array(
        "idx" => $_SESSION["idx"]
    );
    $perm_check = fetch_row("user", $query);
    header("Content-Type: application/json");
    echo json_encode(array("isDebug" => $perm_check["isAdmin"]));
?>