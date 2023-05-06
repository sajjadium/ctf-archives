<?php
class Controller_Captcha extends Authenticated_Controller {
    function Process($parameters) {
        ob_end_clean();
        header("Content-Type: image/png", true);
        echo new Captcha();
        exit;
    }
}
