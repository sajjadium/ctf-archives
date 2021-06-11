<?php

namespace App\Http\Controllers;

use App\Models\User;
use App\Models\Lottery;
use Illuminate\Http\Request;
use App\Exceptions\Exception;
use Laravel\Lumen\Routing\Controller as BaseController;

class LotteryController extends BaseController
{
    protected $price = 100;

    public function buy(Request $request)
    {
        $user = $request->user();
        if ($user->coin < $this->price) {
            throw new Exception("no enough coin");
        }

        $cnt = User::where('id', $user->id)->where('coin', $user->coin)
            ->decrement('coin', $this->price);
        if ($cnt === 0) {
            throw new Exception("unknown error");
        }

        $lottery = Lottery::create(['coin' => 100 - floor(sqrt(random_int(1, 10000)))]);
        $serilized = json_encode([
            'lottery' => $lottery->uuid,
            'user' => $user->uuid,
            'coin' => $lottery->coin,
        ]);
        $enc = base64_encode(mcrypt_encrypt(MCRYPT_RIJNDAEL_256, env('LOTTERY_KEY'), $serilized, MCRYPT_MODE_ECB));
        return [
            'enc' => $enc,
            // 'serialized' => $serilized,
        ];
    }

    public function info(Request $request)
    {
        return [
            'info' => $this->decrypt($request->input('enc')),
        ];
    }

    public function charge(Request $request)
    {
        $info = $this->decrypt($request->input('enc'));
        $lottery = Lottery::where('uuid', $info->lottery)->first();
        if (empty($lottery) || $lottery->used) {
            throw new Exception('invalid lottery');
        }
        if ($info->user !== $request->input('user')) {
            throw new Exception('invalid user');
        }
        $user = User::where('uuid', $info->user)->first();
        if (empty($user)) {
            throw new Exception('invalid user');
        }

        $cnt = Lottery::where('id', $lottery->id)->where('used', false)
            ->update(['used' => 1]);
        if ($cnt === 0) {
            throw new Exception('unknown error');
        }

        $user->coin += $lottery->coin;
        $user->save();

        return [
            // 'user' => $user,
            // 'lottery' => $lottery,
        ];
    }

    private function decrypt($enc)
    {
        $serilized = trim(mcrypt_decrypt(MCRYPT_RIJNDAEL_256, env('LOTTERY_KEY'), base64_decode($enc), MCRYPT_MODE_ECB));
        $info = json_decode($serilized);
        if (empty($info)) {
            throw new Exception('invalid lottery');
        }
        return $info;
    }
}
