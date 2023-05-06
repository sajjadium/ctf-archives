<?php
        $secret = "*REDACTED*";
        $flag   = "3k{*REDACTED*}";

        function fetch_and_parse($page){
                $a=file_get_contents("https://raw.githubusercontent.com/3kctf2021webchallenge/downloader/master/".$page.".html");
                preg_match_all("/<img src=\"(.*?)\">/", $a,$ma);
                return $ma;
        }

        $url = @$_GET['url'];
        $key = @$_GET['key'];
        $dir = @$_GET['dir'];
        if($dir){
                $emojiList = fetch_and_parse($dir);
        }elseif ($url AND $key) {
                if($key === hash_hmac('sha256', $url, $secret)){
                        $d = "bash -c \"curl -o /dev/null ".escapeshellarg("https://raw.githubusercontent.com/3kctf2021webchallenge/downloader/master/".$url)."  \"";
                        exec($d);
                        echo '<script>alert("file download requested");</script>';      
                }else{
                        echo '<script>alert("incorrect download key");</script>';
                }

        }


?>
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>Emoji</title>
  </head>
  <body>
    <h1>Emoji</h1>

    <div class="card-deck">
	  <div class="card">
	    
	    <div class="card-body">
	      <h5 class="card-title"><a href="?dir=eggs">Eggs</a> <a href="?dir=parrot">Parrots</a> <a href="?dir=pepe">Pepe</a></h5>
	      
	      <p class="card-text">
	      	<?php
	      		if(@$emojiList){
	      			foreach ($emojiList[1] as $k => $v) {
	      				echo '<a href="?url='.$v.'&key='.hash_hmac('sha256', $v, $secret).'"><img width=100 src="https://raw.githubusercontent.com/3kctf2021webchallenge/downloader/master/'.$v.'" ></a>';
	      			}
	      		}
	      	?>
	      </p>
	      
	    </div>
	  </div>
	</div>

  </body>
</html>