<?php


require_once "framework/HTTP.module";
require_once "framework/Typed.module";
require_once "framework/CSP.module";
error_reporting(0);


// Model
class CatData extends \ShouFramework\Typed {
    public $hash_string;
    public $time_integer;
    public $content_string;

    protected function construct(){}

    protected function destruct(){}
}

class UserData extends \ShouFramework\Typed {
    public $token_string;

    protected function construct() {
        if (isset($_GET["user"])) {
            $user = unserialize($_GET["user"]);
            if (get_class($user) != "UserData") \ShouFramework\shutdown();
            $this->token_string = $user->token_string;
        }
        // unauthenticated request
        $this->token_string = uniqid("", true);
        return $this;
    }
    protected function destruct(){}
}

// Controllers
class CatGet extends \ShouFramework\HTTP{
    public function render(){
        $this->template_object->render_html("
<h1>Cat Hub</h1>
<form action='/?method=post' method='post'>
    Upload your cat porn articles!
    <br>
    <textarea name='content'></textarea>
    <input type='submit'>
</form>
        ");
    }
}

class CatPost extends \ShouFramework\HTTP{
    public UserData $user_object;

    public function construct() {
        parent::construct();
        $this->user_object = new UserData();
    }

    public function handle(){
        $content = $_POST["content"];
        $time = time();
        $hash = sha1($this->user_object->token_string . $content . "$time");
        $hashhash = sha1($hash);
        $cat_post = new CatData();
        $cat_post->hash_string = $hash;
        $cat_post->time_integer = $time;
        $cat_post->content_string = $content;
        $cat_dump = fopen("tmp/$hashhash", "w+");
        fwrite($cat_dump, serialize($cat_post));
        fclose($cat_dump);
        $this->template_object->render_html("
<h1>Cat Hub</h1>
Your post is saved at: <a href='/?method=show&hash=$hash'>/?method=show&hash=$hash</a>
        ");
    }
    public function render(){}
}

class CatWithHashGet extends \ShouFramework\HTTP{
    public UserData $user_object;
    public \ShouFramework\CSP $csp_object;

    public function construct() {
        parent::construct();
        $this->user_object = new UserData();
        $this->csp_object = new \ShouFramework\CSP();
    }

    public function render() {
        $hash = $_GET["hash"];
        $hashhash = sha1($_GET["hash"]);
        $filename = "tmp/$hashhash";
        if (!file_exists($filename)) {
            $this->template_object->render_html("Not found");
            return;
        }
        $cat_dump = fopen($filename, "r");
        $cat_info = unserialize(fread($cat_dump,filesize($filename)));
        $nonce = $this->csp_object->generate_nonce();
        $this->csp_object->add_csp([$nonce]);
        $this->template_object->render_html("<head></head>");
        $this->template_object->render_script("
function add_js(filename, nonce) {
  var head = document.head;
  var script = document.createElement('script');
  script.nonce = nonce;
  script.src = filename;
  head.appendChild(script);
}
window.onhashchange = () => {let query = window.location.hash.substr(1).split('@'); add_js(query[0], query[1])};
        ", $nonce);
        $this->template_object->render_html("
<h1>Cat Hub</h1>
<p id='time'></p>
<p>$cat_info->content_string</p>
<p>Permalink: <a>/?method=show&hash=$hash</a></p>

<a href='#black.js@$nonce'>Black Background</a>
<a href='#white.js@$nonce'>White Background</a>
        ");
        $this->template_object->render_script("
time.innerText = new Date($cat_info->time_integer)
        ", $nonce);
    }
}

$resp = match ($_GET["method"]) {
    "post" => new CatPost(),
    "show" => new CatWithHashGet(),
    default => new CatGet(),
};
