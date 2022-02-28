<?php if(!defined('__MAIN__')) header('Location: /'); ?>
<?php if(!checkLogin()) header('Location: /'); ?>

<?php if(isset($data)) { ?>

<?php 
    if( isset($data['title']) && isset($data['content']) ){
        $title = htmlspecialchars($data['title']);
        $content = $data['content'];
       
        if (strpos($content, '<') !== false) $result = filterHtml($content);
        else $result = $content;

        $res = insertPost($title, $result, $_SESSION['id']);
        if( $res == 0 ){
            die('{"success":0}');
        }else{
            die('{"success":1}');
        }
    }else{
        die('{"success":0}');
    }
    
?>

<?php } else { ?>

<?php require_once WEBROOT . '/components/header.php'; ?>
<?php require_once WEBROOT . '/components/navbar.php'; ?>

<section>
    <div class="py-3">
        <div class="container">       
            <form>
                <div class="form-group">
                    <label for="id">Title</label>
                    <input type="text" class="form-control" aria-describedby="idHelp" placeholder="제목을 입력해주세요." id="title">
                    <p id="titleHelp" class="form-text" style="color: rgb(108, 117, 125); display:none;">제목 입력해주세요.</p>
                </div>
                <div class="form-group">
                    <label for="pw">Content</label>
                    <textarea class="form-control" id="content" id="exampleFormControlTextarea1" rows="5" placeholder="내용을 입력해주세요"></textarea>
                </div>
                <button type="button" class="btn btn-primary" id="submit">Write</button>
                <p id="writeHelp" class="form-text"  style="color: red; display:none;">글쓰기에 실패했어요.</p>
            </form>

            <script>
              window.onload = () => {
                $('#submit').on('click', async () => {
                  $('#titleHelp').css('display', 'none')
                  $('#writeHelp').css('display', 'none')
                  let response = await axios.post('/write', {
                    title: $('#title').val(),
                    content: $('#content').val()
                  })
                  if(response.data.success){
                    location.href='/';
                  }else{
                    $('#loginHelp').css('display', 'block')
                  }
                })
              }
            </script>
        </div>
    </div>
</section>
<?php require_once WEBROOT . '/components/footer.php'; ?>

<?php } ?>
