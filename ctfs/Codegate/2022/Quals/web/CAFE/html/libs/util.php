<?php
  define('WEBROOT', '/var/www/html');
    
  function hashing($data) {
    return hash('sha256', 'DIFFERENT_ON_SERVER__________'.$data.'_________123!@#');
  }

  function insertUser($id, $pw) {
    $res = query('insert into users value(:id, :pw, now());', [
      ':id' => $id,
      ':pw' => hashing($pw),
    ]);
    return $res['ret'];
  }

  function loginUser($id, $pw) {
    $res = query('select id from users where id=:id and pw=:pw;', [
      ':id' => $id,
      ':pw' => hashing($pw)
    ]);
    return $res;
  }

  function checkLogin() {
    return isset($_SESSION['id']);
  }

  function getPosts($id) {
    $res = query_all('select * from posts where writer=:id', [
      ':id' => $id
    ]);
    return $res;
  }

  function getPost($no) {
    $res = query('select * from posts where no=:no', [
      ':no' => $no
    ]);
    return $res;
  }

  function updateViews($no) {
    $res = query('update posts set views=views+1 where no=:no', [
      ':no' => $no
    ]);
    return $res;
  }

  function searchPosts($text, $id) {
    $res = query_all('select * from posts where writer=:id and content like :text', [
      ':id' => $id,
      ':text' => $text
    ]);
    return $res;
  }

  function insertPost($title, $content, $id) {
    $res = query('insert into posts value(0, :title, :content, :writer, 0);', [
      ':title' => $title,
      ':content' => $content,
      ':writer' => $id
    ]);
    return $res['ret'];
  }


  function filterHtml($content) {
    $result = '';

    $html = new simple_html_dom();
    $html->load($content);
    $allowTag = ['a', 'img', 'p', 'span', 'br', 'hr', 'b', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'code', 'iframe'];

    foreach($allowTag as $tag){
      foreach($html->find($tag) as $element) {
        switch ($tag) {
          case 'a':
            $result .= '<a href="' . str_replace('"', '', $element->href) . '">' . htmlspecialchars($element->innertext) . '</a>';
            break;
          case 'img':
            $result .= '<img src="' . str_replace('"', '', $element->src) . '">' . '</img>';
            break;
          case 'p':
          case 'span':
          case 'b':
          case 'h1':
          case 'h2':
          case 'h3':
          case 'h4':
          case 'h5':
          case 'h6':
          case 'strong':
          case 'em':
          case 'code':
            $result .= '<' . $tag . '>' . htmlspecialchars($element->innertext) . '</' . $tag . '>';
            break;
          case 'iframe':
            $src = $element->src;
            $host = parse_url($src)['host'];
            if (strpos($host, 'youtube.com') !== false){
              $result .= '<iframe src="'. str_replace('"', '', $src) .'"></iframe>';
            }
            break;
        }
      }
    }
    return $result;
  }

  function report($no) {
    system("/run.sh ${no} > /dev/null");
  }
?>