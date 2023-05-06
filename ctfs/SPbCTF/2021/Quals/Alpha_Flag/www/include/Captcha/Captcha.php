<?php
class Captcha {
    private $string;

    function __construct() {
        $session = new Misc_Session();
        if (! $session->Get('captcha')) {
            $session->Set('captcha', str_pad(mt_rand(0, 999999999), 9, "0", STR_PAD_LEFT));
        }
        $this->string = $session->Get('captcha');
    }

    function Verify($string) {
        $session = new Misc_Session();
        $session->Delete('captcha');
        return $string === $this->string;
    }

    function __toString() {
        $session = new Misc_Session();
        $session->Set('captcha', str_pad(mt_rand(0, 999999999), 9, "0", STR_PAD_LEFT));
        $this->string = new Misc_ProfanityFilter($session->Get('captcha'));

        $image = imagecreatetruecolor(300, 100);
        imagefill($image, 0, 0, 0xffffff);

        $x = mt_rand(10, 50);
        $colors = [0xff0000, 0x00ff00, 0x2020ff, 0xff20ff, 0x202020, 0xff0000, 0x2020ff, 0x00ff00, 0xff20ff];
        foreach (str_split($this->string) as $i => $char) {
            $fgColor = imagecolorallocatealpha($image, ($colors[$i] >> 16) & 0xff, ($colors[$i] >> 8) & 0xff, $colors[$i] & 0xff, 70);
            $y = mt_rand(70, 95);
            imagettftext($image, 60, 0, $x, $y, $fgColor, dirname(__FILE__) . "/impact.ttf", $char);
            $x += mt_rand(20, 25);
        }

        ob_start();
        imagepng($image);
        $imagePng = ob_get_contents();
        ob_end_clean();

        return $imagePng;
    }
}
