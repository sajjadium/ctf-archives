<?php

namespace App\Http\Middleware;

use Illuminate\Support\Facades\App;
use Closure;

class ContentLength
{
    public function handle($request, Closure $next)
    {
        $response = $next($request);
        
        if (App::environment('local')) {
            $len = mb_strlen($response->content());
            $response->header('Content-Length', $len);
        }

        return $response;
    }
}
