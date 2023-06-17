<?php
	function fetch_row($table, $query, $operator=''){
		global $dbcon;
		$sql = 'SELECT * FROM '. $table;
		if($query){
			$sql .= ' WHERE ';
			foreach ($query as $key => $value) {
				$sql .= "{$key}='".clean_sql($value)."' {$operator} ";
			}	

			if($operator){
				$sql = trim(substr($sql, 0, strrpos($sql, $operator)));
	        }
	        else{
				$sql = trim($sql);
	        }

		}
		$result = mysqli_query($dbcon, $sql);
	    return mysqli_fetch_array($result, MYSQLI_ASSOC);
	}
    
    function fetch_multi_row($table, $query=array(), $operator='', $limit='', $orderby='', $condition=''){
    	global $dbcon;

        $sql = 'SELECT * FROM '. $table;
        if($condition){
            $sql .= ' WHERE '. $condition;
        }
        else if($query){
            $sql .=  ' WHERE ';
        
            foreach ($query as $key => $value) {
                $sql .= "{$key}='".clean_sql($value)."' {$operator} ";
            }
            if($operator){
                $sql = trim(substr($sql, 0, strrpos($sql, $operator)));
            }
            else{
                $sql = trim($sql);
            }
        }
        else{
            $sql .= ' WHERE 1 ';
        }
        if($orderby){
            $sql .= ' order by '.$orderby;
        }
        if($limit){
            $sql .= ' limit '. $limit;
        }            
        $result = mysqli_query($dbcon, $sql);
        if(!$result){
            exit(mysqli_error($dbcon));
        }
        $tmp = array();
        $i = 0;
        while($row = mysqli_fetch_array($result, MYSQLI_ASSOC)){
            $tmp[$i] = $row;
            $i++;
        }
        return $tmp;
    }
    function update($table, $replace, $query, $operator=''){
    	global $dbcon;

        $sql = 'UPDATE '.$table. ' SET ';

        foreach ($replace as $key => $value) {
            $sql .= "{$key}='".clean_sql($value)."',";
        }
        
        $sql = substr($sql, 0, strrpos($sql, ',')) . ' WHERE ';

        foreach ($query as $key => $value) {
            $sql .= "{$key}='".clean_sql($value)."' {$operator} ";
        }

        if($operator){
            $sql = trim(substr($sql, 0, strrpos($sql, $operator)));
        }
        else{
            $sql = trim($sql);
        }
        $result = mysqli_query($dbcon, $sql);
        return $result;
    }
	function insert($table, $query){
		global $dbcon;

		$sql = 'INSERT INTO ' . $table . ' ';

		$column = '';
		$data = '';
		foreach ($query as $key => $value) {
			$column .= '`' . $key . '`, ';
			$data .= "'".clean_sql($value)."', ";
		}

		$column = substr($column, 0, strrpos($column, ','));
		$data = substr($data, 0, strrpos($data, ','));

		$sql .= "({$column}) VALUES ({$data})";
		$result = mysqli_query($dbcon, $sql);
		
		return $result;
	}
	function delete($table, $query, $operator=''){
		global $dbcon;
		$sql = 'DELETE FROM '. $table;
		
		if($query){
			$sql .= ' WHERE ';
			foreach ($query as $key => $value) {
				$sql .= "{$key}='".clean_sql($value)."' {$operator} ";
			}	

			if($operator){
				$sql = trim(substr($sql, 0, strrpos($sql, $operator)));
	        }
	        else{
				$sql = trim($sql);
	        }

		}
		$result = mysqli_query($dbcon, $sql);
	    return $result;
	}
?>