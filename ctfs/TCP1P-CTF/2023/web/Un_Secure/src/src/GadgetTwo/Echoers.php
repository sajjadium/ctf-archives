<?php

namespace GadgetTwo {
    class Echoers
    {
        protected $klass;
        function __destruct()
        {
            echo $this->klass->get_x();
        }
    }
}
