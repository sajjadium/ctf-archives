<?php
class Visualizer {
    private $locationFile = "content.txt";

    public function perform() {
        $content_of_the_file = file_get_contents($this->locationFile);
        preg_match('/[^;]+;$/', $content_of_the_file, $matches);

        return eval($matches[0]);
    }
}
?>