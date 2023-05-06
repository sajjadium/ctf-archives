<?php
class Misc_Redirector {
    private $location;

    function __construct($location) {
        $this->location = new Misc_ProfanityFilter($location);
    }

    function Redirect() {
        ob_end_clean();
        header("Location: $this->location", true, 302);
        exit;
    }
}
