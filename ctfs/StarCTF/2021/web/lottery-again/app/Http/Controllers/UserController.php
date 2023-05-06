<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Support\Str;
use Illuminate\Http\Request;
use App\Exceptions\Exception;
use Laravel\Lumen\Routing\Controller as BaseController;

class UserController extends BaseController
{
    public function register(Request $request)
    {
        if (User::where('username', $request->input('username'))->first()) {
            throw new Exception('duplicate username');
        }
        return [
            'user' => User::create($request->input()),
        ];
    }

    public function login(Request $request)
    {
        $user = User::where('username', $request->input('username'))
            ->where('password', $request->input('password'))->first();
        $user->api_token = Str::random(32);
        $user->save();
        return [
            'user' => $user,
        ];
    }

    public function info(Request $request)
    {
        return [
            'user' => $request->user(),
        ];
    }
}
