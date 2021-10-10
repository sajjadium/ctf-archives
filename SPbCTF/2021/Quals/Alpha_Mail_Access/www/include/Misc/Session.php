<?php
class Misc_Session {
    private $user;

    function __construct() {
        $this->user = false;
        if ($this->Has('login') && $this->Has('password')) {
            $this->user = new User($this->Get('login'), $this->Get('password'));
            if (! $this->user->CheckPassword()) {
                $this->user = false;
                $this->Delete('login');
                $this->Delete('password');
            }
        }
    }

    function Has($var) {
        return isset($_SESSION[$var]);
    }

    function Get($var) {
        return isset($_SESSION[$var]) ? $_SESSION[$var] : false;
    }

    function Set($var, $value) {
        $_SESSION[$var] = $value;
    }

    function Delete($var) {
        unset($_SESSION[$var]);
    }

    function Authenticated() {
        return $this->user && $this->user->CheckPassword();
    }

    function User() {
        return $this->user;
    }

    function __toString() {
        return "[" . __CLASS__ . ": " . $this->user . "]";
    }
}
