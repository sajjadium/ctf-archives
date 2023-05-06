<?php
namespace App\Controller;
use Symfony\Component\Filesystem\Path;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;

class UploadController extends AbstractController
{
    public function __construct()
    {
        mb_detect_order(["BASE64","ASCII","UTF-8"]);
        $this->ext_blacklist = [
            "php",
            "ini",
            "phtml",
            "htaccess",
        ];
        $this->content_blacklist = ["<?", "php", "handler"];
    }
    public function invalid($msg){
        return new Response("error occurs: $msg");
    }
    #[Route('/', name: 'upload')]
    public function index(Request $request)
    {
        $uploadHtml = <<<EOF
<html>
<form action="/" enctype="multipart/form-data" method="post">
  <input type="file" id="file" name="file">
  <input type="submit">
</form>
</html>
EOF;

        $file = @$_FILES["file"];
        if($file == null){
            return new Response(
                //'<p>Before start you should know that it\'s not a good challenge.You can\'t get anything from this challenge.If you hate this challenge, just skip plz. </p><p>这道题并不是一道好题，你不会从这道题上获得任何东西。如果你讨厌这道题就直接跳过吧。</p>'
                $uploadHtml
            );
        }else {

            $content = file_get_contents($file["tmp_name"]);
            $charset = mb_detect_encoding($content, null, true);
            if(false !== $charset){
                if($charset == "BASE64"){
                    $content = base64_decode($content);
                }
                foreach ($this->content_blacklist as $v) {
                    if(stristr($content, $v)!==false){
                        return $this->invalid("fucking $v .");
                    }
                }
            }else{
                return $this->invalid("fucking invalid format.");
            }
            $ext = Path::getExtension($file["name"], true);
            if(strstr($file["name"], "..")!==false){
                return $this->$this->invalid("fucking path travel");
            }
            foreach ($this->ext_blacklist as $v){
                if (strstr($ext, $v) !== false){
                    return $this->invalid("fucking $ext extension.");
                }
            }
            $dir = dirname($request->server->get('SCRIPT_FILENAME'));

            $result = move_uploaded_file($file["tmp_name"], "$dir/upload/".strtolower($file["name"]));
            if($result){
                return new Response("upload success");
            }else {
                return new Response("upload failed");
            }
        }
    }
}