<?php

namespace Ecc;

require_once 'point.php';

use GMP;

interface Curve
{
    public static function getInstance(): Curve;

    public function name(): string;

    public function p(): GMP;
    public function a(): GMP;
    public function b(): GMP;
    public function G(): Point;
    public function n(): GMP;
    public function h(): GMP;

    public function validate(Point $p);
}

class CurveP256 implements Curve
{
    private readonly GMP $p;
    private readonly GMP $a;
    private readonly GMP $b;
    private readonly Point $G;
    private readonly GMP $n;
    private readonly GMP $h;

    private static ?CurveP256 $curve = null;

    private function __construct()
    {
        $this->p = gmp_init('0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff');
        $this->a = gmp_init('0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc');
        $this->b = gmp_init('0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b');
        $this->G = new Point(
            gmp_init('0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296'),
            gmp_init('0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5')
        );
        $this->n = gmp_init('0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551');
        $this->h = gmp_init('0x1');
    }

    public static function getInstance(): CurveP256
    {
        if (CurveP256::$curve === null) {
            CurveP256::$curve = new CurveP256();
        }
        return CurveP256::$curve;
    }

    public function name(): string
    {
        return "P-256";
    }
    public function p(): GMP
    {
        return $this->p;
    }
    public function a(): GMP
    {
        return $this->a;
    }
    public function b(): GMP
    {
        return $this->b;
    }
    public function G(): Point
    {
        return $this->G;
    }
    public function n(): GMP
    {
        return $this->n;
    }
    public function h(): GMP
    {
        return $this->h;
    }

    public function validate(Point $p): bool
    {
        $f = gmp_mod(gmp_pow($p->y, 2), $this->p);
        $s = gmp_mod(gmp_add(gmp_add(gmp_pow($p->x, 3), gmp_mul($this->a, $p->x)), $this->b), $this->p);
        return (gmp_cmp($f, $s) === 0);
    }
}
