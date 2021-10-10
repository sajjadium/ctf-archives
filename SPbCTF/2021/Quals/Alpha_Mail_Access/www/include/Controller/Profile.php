<?php
class Controller_Profile extends Proven_Controller {
    function Process($parameters) {
        $result = "";

        $user = (new Misc_Session())->User();

        if ($_SERVER['REQUEST_METHOD'] == "POST") {
            $password = $_POST['password'];
            $profile = $_POST['profile'] ?: [];

            if (!empty($password)) {
                $user->UpdatePassword($password);
                $result .= "Password set<br/>";
            }

            $user->UpdateProfile($profile);
            $result .= "Profile saved<br/>";
        }

        $profileStr = "";
        foreach ($user->GetProfile() as $key => $value) {
            $profileStr .= '<tr><td align="right">' . htmlspecialchars(new Misc_ProfanityFilter(ucfirst($key))) . '</td><td align="left"><input type="text" name="profile[' . htmlspecialchars(new Misc_ProfanityFilter($key)) . ']" value="' . htmlspecialchars(new Misc_ProfanityFilter($value)) . '" /></td></tr>';
        }
        $vars = [
            'login' => htmlspecialchars($user->GetLogin()),
            'proven' => $user->GetProven() ? "Yes" : "No",
            'profile' => $profileStr,
        ];

        $title = "Profile";
        $head = "";
        $body = new Template_Profile();
        $body->AssignVariables($vars);
        $body->AssignVariable('profile_result', $result);

        return [$title, $head, $body];
    }
}
