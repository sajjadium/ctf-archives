<?php
foreach (glob(dirname(__FILE__) . "/*/*.php") as $fileName) {
    require_once $fileName;
}
