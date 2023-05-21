<?php
include('Records.php');

class Albums {
    private $store;

    public function __construct($store) {
        $this->store = $store;
    }

    public function getAlbum($id) {
        return $this->store->getRecord($id);
    }

    public function addAlbum($album) {
        return $this->store->addRecord($album);
    }

    public function updateAlbum($id, $album) {
        return $this->store->updateRecord($id, $album);
    }

    public function deleteAlbum($id) {
        return $this->store->deleteRecord($id);
    }

    public function getAllAlbums() {
        return $this->store->getAllRecords();
    }

    public function __debugInfo() {
        return $this->getAllAlbums();
    }
}