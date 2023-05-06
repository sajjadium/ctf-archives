<?php if(!defined('__MAIN__')) header('Location: /'); ?>
<?php if(!checkLogin()) header('Location: /'); ?>


<?php 
  if(isset($_GET['text'])){
    $text = $_GET['text'];
    $id = $_SESSION['id'];

    $posts = searchPosts('%'.$text.'%', $id)['all'];
  }
?>

<?php require_once WEBROOT . '/components/header.php'; ?>
<?php require_once WEBROOT . '/components/navbar.php'; ?>

<section>
    <div class="py-3">
        <div class="container">       
          <p>Search result: <?= $text ?> </p>
          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Title</th>
                <th scope="col">Content</th>
                <th scope="col">Writer</th>
                <th scope="col">Views</th>
              </tr>
            </thead>
            <tbody>
              <?php 
                foreach($posts as $post) {
                  echo '<tr onclick=location.href="/read?no='.$post['no'].'">';
                  echo '<th scope="row">'.$post['no'].'</th>';
                  echo '<td>'.$post['title'].'</td>';
                  echo '<td>'.substr($post['content'],0,4).'..</td>';
                  echo '<td>'.$post['writer'].'</td>';
                  echo '<td>'.$post['views'].'</td>';
                  echo '</tr>';
                }
              ?>
            </tbody>
          </table>
        </div>
    </div>
</section>
<?php require_once WEBROOT . '/components/footer.php'; ?>
