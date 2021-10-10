<?php
class User {
    private $db, $hostname;
    private $login, $password, $proven = 0, $profile = [];

    function __construct($login, $password) {
        $this->db = Db::Instance();
        $this->hostname = gethostname();

        if (strstr($login, "@")) {
            list ($login, $host) = explode("@", $login);
            if ($host !== $this->hostname) {
                $login = "";
            }
        }
        $login = strtolower($login);
        if (preg_match('/[^a-z0-9-]/', $login)) {
            $login = "";
        }

        $this->login = $login;
        $this->password = $password;
        $this->profile = ['name' => "", 'country' => ""];
        $this->LoadInfo();
    }

    function Add() {
        if ($this->login === "") {
            return false;
        }
        if ($this->Exists()) {
            return false;
        }
        return (bool) $this->db->Insert("users", ['login' => $this->login, 'password' => md5($this->password), 'proven' => $this->proven, 'profile' => serialize($this->profile)]);
    }

    function Exists() {
        if ($this->login === "") {
            return false;
        }
        return (bool) $this->db->Select("users", 1, ['login' => $this->login]);
    }

    function CheckPassword() {
        if ($this->login === "") {
            return false;
        }
        return (bool) $this->db->Select("users", 1, ['login' => $this->login, 'password' => md5($this->password)]);
    }

    function LoadInfo() {
        if ($this->login === "") {
            return;
        }
        if ($this->Exists()) {
            $info = $this->db->Select("users", false, ['login' => $this->login]);
            $this->proven = $info[0]['proven'];
            if (is_array($profile = unserialize($info[0]['profile']))) {
                $this->profile = $profile;
            }
        }
    }

    function GetLogin() {
        return $this->login . "@" . $this->hostname;
    }

    private function GetPassword() {
        return $this->password;
    }

    function GetProven() {
        return $this->proven;
    }

    function GetProfile() {
        return $this->profile;
    }

    function UpdateLogin($newLogin) {
        if (strstr($newLogin, "@")) {
            list ($newLogin, $host) = explode("@", $newLogin);
            if ($host !== $this->hostname) {
                $newLogin = "";
            }
        }
        $newLogin = strtolower($newLogin);
        if (preg_match('/[^a-z0-9-]/', $newLogin)) {
            $newLogin = "";
        }
        if ($newLogin === "") {
            return;
        }
        $result = (bool) $this->db->Update("users", ['login' => $newLogin], ['login' => $this->login]);
        if ($result) {
            $this->login = $newLogin;
        }
    }

    function UpdatePassword($newPassword) {
        $result = (bool) $this->db->Update("users", ['password' => md5($newPassword)], ['login' => $this->login]);
        if ($result) {
            $this->password = $newPassword;
        }
    }

    function UpdateProven($newProven) {
        $result = (bool) $this->db->Update("users", ['proven' => $newProven], ['login' => $this->login]);
        if ($result) {
            $this->proven = $newProven;
            if ($newProven) {
                system("useradd -MN -s /bin/false -u 33 -o " . escapeshellarg($this->login));
                // don't mind me, that's just so that mails are deliverable and readable by web interface. No vuln here
            }
        }
    }

    function UpdateProfile($newProfile) {
        $result = (bool) $this->db->Update("users", ['profile' => serialize($newProfile)], ['login' => $this->login]);
        if ($result) {
            $this->profile = $newProfile;
        }
    }

    function __toString() {
        return "[" . __CLASS__ . ": " . $this->login . "]";
    }
}
