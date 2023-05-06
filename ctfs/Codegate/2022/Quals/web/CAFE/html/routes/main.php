<?php if(!defined('__MAIN__')) header('Location: /'); ?>
<?php require_once WEBROOT . '/components/header.php'; ?>
<?php require_once WEBROOT . '/components/navbar.php'; ?>

<section>
  <div class="py-3">
    <div class="container">     
      <div class="form-group">
        
       
      </div>
      <?php if(checkLogin()) { ?> 
        <div class="input-group mb-3">
           <input type="text" class="form-control" aria-describedby="idHelp" placeholder="search" id="search">
          <div class="input-group-append">
            <button class="btn btn-outline-secondary" type="button" id="searchBtn">Search</button>
          </div>
        </div>
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
              $id = $_SESSION['id'];
              $posts = getPosts($id)['all'];
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
      <?php } ?>
      <script>
        window.onload = () => {
          $('#searchBtn').on('click', async () => {
            location.href = '/search?text=' + $('#search').val()
          })  
        }
      </script>
    </div>
  </div>
</section>



<?php require_once WEBROOT . '/components/footer.php'; ?>
