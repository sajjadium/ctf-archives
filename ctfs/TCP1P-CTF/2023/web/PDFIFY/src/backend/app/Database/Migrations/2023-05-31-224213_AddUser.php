<?php

namespace App\Database\Migrations;

use CodeIgniter\Database\Migration;

class AddUser extends Migration
{
    public function up()
    {
        $this->forge->addField([
            'id' => [
                'type' => 'INT',
                'constraint' => 5,
                'unsigned' => true,
                'auto_increment' => true,
            ],
            'username' => [
                'type' => 'VARCHAR',
                'constraint' => 50,
                'unique' => true,
                'null' => false,
            ],
            'password' => [
                'type' => 'VARCHAR',
                'constraint' => 60,
                'null' => false,
            ],
            'email' => [
                'type' => 'VARCHAR',
                'constraint' => 50,
                'null' => false,
            ],
            'role' => [
                'type' => 'VARCHAR',
                'constraint' => 10,
                'null' => false,
            ]
        ]);
        $this->forge->addKey('id', true, true);
        $this->forge->createTable('users');
    }

    public function down()
    {
        $this->forge->dropTable('users');
    }
}
