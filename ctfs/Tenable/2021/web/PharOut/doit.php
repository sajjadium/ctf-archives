<?php

class Doit {
        public function __construct()
        {
                $flag = getenv("FLAG");
                echo "flag{{$flag}}\n";
        }
}

?>
