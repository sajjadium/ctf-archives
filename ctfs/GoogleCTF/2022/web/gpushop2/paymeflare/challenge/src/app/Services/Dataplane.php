<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;


class Dataplane {
    
    public static function http_dataplane() {
        return Http::withOptions(['curl' => 
            [CURLOPT_UNIX_SOCKET_PATH => config('app.dataplane_socket')]
        ])->withBasicAuth('admin', config('app.dataplane_passwd'));
    }

    public static function get_version() {
        $http = self::http_dataplane();
        $res = $http->get('http://localhost/v2/services/haproxy/configuration/version');
        return $res->json();
    }

    public static function delete_backend($host, $txid='') {
        $http = self::http_dataplane();

        $url = "http://localhost/v2/services/haproxy/configuration/backends/${host}?";
        
        if ($txid)
            $url .= "transaction_id=".$txid;
        else
            $url .= "version=".self::get_version();
            
        $res = $http->delete($url);
        
        if ($res->failed()) {
            Log::error($res->body());
        }
    }

    public static function add_backend($host, $ip, $txid='') {
        $http = self::http_dataplane();

        $port = 80;
        if (strpos($ip, ':') !== false) {
            list($ip, $port) = explode(':', $ip);
            $port = intval($port);
        }
        
        $append = "transaction_id=".$txid;
        
        if (!$txid)
            $append = "version=".self::get_version();
        
        $res = $http->post('http://dataplane/v2/services/haproxy/configuration/backends?'.$append, [
            'name' => $host,
            'balance' => [
                'algorithm' => 'roundrobin',
            ]
        ]);
        
        if ($res->failed()) {
            Log::error($res->body());
            return false;
        }
        
        if (!$txid)
            $append = "version=".self::get_version();    
        
        $res = $http->post("http://dataplane/v2/services/haproxy/configuration/servers?backend=${host}&".$append, [
            'address' => $ip,
            'name' => 'www',
            'port' => $port,      
        ]);    
        
        if ($res->failed()) {
            Log::error($res->body());
            return false;
        }
        
        return true;
    }

    public static function update_backend($old_backend, $host, $ip) {
        $http = self::http_dataplane();
        
        $txid = $http->post('http://dataplane/v2/services/haproxy/transactions?version='.self::get_version())['id'];
        
        if ($old_backend) {
            self::delete_backend($old_backend, $txid);
        }
        
        if (!self::add_backend($host, $ip, $txid))
            return false;
        
        $res = $http->put("http://dataplane/v2/services/haproxy/transactions/${txid}");
        
        if ($res->failed()) {
            Log::error($res->body());
            return false;
        }
        
        return true;    
    }
    
}
