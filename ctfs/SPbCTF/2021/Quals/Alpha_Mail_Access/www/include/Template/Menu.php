<?php
class Template_Menu extends Template {
    protected $template = "";

    function __construct($page) {
        $items = [
            '' => "Main Page",
        ];

        $session = new Misc_Session();
        $isAuthenticated = $session->Authenticated();
        $isProven = $isAuthenticated && $session->User()->GetProven();

        if ($isAuthenticated) {
            if ($isProven) {
                $items += [
                    'inbox' => "Inbox",
                    'compose' => "Compose",
                    'profile' => "Profile",
                ];
            } else {
                $items += [
                    'prove' => "Prove",
                ];
            }
            $items += [
                'logout' => "Logout",
            ];
        } else {
            $items += [
                'register' => "Register",
                'login' => "Login",
            ];
        }

        foreach ($items as $itemPage => $itemTitle) {
            if ($itemPage == $page) {
                $this->template .= "<em>$itemTitle</em><br/>";
            } else {
                $this->template .= "<a href='/$itemPage'>$itemTitle</a><br/>";
            }
        }

        if ($isAuthenticated) {
            $this->template .= "<br/>Logged in as<br/>{user}";
            $this->AssignVariable('user', $session->User()->GetLogin());
        }
    }
}
