<?php
class noitpecxe extends Exception
{
    public $error_func = NULL;
    public function __construct($message, $code, $previous = null, $error_func = "printf") {
        // remove when PHP 5.3 is no longer supported
        $this->error_func = $error_func;
        $this->message = $message;
        $previous = NULL;
        //dont care what ur code is LOL!
        $code = 69;
        parent::__construct($message, $code, $previous);
    }

    public function __toString() {
        $error_func = $this->error_func;
        $error_func($this->message);
        return __CLASS__ . ": {$this->code}\n";
    }
}
?>