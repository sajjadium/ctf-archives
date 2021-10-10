<?php
abstract class Authenticated_Controller extends Controller {
    function __construct() {
        $session = new Misc_Session();
        if (! $session->Authenticated()) {
            (new Misc_Redirector("/"))->Redirect();
        }
    }
}
