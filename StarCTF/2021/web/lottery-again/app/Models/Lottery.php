<?php

namespace App\Models;

use Illuminate\Support\Str;
use Illuminate\Database\Eloquent\Model;

class Lottery extends Model
{
    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'coin',
    ];

    public static function boot()
    {
        parent::boot();

        self::creating(function ($user) {
            $user->uuid = Str::uuid();
        });
    }
}
