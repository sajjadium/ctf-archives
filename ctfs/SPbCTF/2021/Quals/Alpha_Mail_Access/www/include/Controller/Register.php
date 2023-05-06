<?php
class Controller_Register extends Controller {
    function Process($parameters) {
        $result = "";

        if ($_SERVER['REQUEST_METHOD'] == "POST") {
            $login = $_POST['login'];
            $password = $_POST['password'];
            $password2 = $_POST['password2'];

            if (empty($login)) {
                $result .= "Enter login<br/>";
            }
            if (empty($password)) {
                $result .= "Enter password<br/>";
            }
            if (empty($password2)) {
                $result .= "Enter confirmation<br/>";
            }

            if ($result === "") {
                if ($password !== $password2) {
                    $result .= "Enter passwords steadily<br/>";
                }
            }

            if ($result === "") {
                if ((new User($login, ""))->Exists()) {
                    $result .= "Login already taken<br/>";
                }

                if ((new User($login, $password))->Add()) {
                    $result .= "Registered</br>";
                } else {
                    $result .= "Failed. Try again</br>";
                }
            }
        }

        $title = "Register";
        $head = "";
        $body = new Template_Register();
        $body->AssignVariable('reg_result', $result);

        return [$title, $head, $body];
    }
}
