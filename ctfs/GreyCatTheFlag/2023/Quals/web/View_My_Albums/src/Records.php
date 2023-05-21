<?php

interface RecordStore
{
    public function getRecord($id);
    public function addRecord($record);
    public function updateRecord($id, $record);
    public function deleteRecord($id);
    public function getAllRecords();
}

class Record {
    private $data = array();

    public function __construct($id = null) {
        $this->data['id'] = $id;
    }

    public function __get($name) {
        if (array_key_exists($name, $this->data)) {
            return $this->data[$name];
        }
        return null;
    }

    public function __set($name, $value) {
        $this->data[$name] = $value;
    }

    public function getArray() {
        return $this->data;
    }
}

class MysqlRecordStore implements RecordStore
{
    private $mysqli;
    private $table;
    private $host;
    private $user;
    private $pass;
    private $db;

    public function __construct($host, $user, $pass, $db, $table) {
        $this->host = $host;
        $this->user = $user;
        $this->pass = $pass;
        $this->db = $db;
        $this->mysqli = new mysqli($host, $user, $pass, $db);
        $this->table = $table;
    }

    public function getRecord($id) {
        $stmt = $this->mysqli->prepare("SELECT * FROM {$this->table} WHERE id = ?");
        $stmt->bind_param('i', $id);
        $stmt->execute();
        $row = $stmt->get_result()->fetch_assoc();
        $record = new Record($id);
        foreach ($row as $key => $value) {
            $record->$key = $value;
        }
        return $record;
    }

    public function addRecord($record) {
        $keys = array();
        $values = array();
        foreach ($record->getArray() as $key => $value) {
            $keys[] = $key;
            $values[] = '?';
        }
        $keys = implode(',', $keys);
        $values = implode(',', $values);
        $stmt = $this->mysqli->prepare("INSERT INTO {$this->table} ($keys) VALUES ($values)");
        $stmt->bind_param(str_repeat('s', count($record->getArray())), ...$record->getArray());
        $stmt->execute();
        return $stmt->insert_id;
    }

    public function updateRecord($id, $record) {
        $updates = array();
        foreach ($record->getArray() as $key => $value) {
            $updates[] = "$key = ?";
        }
        $updates = implode(',', $updates);
        $stmt = $this->mysqli->prepare("UPDATE {$this->table} SET $updates WHERE id = ?");
        $stmt->bind_param(str_repeat('s', count($record->getArray())) . 'i', ...array_merge($record->getArray(), [$id]));
        $stmt->execute();
    }

    public function deleteRecord($id) {
        $stmt = $this->mysqli->prepare("DELETE FROM {$this->table} WHERE id = ?");
        $stmt->bind_param('i', $id);
        $stmt->execute();
    }

    public function getAllRecords() {
        $stmt = $this->mysqli->prepare("SELECT * FROM {$this->table}");
        $stmt->execute();
        $rows = $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
        $records = array();
        foreach ($rows as $row) {
            $record = new Record($row['id']);
            foreach ($row as $key => $value) {
                $record->$key = $value;
            }
            $records[] = $record;
        }
        return $records;
    }

    public function __destruct() {
        $this->mysqli->close();
    }

    public function __wakeup() {
        $this->mysqli = new mysqli($this->host, $this->user, $this->pass, $this->db);
    }
}

class JsonRecordStore implements RecordStore
{
    private $file;

    public function __construct($file) {
        $this->file = $file;
    }

    public function getRecord($id) {
        $data = json_decode(file_get_contents($this->file), true);
        $record = new Record($id);
        foreach ($data[$id] as $key => $value) {
            $record->$key = $value;
        }
        return $record;
    }

    public function addRecord($record) {
        $data = json_decode(file_get_contents($this->file), true);
        $data[] = $record->getArray();
        file_put_contents($this->file, json_encode($data));
        return count($data) - 1;
    }

    public function updateRecord($id, $record) {
        $data = json_decode(file_get_contents($this->file), true);
        $data[$id] = $record->getArray();
        file_put_contents($this->file, json_encode($data));
    }

    public function deleteRecord($id) {
        $data = json_decode(file_get_contents($this->file), true);
        unset($data[$id]);
        file_put_contents($this->file, json_encode($data));
    }

    public function getAllRecords() {
        $data = json_decode(file_get_contents($this->file), true);
        $records = array();
        foreach ($data as $id => $row) {
            $record = new Record($id);
            foreach ($row as $key => $value) {
                $record->$key = $value;
            }
            $records[] = $record;
        }
        return $records;
    }
}

class CsvRecordStore implements RecordStore
{
    private $file;

    public function __construct($file) {
        $this->file = $file;
    }

    public function getRecord($id) {
        $data = array_map('str_getcsv', file($this->file));
        $record = new Record($id);
        foreach ($data[$id] as $key => $value) {
            $record->$key = $value;
        }
        return $record;
    }

    public function addRecord($record) {
        $data = array_map('str_getcsv', file($this->file));
        $data[] = $record->getArray();
        $fp = fopen($this->file, 'w');
        foreach ($data as $fields) {
            fputcsv($fp, $fields);
        }
        fclose($fp);
        return count($data) - 1;
    }

    public function updateRecord($id, $record) {
        $data = array_map('str_getcsv', file($this->file));
        $data[$id] = $record->getArray();
        $fp = fopen($this->file, 'w');
        foreach ($data as $fields) {
            fputcsv($fp, $fields);
        }
        fclose($fp);
    }

    public function deleteRecord($id) {
        $data = array_map('str_getcsv', file($this->file));
        unset($data[$id]);
        $fp = fopen($this->file, 'w');
        foreach ($data as $fields) {
            fputcsv($fp, $fields);
        }
        fclose($fp);
    }

    public function getAllRecords() {
        $data = array_map('str_getcsv', file($this->file));
        $records = array();
        foreach ($data as $id => $row) {
            $record = new Record($id);
            foreach ($row as $key => $value) {
                $record->$key = $value;
            }
            $records[] = $record;
        }
        return $records;
    }
}

?>