<?php

  mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

  function search() {
    $ret = [];

    if (!isset($_GET["q"])) {
      return $ret;
    }

    $db = new mysqli("p:mysql", "app", "07b05ee6779745b258ef8dde529940012b72ba3a007c7d40a83f83f0938b5bf0", "analects");

    $query = addslashes($_GET["q"]);
    $sql = "SELECT * FROM analects WHERE chinese LIKE '%{$query}%' OR english LIKE '%{$query}%'";
    $result = $db->query($sql);

    while ($row = $result->fetch_assoc()) {
      $row["chinese"] = mb_convert_encoding($row["chinese"], "UTF-8", "GB18030");
      $row["english"] = mb_convert_encoding($row["english"], "UTF-8", "GB18030");
      array_push($ret, $row);
    }
    $result->free_result();

    return $ret;
  }

  header('Content-Type: application/json; charset=UTF-8');
  echo json_encode(search());
?>
