<?php
class Controller_Logout extends Authenticated_Controller {
    function Process($parameters) {
        $session = new Misc_Session();
        $session->Delete('login');
        $session->Delete('password');
        (new Misc_Redirector('/'))->Redirect();
    }
}
