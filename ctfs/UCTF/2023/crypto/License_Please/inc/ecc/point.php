<?php

namespace Ecc;

use GMP;

class Point
{
    private static ?Point $inf = null;

    public readonly GMP $x, $y;

    public function __construct(GMP $x, GMP $y)
    {
        $this->x = $x;
        $this->y = $y;
    }

    public static function infinity()
    {
        if (Point::$inf === null) {
            Point::$inf = new Point(gmp_init(0), gmp_init(0), null);
        }

        return Point::$inf;
    }

    public function __toString()
    {
        return '(' . gmp_strval($this->x, 16) . ', ' . gmp_strval($this->y, 16) . ')';
    }
}

class PointOp
{
    public readonly GMP $a, $prime;

    public function __construct(GMP $a, GMP $prime)
    {
        $this->a = $a;
        $this->prime = $prime;
    }

    public function add(Point $p, Point $q): Point
    {
        if ($p == Point::infinity())
            return $q;
        if ($q == Point::infinity())
            return $p;

        if ($p == $q)
            return $this->double($p);

        if (gmp_cmp($p->x, $q->x) == 0) {
            return Point::infinity();
        }

        $s = gmp_mul(gmp_sub($q->y, $p->y), gmp_invert(gmp_sub($q->x, $p->x), $this->prime));

        $x = gmp_mod(gmp_sub(gmp_sub(gmp_pow($s, 2), $q->x), $p->x), $this->prime);
        $y = gmp_mod(gmp_sub(gmp_mul($s, gmp_sub($q->x, $x)), $q->y), $this->prime);

        return new Point($x, $y);
    }

    public function double(Point $p): Point
    {
        if ($p == Point::infinity())
            return $p;

        $s = gmp_mul(
            gmp_add(gmp_mul(3, gmp_pow($p->x, 2)), $this->a),
            gmp_invert(gmp_mul(2, $p->y), $this->prime)
        );

        $x = gmp_mod(gmp_sub(gmp_pow($s, 2), gmp_mul(2, $p->x)), $this->prime);
        $y = gmp_mod(gmp_sub(gmp_mul($s, gmp_sub($p->x, $x)), $p->y), $this->prime);

        return new Point($x, $y);
    }

    public function multiply(Point $p, GMP $n): Point
    {
        $res = Point::infinity();
        $tmp = $p;

        $bits = strlen(gmp_strval($n, 2));
        for ($i = 0; $i < $bits; $i++) {
            if (gmp_testbit($n, $i)) {
                $res = $this->add($res, $tmp);
            }

            $tmp = $this->double($tmp);
        }

        return $res;
    }
}
