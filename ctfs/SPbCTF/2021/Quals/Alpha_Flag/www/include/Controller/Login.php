<?php
class Controller_Login extends Controller {
    function Process($parameters) {
        $result = "";

        if ($_SERVER['REQUEST_METHOD'] == "POST") {
            $login = $_POST['login'];
            $password = $_POST['password'];

            if (empty($login)) {
                $result .= "Enter login<br/>";
            }
            if (empty($password)) {
                $result .= "Enter password<br/>";
            }

            if ($result === "") {
                $user = new User($login, $password);
                if ($user->CheckPassword()) {
                    $session = new Misc_Session();
                    $session->Set('login', $login);
                    $session->Set('password', $password);
                    (new Misc_Redirector($user->GetProven() ? '/inbox' : '/prove'))->Redirect();
                } else {
                    $result .= "Wrong password</br>";
                }
            }
        }

        $title = "Login";
        $head = "";
        $body = new Template_Login();
        $body->AssignVariable('login_result', $result);

        return [$title, $head, $body];
    }
}
