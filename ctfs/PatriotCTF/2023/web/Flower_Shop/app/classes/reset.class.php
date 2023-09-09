<?php

include "../modules/helpers.php";

class Reset extends Dbh {

    protected function checkUser($uid) {
        if (empty($uid)) {
            header("location: ../login.php?error=EmptyUser");
            exit();
        }

        $stmt = $this->connect()->prepare('SELECT * FROM users where username = :username');
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

        $wh = $user[0]["webhook"];
        return $wh;

    }

    protected function tmpPwd($uid) {
        $tmpPass = genTmpPwd();
        $tmpHash = password_hash($tmpPass, PASSWORD_DEFAULT);

        $stmt = $this->connect()->prepare('UPDATE users SET password = :password, tmp_pass_time = :tmp_pass_time WHERE username = :username');
        $stmt->bindValue(':username', $uid);
        $stmt->bindValue(':password', $tmpHash);
        $stmt->bindValue(':tmp_pass_time', time());
        
        if (!$stmt->execute()) {
            $errorInfo = $stmt->errorInfo();
            $errorMessage = $errorInfo[2];
            $stmt = null;
            header("location: ../login.php?error=" . $errorMessage);
            exit();
        }

        $stmt = null;
        return $tmpPass;
    }

}


class ResetController extends Reset {

    private $uid;
    private $wh;
    private $tmpPass;

    public function __construct($uid) {
        $this->uid = $uid;
    }

    public function resetPassword() {
        $this->wh = $this->checkUser($this->uid);
        if (!$this->wh) {
            header("location: ../login.php?error=InvalidUser");
            exit();
        }

        $this->tmpPass = $this->tmpPwd($this->uid);

        exec("php ../scripts/send_pass.php " . $this->tmpPass . " " . $this->wh . " > /dev/null 2>&1 &");

        return $this->tmpPass;
    }

}

?>