<?php
include_once "header.php";
?>


<h1 class="text-center my-5">Choose from our superb variety of magicians</h1>

<div class="grid text-center">
    <?php
    $magicians = scandir("./magicians");
    foreach ($magicians as $magician) {
        if ($magician == "." or $magician == "..") continue;

        $name = htmlspecialchars(explode("magic", $magician)[0], ENT_QUOTES, "UTF-8");
        $path = "/magicians/" . $magician;

        echo
        "<div class='text-center mb-5'>
            <p>$name</p>
            <img src='$path' class='magician-image'/>
        </div>";
    }
    ?>
</div>
