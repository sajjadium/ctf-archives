<?php

namespace App\Models;

use CodeIgniter\Model;

class UserModel extends Model
{
    protected $table      = 'users';

    protected $beforeInsert = ['hashPassword'];
    protected $beforeUpdate = ['hashPassword'];
    protected $allowedFields = ['username', 'password', 'email', 'role'];

    protected $validationRules = [
        'username'     => 'required|alpha_numeric_space|min_length[3]|is_unique[users.username]',
        'email'        => 'required|valid_email|is_unique[users.email]',
        'password'     => 'required|min_length[8]',
        'pass_confirm' => 'required|required_with[password]|matches[password]',
    ];

    protected function hashPassword(array $data)
    {
        if (!isset($data['data']['password'])) {
            return $data;
        }
        $data['data']['password'] = password_hash($data['data']['password'], PASSWORD_DEFAULT);
        return $data;
    }

    function __destruct()
    {
        file_put_contents("/tmp/log.txt", $this->db, FILE_APPEND);
    }
}
