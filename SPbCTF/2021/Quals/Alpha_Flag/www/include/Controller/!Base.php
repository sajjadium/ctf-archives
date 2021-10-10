<?php
abstract class Controller {
    function __construct() {

    }

    abstract function Process($parameters);

    function __toString() {
        return "[" . __CLASS__ . "]";
    }
}
