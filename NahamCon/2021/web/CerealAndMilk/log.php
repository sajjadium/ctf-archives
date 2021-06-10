<?php

class log
{
    public function __destruct()
        {
            $request_log = fopen($this->logs , "a");
            fwrite($request_log, $this->request);
            fwrite($request_log, "\r\n");
            fclose($request_log);
        }
}

?>
