<?php
class Controller_404 extends Controller {
    function Process($parameters) {
        $title = "404";
        $head = "";
        $body = new Template_404();

        return [$title, $head, $body];
    }
}
