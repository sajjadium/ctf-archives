<?php
/**
 * GuestFS is a simple file server.
 *
 *  - Every user has a root directory (user-space)
 *  - Users can put files in their user-space
 */
class GuestFS {
    function __construct($root)
    {
        if (!is_dir($root)) {
            mkdir($root, 0755);
        }
        $this->root = $root;
    }

    /**
     * Create a new file
     *
     * @param string $name Filename to create
     * @param int $type File type (0:normal/1:symlink)
     * @param string $link Path to the real file (when $type=1)
     */
    function create($name, $type=0, $target="")
    {
        $this->validate_filename($name);

        if ($type === 0) {

            /* Create an empty file */
            $fp = @fopen($this->root.$name, "w");
            @fwrite($fp, '');
            @fclose($fp);

        } else {

            /* Target file must exist */
            $this->assert_file_exists($this->root.$target);

            /* Create a symbolic link */
            @symlink($target, $this->root.$name);

            /* This check ensures $target points to inside user-space */
            try {
                $this->validate_filepath(@readlink($this->root.$name));
            } catch(Exception $e) {
                /* Revert changes */
                @unlink($this->root.$name);
                throw $e;
            }

        }
    }

    /**
     * Read a file
     *
     * @param string $name Filename to read
     * @param int $offset Offset to read
     */
    function read($name, $size=-1, $offset=0)
    {
        /* Check filename, size and offset */
        $this->validate_filename($name);
        $this->assert_file_exists($this->root.$name);
        $size = $this->validate_bounds($this->root.$name, $size, $offset);

        /* This may alleviate heavy disk load. */
        usleep(500000);

        /* Read contents */
        $fp = @fopen($this->root.$name, "r");
        @fseek($fp, $offset, SEEK_SET);
        $buf = @fread($fp, $size);
        @fclose($fp);

        return $buf;
    }

    /**
     * Write to a file
     *
     * @param string $name Filename to write
     * @param string $data Contents to write
     * @param int $offset Offset to write
     */
    function write($name, $data, $offset=0)
    {
        /* We don't call validate_bounds to allow appending data */
        $this->validate_filename($name);
        $this->assert_file_exists($this->root.$name);

        /* This may alleviate heavy disk load. */
        usleep(500000);

        /* Write contents */
        $fp = @fopen($this->root.$name, "w");
        @fseek($fp, $offset, SEEK_SET);
        @fwrite($fp, $data);
        @fclose($fp);
    }

    /**
     * Delete a file
     *
     * @param string $name Filename to delete
     */
    function delete($name)
    {
        $this->validate_filename($name);
        $this->assert_file_exists($this->root.$name);

        @unlink($this->root.$name);        
    }

    /**
     * List files in the user space
     */
    function listup()
    {
        $result = array();

        $list = array_diff(scandir($this->root), array('..', '.'));
        foreach($list as $key => $value) {
            if (is_link($this->root.$value)) {
                $result[$value] = "Symlink to ".@readlink($this->root.$value);
            } else {
                $result[$value] = "Regular file";
            }
        }

        return $result;
    }

    /* Security Functions */
    function validate_filepath($path)
    {
        if (strpos($path, "/") === 0) {
            throw new Exception('invalid filepath (absolute path)');
        } else if (strpos($path, "..") !== false) {
            throw new Exception('invalid filepath (outside user-space)');
        }
    }

    function validate_filename($name)
    {
        if (preg_match('/[^a-z0-9]/i', $name)) {
            throw new Exception('invalid filename');
        }
    }

    function assert_file_exists($name)
    {
        if (file_exists($name) === false
            && is_link($name) === false) {
            throw new Exception('file not found');
        }
    }

    function validate_bounds($path, $size, $offset)
    {
        $st = @stat($path);
        if ($offset < 0) {
            throw new Exception('offset must be positive');
        }
        if ($size < 0) {
            $size = $st['size'] - $offset;
            if ($size < 0) {
                throw new Exception('offset is larger than file size');
            }
        }
        if ($size + $offset > $st['size']) {
            throw new Exception('trying to read out of bound');
        }
        return $size;
    }
}
?>
