<?php
class Misc_Flag {
    private $owner;

    function __construct($owner) {
        $this->owner = $owner;
    }

    function __toString() {
        if ($this->owner->GetLogin() !== "snowden@nsa.gov") {
            return "";
        }
        return "spbctf{...HERE.IS.THE.SECOND.FLAG!!...}";
    }
}
