<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Config;
use App\Services\Dataplane;


class ProdDatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     *
     * @return void
     */
    public function run()
    {
        Config::create([
            'id' => '111111111111111111111',
            'host' => config('app.gpushop_host'),
            'ip' => config('app.gpushop_ip'),
        ]);
        
       Dataplane::add_backend(config('app.gpushop_host'), config('app.gpushop_ip'));
    }
}
