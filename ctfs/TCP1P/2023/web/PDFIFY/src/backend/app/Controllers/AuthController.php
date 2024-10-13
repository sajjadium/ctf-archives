<?php

namespace App\Controllers;

use CodeIgniter\API\ResponseTrait;
use App\Models\UserModel;

class AuthController extends BaseController
{
    use ResponseTrait;
    protected $model;
    protected $session;
    public function __construct()
    {
        $this->model = model(UserModel::class);
        $this->session = \Config\Services::session();
    }

    public function login()
    {
        $data = $this->request->getPost();
        if (!isset($data['username']) || !isset($data['password'])) {
            return $this->fail("username or password not set");
        }
        $password = $data['password'];
        unset($data['password']);

        $user = $this->model->where($data)->first();
        if (!$user) {
            return $this->fail("username not found!");
        }

        if (!password_verify($password, $user['password'])) {
            return $this->fail("incorrect password!");
        }

        $this->session->set("username", $user['username']);
        $this->session->set("role", $user['role']);
        return $this->respond([
            "message" => "successful log in as user " . $user['username']
        ]);
    }

    public function register()
    {
        $data = $this->request->getPost();
        if (!$this->model->validate($data)) {
            return $this->failValidationErrors($this->model->errors());
        }
        $data['role'] = 'user';
        $this->model->save($data);
        $this->session->set("username", $data['username']);
        $this->session->set("role", $data['role']);
        return $this->respond([
            "message" => "User " . $data['username'] . " created successfully",
        ]);
    }

}
