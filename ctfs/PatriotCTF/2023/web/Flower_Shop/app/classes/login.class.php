<?php

class Login extends Dbh {

    protected function getUser($uid, $pwd) {

        $stmt = $this->connect()->prepare('SELECT * FROM users WHERE username = :username');
        $stmt->bindValue(':username', $uid);
        
        if (!$stmt->execute()) {
            $stmt = null;
            header("location: ../login.php?error=stmtfaild");
            exit();
        }

        $user = $stmt->fetchAll(PDO::FETCH_ASSOC);
        if ($user == false) {
            $stmt = null;
            header("location: ../login.php?error=UserNotFound");
            exit();
        }

        $pwdHashed = $user[0]["password"];
        $checkPwd = password_verify($pwd, $pwdHashed);

        if ($checkPwd == false) { 
            $stmt = null;
            header("location: ../login.php?error=WrongPassword");
            exit();
        } else { 
            if (isset($user[0]["tmp_pass_time"])) {
                $currTime = time();
                $tempTime = $user[0]["tmp_pass_time"];
                $delta = $currTime - $tempTime;
                
                if ($delta > 3600) {
                    header("location: ../login.php?error=TempPassExpired");
                    exit();
                } else {
                    $stmt = $this->connect()->prepare('UPDATE users SET tmp_pass_time = NULL WHERE username = :username');
                    $stmt->bindValue(':username', $uid);
                    
                    if (!$stmt->execute()) {
                        $stmt = null;
                        header("location: ../login.php?error=stmtfaild");
                        exit();
                    }
                }
            }
            
            session_start();
            $_SESSION["userid"] = $user[0]["user_id"];
            $_SESSION["username"] = $user[0]["username"];
            
            $stmt = null;
        }        
    }
}

class LoginController extends Login {

    private $uid;
    private $pwd;

    public function __construct($uid, $pwd) {
        $this->uid = $uid;
        $this->pwd = $pwd;
    }

    public function loginUser() {
        if (empty($this->uid)) {
            header("location: ../login.php?error=EmptyInput");
            exit();
        }

        $this->getUser($this->uid, $this->pwd);
    }
}

?>
