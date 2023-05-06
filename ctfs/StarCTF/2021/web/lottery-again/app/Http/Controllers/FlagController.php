<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Exceptions\Exception;
use Laravel\Lumen\Routing\Controller as BaseController;

class FlagController extends BaseController
{
    protected $price = 9999;

    public function flag(Request $request)
    {
        $user = $request->user();
        if ($user->coin < $this->price) {
            throw new Exception("no enough coin");
        }
        $user->coin -= $this->price;
        $user->save();
        return ['flag' => env('FLAG')];
    }
}
