<?php
class Smtp_Sender {
    private $host, $port, $mail;

    function __construct($mail) {
        $this->host = Smtp_Config::$host;
        $this->port = Smtp_Config::$port;
        $this->mail = $mail;
    }

    private function GetResponse($socket) {
        $code = false;
        $data = "";
        do {
            $line = fgets($socket);
            if (! $line) {
                break;
            }
            $code = substr($line, 0, 3);
            $data .= substr($line, 4);
        } while ($line[3] == '-');
        return [$code, $data];
    }

    function __toString() {
        $socket = fsockopen($this->host, $this->port, $nul, $nul, 2);
        if (! $socket) {
            return "Connection error";
        }
        stream_set_timeout($socket, 5);

        list ($code, $banner) = $this->GetResponse($socket);
        if ($code != 220) {
            return "Bad SMTP banner: '" . trim($banner) . "'";
        }

        fwrite($socket, "EHLO " . gethostname() . "\r\n");
        list ($code, $response) = $this->GetResponse($socket);
        if ($code != 250) {
            return "Bad EHLO response: '" . trim($response) ."'";
        }

        fwrite($socket, "MAIL FROM: <" . $this->mail->GetFrom() . ">\r\n");
        list ($code, $response) = $this->GetResponse($socket);
        if ($code != 250) {
            return "Bad MAIL response: '" . trim($response) ."'";
        }

        fwrite($socket, "RCPT TO: <" . $this->mail->GetTo() . ">\r\n");
        list ($code, $response) = $this->GetResponse($socket);
        if ($code != 250) {
            return "Bad RCPT response: '" . trim($response) ."'";
        }

        fwrite($socket, "DATA\r\n");
        list ($code, $response) = $this->GetResponse($socket);
        if ($code != 354) {
            return "Bad DATA response: '" . trim($response) ."'";
        }

        $data = $this->mail->GetData();
        do {
            $sent = fwrite($socket, $data);
            $data = substr($data, $sent);
        } while ($sent && strlen($data));
        fwrite($socket, "\r\n.\r\nQUIT\r\n");
        return stream_get_contents($socket);
    }
}
