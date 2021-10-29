<?php
include_once("functions.php");
include_once("config.php");

$_SESSION['CSRFToken'] = md5(random_bytes(32));
if (!isset($_SESSION['is_auth']) or !$_SESSION['is_auth']){
    redirect('login.php');
    die();
}
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Diamond Safe</title>
        <meta charset="utf-8">
        <script src="<?= $static_dir ?>jquery-3.2.1.min.js"></script>
        <script src="<?= $static_dir ?>bootstrap.min.js"></script>
        <link rel="stylesheet" href="<?= $static_dir ?>bootstrap.min.css">
        <link rel="stylesheet" href="<?= $static_dir ?>main.css">
        <link rel="icon" type="image/png" href="<?= $static_dir ?>favicon.png">
    </head>
    <body>
        <script>
            var csrf_token = "<?= $_SESSION['CSRFToken'] ?>";
        </script>
        <div class="container">
            <br>
            <nav class="navbar navbar-default navbar">
                <div class="container-fluid">
                    <div class="navbar-header">
                        <a class="navbar-brand">Diamond Safe</a>
                    </div>
                    <ul class="nav navbar-nav">
                        <li><a href="<?= $base_dir ?>index.php">About</a></li>
                        <li class="active"><a href="<?= $base_dir ?>vault.php">My Vault</a></li>
                        <li><a href="<?= $base_dir ?>logout.php">Logout</a></li>
                    </ul>
                </div>
            </nav>
        </div>
        <div class="container container-body">
            <div class="panel panel-default">
                <div class="panel-heading">
                    Vault - <?= ms($_SESSION['user']);?>
                </div>
                <div class="panel-body">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Password</th>
                                <th>Email</th>
                            </tr>
                        </thead>
                        <tbody>
                            
                            <?php
                            $query = "SELECT id,name,email FROM vault";
                            $result = db::commit($query);
                            if ($result->num_rows > 0) {
                                while ($row = $result->fetch_row()) {
                                    ?><tr>
                                        <td><div onclick="vault_delete('<?=ms($row[0]);?>')" style='cursor:pointer'><?=ms($row[0]);?></div></td>
                                        <td><?=ms($row[1]);?></td>
                                        <td><div onclick="vault_show('<?=ms($row[0]);?>')" id='id_<?=ms($row[0]);?>' style='cursor:pointer'>***********</div></td>
                                        <td><?=ms($row[2]);?></td>
                                    </tr>
                                    <?php
                                }
                            }
                            ?><tr>
                                <td></td>
                                <td><input class="input-sm form-control" name="data[name]" id="name" placeholder="Enter name"></td>
                                <td><input class="input-sm form-control" type="password" name="data[password]" id="password" placeholder="Enter password"></td>
                                <td><input class="input-sm form-control" name="data[email]" id="email" placeholder="Enter email"></td>
                            </tr>
                        </tbody>
                        </table>
                        <button type="submit" class="btn btn-default" onclick="vault_add()">Submit</button>
                </div>
            </div>
            <div class="panel panel-default">
                <div class="panel-heading">
                    Active Sessions - <a data-toggle="collapse" href="#session">show</a>
                </div>
                <div id="session" class="panel-collapse collapse">
                    <div class="panel-body">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th><center>Id</center></th>
                                    <th><center>User-Agent</center></th>
                                    <th><center>IP</center></th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><center>1</center></td>
                                    <td><center><?= ms($_SESSION['user_agent']); ?></center></td>
                                    <td><center><?= ms($_SESSION['ip']); ?></center></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        
            <div class="panel panel-default">
                    <div class="panel-heading">
                        Secure Files - <a data-toggle="collapse" href="#securefiles">show</a>
                    </div>
                    <div id="securefiles" class="panel-collapse collapse">
                        <div class="panel-body">
                            <ul>
                            <?php 
                                    $dir = '/var/www/files';
                                    $scanned_dir = array_diff(scandir($dir), array('..', '.'));

                                    foreach ($scanned_dir as $key => $file_name){?>
                                        
                                        <li><a href="<?= gen_secure_url($file_name)?>"><?= ms($file_name)?></a></li>

                                    <?php  }  ?>        

                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    <?php print_footer(); ?>

    <?php echo '<script src="'.$static_dir.'api.js"></script>';?>

    </body>
</html>