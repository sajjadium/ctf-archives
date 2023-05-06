<?php

namespace App\Services\Auth;
 
use Illuminate\Http\Request;
use Illuminate\Contracts\Auth\Guard;
use Illuminate\Contracts\Auth\UserProvider;
use Illuminate\Contracts\Auth\Authenticatable;
use Illuminate\Auth\GuardHelpers;
use Illuminate\Support\Facades\Log;

class JwtGuard implements Guard
{
    use GuardHelpers;
    protected $request;
    protected $provider;
    protected $user;
  
    public function __construct(UserProvider $provider, Request $request, $hash = false)
    {
        $this->request = $request;
        $this->provider = $provider;
    }
    
    public function user()
    {
        if (! is_null($this->user)) {
            return $this->user;
        }

        $user = null;

        $token = $this->getTokenForRequest();
        

        if (!empty($token)) {
            $parts = explode('.', $token);
            $data = base64_decode(str_replace(['_', '-'], ['/', '+'], $parts[1]));
            $data = json_decode($data, true);

            $user = $this->provider->createModel();
            $user->id = $data['sub'];
            $user->name = $data['name'];
            $user->email = $data['email'];
            $user->avatar = $data['picture'];
        }

        return $this->user = $user;
    }
    
    public function getTokenForRequest()
    {
        $token = $this->request->bearerToken();

        return $token;
    }
    
    public function validate(array $credentials = [])
    {
        Log::info('validate '.$credentials);
        if ($this->user()) {
            return true;
        }

        return false;
    }

    public function setRequest(Request $request)
    {
        $this->request = $request;

        return $this;
    }
}
