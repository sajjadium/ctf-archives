<style type="text/css">
<?php
  $themes = array('light'=>['#111', '#eee'], 'dark'=>['#eee','#111']);

  if (!isset($_SESSION['theme'])) {
    $_SESSION['theme'] = 'light';
  }

  $theme = $_SESSION['theme'];
  if (!array_key_exists($theme, $themes)) {
    $theme = 'light';
  }

  echo 'body { color: ' . $themes[$theme][0] . '; background-color: ' . $themes[$theme][1] . '; }';
?>
</style>
