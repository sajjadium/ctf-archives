<?php

namespace Ecc;

use GMP;
use JsonSerializable;
use Stringable;
use ValueError;

class Signature implements Stringable, JsonSerializable
{
    public const SIG_DELIM = '.';
    public const SIG_HASH = 'sha256';

    public readonly GMP $r, $s;

    private function __construct(GMP $r, GMP $s)
    {
        $this->r = $r;
        $this->s = $s;
    }

    public function verify(string $data, Point $pubkey, Curve $curve): bool
    {
        $hash = hash(Signature::SIG_HASH, $data);
        $h = gmp_init($hash, 16);

        $inv_s = gmp_invert($this->s, $curve->n());
        $u1 = gmp_mod(gmp_mul($h, $inv_s), $curve->n());
        $u2 = gmp_mod(gmp_mul($this->r, $inv_s), $curve->n());

        $op = new PointOp($curve->a(), $curve->p());
        $p = $op->add($op->multiply($curve->G(), $u1), $op->multiply($pubkey, $u2));

        return (gmp_cmp($p->x, $this->r) === 0);
    }

    public static function of(string $data, GMP $privkey, Curve $curve): Signature
    {
        $hash = hash(Signature::SIG_HASH, $data);
        $h = gmp_init($hash, 16);

        gmp_random_seed(time());
        $k = gmp_random_range(1, gmp_sub($curve->n(), 1));

        $op = new PointOp($curve->a(), $curve->p());
        $p = $op->multiply($curve->G(), $k);
        $r = gmp_mod($p->x, $curve->n());

        $inv_k = gmp_invert($k, $curve->n());
        $s = gmp_mod(gmp_mul($inv_k, gmp_add($h, gmp_mul($r, $privkey))), $curve->n());

        return new Signature($r, $s);
    }

    public static function import(string $string): Signature
    {
        $arr = explode(Signature::SIG_DELIM, $string);
        if (count($arr) != 2) {
            throw new ValueError('Invalid string');
        }

        try {
            $r = gmp_init($arr[0], 62);
            $s = gmp_init($arr[1], 62);
        } catch (ValueError $e) {
            throw new ValueError('Failed to parse values');
        }

        return new Signature($r, $s);
    }

    public function __toString()
    {
        return gmp_strval($this->r, 62) . Signature::SIG_DELIM . gmp_strval($this->s, 62);
    }

    public function jsonSerialize(): mixed
    {
        return $this->__toString();
    }
}
