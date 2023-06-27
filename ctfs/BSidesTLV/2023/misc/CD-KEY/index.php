<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Product Identification</title>
    <link rel="stylesheet" href="//unpkg.com/xp.css" />
    <link href="//cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">

    <style>

        body{
            background-image: url("//artsy-media-uploads.s3.amazonaws.com/2RNK1P0BYVrSCZEy_Sd1Ew%2F3417757448_4a6bdf36ce_o.jpg");
            background-repeat: no-repeat;
            background-size: cover;
            height: 100vh;
            overflow: hidden;
        }
        .window{
            width: 50%;
            margin: 0 auto;
        }
        .window-body{
            margin: 0;
        }

        .key{
            width: 100%;
        }
        input[type=submit],input[type=button]{
            font-size: 15px;
            margin-top: 5px;
            border-radius: 0;
        }

        .card{
            border-radius: 0;
            border: 0;
        }
        .card-body{
            background-color: lightgrey;
        }
        .card-header{
            border-radius: 0px !important;
            background-color: steelblue;

        }
        .wrapper{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .buttons{
            margin-bottom: 15px;
            margin-top: 15px;
        }
        .error{
            border: 1px solid red !important;
        }

    </style>
</head>

<body>
<?php


$isValid = false;
$isSubmitted = false;
$flag = getenv('FLAG') ?? "BSidesTLV2023{This_Is_Not_The_Flag}";
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $isSubmitted = true;
    $isValid = validate_key($_POST["key"]);
}
?>

<div class="wrapper">
    <div class="window">
        <div class="title-bar">
            <div class="title-bar-text">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-key" viewBox="0 0 16 16">
                    <path d="M0 8a4 4 0 0 1 7.465-2H14a.5.5 0 0 1 .354.146l1.5 1.5a.5.5 0 0 1 0 .708l-1.5 1.5a.5.5 0 0 1-.708 0L13 9.207l-.646.647a.5.5 0 0 1-.708 0L11 9.207l-.646.647a.5.5 0 0 1-.708 0L9 9.207l-.646.647A.5.5 0 0 1 8 10h-.535A4 4 0 0 1 0 8zm4-3a3 3 0 1 0 2.712 4.285A.5.5 0 0 1 7.163 9h.63l.853-.854a.5.5 0 0 1 .708 0l.646.647.646-.647a.5.5 0 0 1 .708 0l.646.647.646-.647a.5.5 0 0 1 .708 0l.646.647.793-.793-1-1h-6.63a.5.5 0 0 1-.451-.285A3 3 0 0 0 4 5z"/>
                    <path d="M4 8a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
                </svg>
                Software License Activation
            </div>
            <div class="title-bar-controls">
                <button aria-label="Minimize"></button>
                <button aria-label="Maximize"></button>
                <button aria-label="Close"></button>
            </div>
        </div>
        <div class="window-body">

            <div class="card">
                <div class="card-header">
                    Your trial is expired
                </div>
                <div class="card-body">
                    <h5 class="card-title">Product key</h5>
                    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
                        <input class="key <?php if(!$isValid && $isSubmitted){ echo 'error';}?>" type="text" name="key" placeholder="XXXXXXXXXXXXXXXXXX">

                        <div class="d-flex buttons">
                            <div class="d-flex justify-content-start">
                                <input type="button" class="btn btn-success btn-lg" value="Buy Now"></input>
                            </div>
                            <div class="d-flex" style="margin-left: auto;" >
                                <input type="submit" class="btn btn-success btn-lg" name="submit" value="Activate">
                                <input type="button" class="btn btn-success btn-lg"  value="Cancel" style="margin-left: 5px;">
                            </div>

                        </div>
                        <span>For more information visit </span> <a href="#" class="card-link">www.owasp.com</a>
                        <div>
                            <?php if($isValid) {
                                echo $flag;
                            }
                            ?>

                        </div>
                    </form>

                </div>
            </div>

        </div>
    </div>

</div>

<?php
function validate_key($Nd2Ei) : bool { goto EHUvl; EHUvl: $RswYn = "\57\136\133\60\x2d\71\135\x7b\65\x7d\x2d\x5b\x41\x2d\132\141\x2d\x7a\x5d\x7b\63\x7d\55\133\60\x2d\x39\135\173\67\x7d\55\x5b\60\x2d\x39\135\173\65\175\x24\x2f\151"; goto Jqlvn; IiZFB: return $iemVT % 7 == 0; goto To7Hm; tI8cc: $Nd2Ei = htmlspecialchars($Nd2Ei); goto LQHHH; aZ2HL: $iemVT = 0; goto Jsi21; Y1JYP: if (is_numeric($Nd2Ei[$mM5aW + 18])) { goto BcHCu; } goto lIceC; va6be: eHqaj: goto c9E41; Q6G_X: if (in_array(substr($Nd2Ei, 3, 2), [$MN1tG[52] . $MN1tG[52], $MN1tG[52] . $MN1tG[53], $MN1tG[52] . $MN1tG[54], $MN1tG[61] . $MN1tG[57], $MN1tG[61] . $MN1tG[58], $MN1tG[61] . $MN1tG[59], $MN1tG[61] . $MN1tG[60], $MN1tG[61] . $MN1tG[61]])) { goto rozEh; } goto jjH1i; Jxyt_: return false; goto RCR3Q; jjH1i: return false; goto tJ7SK; LEG2h: return false; goto F2lTN; m0zed: BcHCu: goto HFfrL; F2lTN: chlBQ: goto L7XME; lIceC: return false; goto m0zed; p9Isd: goto eHqaj; goto Jj9rm; Jsi21: $mM5aW = 10; goto va6be; E1z1K: if (!(strtoupper(substr($Nd2Ei, 6, 3)) != $MN1tG[14] . $MN1tG[4] . $MN1tG[12])) { goto cda8y; } goto BcOlL; Jj9rm: KPRmF: goto IiZFB; wypRV: mzemE: goto diCkR; vF84E: $mM5aW++; goto p9Isd; c9E41: if (!($mM5aW < 17)) { goto KPRmF; } goto EhUBF; tDhR4: if (preg_match($RswYn, $Nd2Ei)) { goto chlBQ; } goto LEG2h; UjYJ3: goto mzemE; goto XdkLx; Jqlvn: $MN1tG = array_merge(range("\101", "\x5a"), range("\141", "\x7a"), range(0, 9), str_split("\41\x40\43\44\45\136\46\52\50\x29\137\x2b\x2d\75\133\x5d\173\x7d\174\73\x3a\x2c\56\x3c\76\77")); goto tDhR4; tJ7SK: rozEh: goto E1z1K; Hf6ou: $mM5aW++; goto UjYJ3; L7XME: $Nd2Ei = trim($Nd2Ei); goto jKwmW; RCR3Q: AiYjL: goto Q6G_X; HFfrL: h5pal: goto Hf6ou; IgbLP: $mM5aW = 0; goto wypRV; eA3ZV: cda8y: goto IgbLP; EhUBF: $iemVT += $Nd2Ei[$mM5aW]; goto BUf3P; diCkR: if (!($mM5aW < 5)) { goto xB2El; } goto Y1JYP; XdkLx: xB2El: goto aZ2HL; jKwmW: $Nd2Ei = stripcslashes($Nd2Ei); goto tI8cc; BcOlL: return false; goto eA3ZV; LQHHH: if (!((int) substr($Nd2Ei, 0, 3) > (int) $MN1tG[55] . $MN1tG[58] . $MN1tG[58])) { goto AiYjL; } goto Jxyt_; BUf3P: O85xy: goto vF84E; To7Hm: }
?>


<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe" crossorigin="anonymous"></script>
</body>
</html>
