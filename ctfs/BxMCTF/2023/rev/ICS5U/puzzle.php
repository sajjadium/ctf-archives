<?php

/* Hmm, what does this program seem to do? */

function alpha($a, $b)
{
    if ($a < $b)
    {
        return alpha($b, $a);
    }
    
    if ($a % $b == ($a ^ $a))
    {
        return $b;
    }
    
    return alpha($b, $a % $b);
}

function beta($x, $y, $z)
{
    $ans = 1;

    if ($y & 1 != 0)
    {
        $ans = $x;
    }

    while ($y != 0)
    {
        $y >>= 1;
        $x = ($x * $x) % $z;

        if ($y & 1 != 0)
        {
            $ans = ($ans * $x) % $z;
        }
    }

    return $ans;
}

function gamma($n)
{
    for ($_ = 2; $_ <= $n; ++$_)
    {
        
        if (alpha($_, $n) == 1)
        {
            
            if (beta($_, $n - 1, $n) != 1)
            {
                return 0;
            }
        }
    }
    
    return 1;
}

function init($n)
{
    $check = (gamma($n) == 1 ? true : false);

    if ($check)
    {
        echo('YES');
    }

    else
    {
        echo('NO');
    }
}

?>
