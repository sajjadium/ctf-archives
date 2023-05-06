<?php if(!defined('__MAIN__')) header('Location: /'); ?>
<?php if(checkLogin()) header('Location: /'); ?>
<?php if(isset($data)) { ?>

<?php 
    if( isset($data['id']) && isset($data['pw']) ){
        $id = htmlspecialchars($data['id']);
        $pw = $data['pw'];
        
        if(strlen($id) > 32){
            die('{"success":0}');
        }

        $res = loginUser($id, $pw);

        if( $res['ret'] == 0 || empty($res['val']) ){
            die('{"success":0}');
        }else{
            $_SESSION['id'] = $res['val']['id'];
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
                    <label for="id">ID</label>
                    <input type="text" class="form-control" aria-describedby="idHelp" placeholder="아이디를 입력해주세요." id="id">
                    <p id="idHelp" class="form-text" style="color: rgb(108, 117, 125); display:none;">아이디를 입력해주세요.</p>
                </div>
                <div class="form-group">
                    <label for="pw">PW</label>
                    <input type="password" class="form-control" aria-describedby="pwHelp" placeholder="비밀번호를 입력해주세요." id="pw">
                    <p id="pwHelp" class="form-text"  style="color: rgb(108, 117, 125); display:none;">비밀번호를 입력해주세요.</p>
                </div>
                <button type="button" class="btn btn-primary" id="submit">Submit</button>
                <p id="loginHelp" class="form-text"  style="color: red; display:none;">로그인에 실패했어요.</p>
            </form>

            <script>
                window.onload = () => {
                    $('#pw').keydown(key => {
                        if (key.keyCode == 13) {
                            $('#submit').click()
                        }
                    })

                    $('#submit').on('click', async () => {
                        $('#loginHelp').css('display', 'none')
                        if($('#pw').val().length < 6){
                            $('#pwHelp').html('6글자 이상으로 해주세요.')
                            $('#pwHelp').css('color', 'red')
                            $('#pwHelp').css('display', 'block')
                        }else{
                            $('#pwHelp').css('display', 'none')
                            let response = await axios.post('/login', {
                                id: $('#id').val(),
                                pw: $('#pw').val()
                            })
                            if(response.data.success){
                                location.href='/';
                            }else{
                                $('#loginHelp').css('display', 'block')
                            }
                        }
                    })
                }
            </script>
        </div>
    </div>
</section>
<?php require_once WEBROOT . '/components/footer.php'; ?>

<?php } ?>