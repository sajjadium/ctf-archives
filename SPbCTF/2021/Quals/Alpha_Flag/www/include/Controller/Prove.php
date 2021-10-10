<?php
class Controller_Prove extends Authenticated_Controller {
    function Process($parameters) {
        $validMethods = ["strength" => true, "stamina" => true, "speed" => true];

        if (!isset($parameters[0]) || !isset($validMethods[$parameters[0]])) {
            $title = "Prove";
            $head = "";
            $body = new Template_Prove_Choose();
        } elseif ($parameters[0] == "strength") {
            $title = "Prove your Strength";
            $head = "";
            $body = new Template_Prove_Strength();
        } elseif ($parameters[0] == "stamina") {
            $title = "Prove your Stamina";
            $head = "";

            $vars = ['message' => ''];
            $session = new Misc_Session();

            if ($session->Has('nextNumber') && time() - $session->Get('lastTime') > 60) {
                $session->Delete('nextNumber');
                $session->Delete('firstTime');
                $vars['message'] .= "No clicks for minute &mdash; lost progress<br/>";
            }

            if ($_SERVER['REQUEST_METHOD'] == "POST") {
                if ($parameters[1] == $session->Get('nextNumber')) {
                    if (! $session->Has('firstTime')) {
                        $session->Set('firstTime', time());
                    }
                    $session->Set('lastTime', time());
                    $session->Set('nextNumber', $session->Get('nextNumber') + 1);

                    if ($session->Get('firstTime') && $session->Get('lastTime') - $session->Get('firstTime') >= 604800) {
                        $vars['message'] .= "Welcome, man.<br/>";
                        $session->User()->UpdateProven(1);
                    }
                }
            }

            $vars['first'] = $session->Has('firstTime') ? date("Y-m-d H:i:s", $session->Get('firstTime')) : "none";
            $vars['last'] = $session->Has('lastTime') ? date("Y-m-d H:i:s", $session->Get('lastTime')) : "none";
            $vars['number'] = (int)$session->Get('nextNumber');

            $body = new Template_Prove_Stamina();
            $body->AssignVariables($vars);
        } elseif ($parameters[0] == "speed") {
            $title = "Prove your Speed";
            $head = "";

            $vars = ['message' => ''];
            $session = new Misc_Session();

            if ($session->Has('correctCount') && time() - $session->Get('firstTime') > 180) {
                $vars['message'] .= "You got " . $session->Get('correctCount') . " in three minutes. Go away.<br/>";
                $session->Delete('correctCount');
                $session->Delete('firstTime');
            }

            if ($_SERVER['REQUEST_METHOD'] == "POST") {
                if ($parameters[1] == $session->Get('correctCount')) {
                    if (! $session->Has('firstTime')) {
                        $session->Set('firstTime', time());
                    }
                    $session->Set('lastTime', time());

                    $captcha = new Captcha();
                    if (! $captcha->Verify($_POST['captcha'])) {
                        $session->Delete('correctCount');
                        $session->Delete('firstTime');
                        $vars['message'] .= "Wrong<br/>";
                    } else {
                        $session->Set('correctCount', $session->Get('correctCount') + 1);

                        if ($session->Get('firstTime') && $session->Get('lastTime') - $session->Get('firstTime') <= 180 && $session->Get('correctCount') >= 100) {
                            $vars['message'] .= "Welcome, man.<br/>";
                            $session->User()->UpdateProven(1);
                        }
                    }
                }
            }

            $vars['first'] = $session->Has('firstTime') ? date("Y-m-d H:i:s", $session->Get('firstTime')) : "none";
            $vars['last'] = $session->Has('lastTime') ? date("Y-m-d H:i:s", $session->Get('lastTime')) : "none";
            $vars['number'] = (int)$session->Get('correctCount');

            $body = new Template_Prove_Speed();
            $body->AssignVariables($vars);
        }

        return [$title, $head, $body];
    }
}
