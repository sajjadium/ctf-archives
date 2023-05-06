<?php
class Controller_Main extends Controller {
    function Process($parameters) {
        $title = "Main Page";
        $head = "";
        $body = new Template_Main();

        return [$title, $head, $body];
    }
}
