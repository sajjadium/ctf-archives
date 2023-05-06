<?php
abstract class Proven_Controller extends Authenticated_Controller {
    function __construct() {
        parent::__construct();
        $session = new Misc_Session();
        if (! $session->User()->GetProven()) {
            (new Misc_Redirector("/"))->Redirect();
        }
    }
}
