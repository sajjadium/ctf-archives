<?php
class Misc_Router {
    private $url, $page, $parameters;

    function __construct($url) {
        $this->url = $url;
        list ($this->url) = explode("?", $this->url);
        $fragments = explode("/", $this->url);
        array_shift($fragments);

        $this->parameters = $fragments;
        $this->page = array_shift($this->parameters);
    }

    function getPage() {
        return $this->page;
    }

    function getParameters() {
        return $this->parameters;
    }

    function __toString() {
        return "[" . __CLASS__ . ": " . $this->url . "]";
    }
}
