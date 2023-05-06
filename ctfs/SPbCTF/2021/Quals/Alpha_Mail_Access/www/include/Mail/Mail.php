<?php
class Mail {
    private $id, $headers, $body;

    function __construct($id, $data) {
        $this->id = $id;

        $data = str_replace("\r\n", "\n", preg_replace('/^(\s*)(\.\s*)$/m', '\1.\2', $data));
        list ($headers, $this->body) = explode("\n\n", ltrim($data, "\n"), 2);
        $this->headers = [];
        $prevName = false;
        foreach (explode("\n", trim($headers, "\r\n")) as $headerLine) {
            if ($headerLine[0] != " " && $headerLine[0] != "\t") {
                list ($name, $value) = explode(":", $headerLine, 2);
                $name = trim($name);
                $value = trim($value);
                $this->headers[$name] = $value;
                $prevName = $name;
            } elseif ($prevName !== false) {
                $this->headers[$prevName] .= " " . trim($headerLine);
            }
        }
    }

    function GetId() {
        return $this->id;
    }

    function GetBody() {
        return $this->body;
    }

    function GetHeader($name) {
        return isset($this->headers[$name]) ? $this->headers[$name] : false;
    }

    function GetFrom() {
        return $this->GetHeader("From") ?: "<undisclosed sender>";
    }

    function GetTo() {
        return $this->GetHeader("To") ?: "<undisclosed recipients>";
    }

    function GetDate() {
        if (! $this->GetHeader("Date")) {
            return "<unknown date>";
        }
        $time = strtotime($this->GetHeader("Date"));
        if (time() - $time < 3600 * 12) {
            return date("H:i", $time);
        } else {
            return date("Y-m-d", $time);
        }
    }

    function GetSubject() {
        return $this->GetHeader("Subject") ?: "<no subject>";
    }

    function GetData() {
        $data = "";
        foreach ($this->headers as $name => $value) {
            $data .= "$name: $value\r\n";
        }
        $data .= "\r\n";
        $data .= preg_replace('/(?<!\r)\n/', "\r\n", $this->body);
        return $data;
    }

    function __toString() {
        return "<tr><td>" . htmlspecialchars($this->GetFrom()) . "</td><td><a href='/inbox/" . $this->id . "'>" . htmlspecialchars($this->GetSubject()) . "</a></td><td>" . htmlspecialchars($this->GetDate()) . "</td></tr>";
    }
}
