<?php
require __DIR__ . '/vendor/autoload.php';
use MiladRahimi\Jwt\Parser;
use MiladRahimi\Jwt\Cryptography\Algorithms\Hmac\HS256;

require_once('md5Hashes.php');

class Handler {

    function md5ObjectManager($claims) {
        $unserialized = unserialize(base64_decode($claims['md5Searcher']));
        die("[Returned]: " . $unserialized);
    }

    function perform() {
        include("db_connector.php");

        $signer = new HS256($token);

        // Parse the JWT
        $parser = new Parser($signer);
        if (isset($_COOKIE) && !empty($_COOKIE['decodeMyJwt'])) {
            $jwt = $_COOKIE['decodeMyJwt'];
            $claims = $parser->parse($jwt);
            // Authorized request, proceeding to return the visualized content
            //print_r($claims);
            if (isset($claims['md5Searcher']) && !empty($claims['md5Searcher'])) {
                return $this->md5ObjectManager($claims);
            }
        }

        return "Unauthorized";
    }

    public function __toString() {
        return $this->perform();
    }
}
?>