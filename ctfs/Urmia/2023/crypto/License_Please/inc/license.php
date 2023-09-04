<?php

require_once 'ecc/curve.php';
require_once 'ecc/point.php';
require_once 'ecc/signature.php';

use Ecc\Curve;
use Ecc\Point;
use Ecc\Signature;

class License implements JsonSerializable
{
    public readonly string $user;
    public readonly DateTime $expire;
    public readonly bool $demo;
    public readonly Signature $signature;

    private function __construct(string $user, DateTime $expire, bool $demo, Signature $signature)
    {
        $this->user = $user;
        $this->expire = $expire;
        $this->demo = $demo;
        $this->signature = $signature;
    }

    public static function new(string $user, string $expire, bool $demo, GMP $privkey, Curve $curve): License
    {
        $exp = new DateTime();
        $exp->modify($expire);

        $sig_data =  $user . $exp->format(DateTime::ISO8601_EXPANDED) . var_export($demo, true);
        $sig = Signature::of($sig_data, $privkey, $curve);

        return new License($user, $exp, $demo, $sig);
    }

    public static function import(string $json, Point $pubkey, Curve $curve): License
    {
        $json_dec = json_decode($json, true);
        if ($json_dec === null) {
            throw new LicenseInvalidFormatException();
        }

        $user = $json_dec['user'] ?? null;
        $expire = $json_dec['expire'] ?? null;
        $demo = $json_dec['demo'] ?? null;
        $signature = $json_dec['signature'] ?? null;
        if ($user === null || $expire === null || $demo === null || $signature === null) {
            throw new LicenseInvalidFormatException('Missing fields');
        }

        try {
            $sig = Signature::import($signature);
        } catch (ValueError) {
            throw new LicenseInvalidSignatureException();
        }
        $sig_data = $user . $expire . var_export($demo, true);
        if ($sig->verify($sig_data, $pubkey, $curve) === false) {
            throw new LicenseInvalidSignatureException();
        }

        try {
            $exp = new DateTime($expire);
        } catch (Exception) {
            throw new LicenseInvalidFormatException();
        }
        $now = new DateTime();
        if ($exp <= $now) {
            throw new LicenseExpiredException();
        }

        return new License($user, $exp, $demo, $sig);
    }

    public function jsonSerialize(): mixed
    {
        return [
            'user' => $this->user,
            'expire' => $this->expire->format(DateTime::ISO8601_EXPANDED),
            'demo' => $this->demo,
            'signature' => $this->signature,
        ];
    }

    public function __toString()
    {
        return json_encode($this);
    }
}

class LicenseInvalidFormatException extends Exception
{
    public function __construct($message = 'Invalid license format', $code = 0, Exception $previous = null)
    {
        parent::__construct($message, $code, $previous);
    }
}

class LicenseInvalidSignatureException extends Exception
{
    public function __construct($message = 'Invalid signature', $code = 0, Exception $previous = null)
    {
        parent::__construct($message, $code, $previous);
    }
}

class LicenseExpiredException extends Exception
{
    public function __construct($message = 'Expired license', $code = 0, Exception $previous = null)
    {
        parent::__construct($message, $code, $previous);
    }
}
