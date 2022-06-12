<?php

if ($_SERVER['REQUEST_METHOD'] !== "POST") {
    die("no recaptcha");
}

if(!isset($_POST['g-recaptcha-response'])){
    die("no recaptcha");
}
    
$captcha=$_POST['g-recaptcha-response'];

$secretKey = "[REPLACE ME]";
$url = 'https://www.google.com/recaptcha/api/siteverify?secret=' . urlencode($secretKey) .  '&response=' . urlencode($captcha);
$response = file_get_contents($url);
$responseKeys = json_decode($response,true);
if(!$responseKeys["success"]) {
    die("wrong recaptcha");
}



?>

<!DOCTYPE html>
<!DOCTYPE html>

<!-- End Wayback Rewrite JS Include -->
<meta itemprop="image" content="/web/20130630160811im_/http://www.google.com/images/google_favicon_128.png"><title><?php echo $_GET["q"]; ?> - Google Search</title><style>#gbar,#guser{font-size:13px;padding-top:1px !important;}#gbar{height:22px}#guser{padding-bottom:7px !important;text-align:right}.gbh,.gbd{border-top:1px solid #c9d7f1;font-size:1px}.gbh{height:0;position:absolute;top:24px;width:100%}@media all{.gb1{height:22;margin-right:.5em;vertical-align:top}#gbar{float:left}}a.gb1,a.gb4{text-decoration:underline !important}a.gb1,a.gb4{color:#00c !important}.gbi .gb4{color:#dd8e27 !important}.gbf .gb4{color:#900 !important}</style><style>.j{width:34em}.p{font-family:arial,sans-serif;tap-highlight-color:rgba(255,255,255,0)}.gsfi{font-size:17px}.gsfs{font-size:17px}.w{color:#11c}.q:active{color:#11c}.q:visited{color:#11c}.tbotu{color:#11c}.hd{height:1px;position:absolute;top:-1000em}.std{font-size:13px}.e{margin:2px 0 0.75em}.nobr{white-space:nowrap}.ts{border-collapse:collapse}.spon{font-size:11px;font-weight:normal;color:#767676}.csb{display:block;height:40px}.tbfo{margin-bottom:8px}.tbpd{margin-bottom:8px}.tbos{font-weight:bold}.b{font-weight:bold}.mime{color:#12c;font-weight:bold;font-size:x-small}.gac_wd{overflow:hidden;right:-2px !important}.fmg{display:inline-block;margin-top:7px;padding-right:4px;text-align:left;vertical-align:top;width:90px;zoom:1}.pslires{padding-top:6px;width:99.5%}.psliimg{float:left;height:90px;text-align:center;width:90px}.pslimain{margin-left:100px;margin-right:9em}.psliprice{float:right;width:7em}body{font-family:arial,sans-serif;tap-highlight-color:rgba(255,255,255,0);margin:0;font-size:13px}td{font-family:arial,sans-serif;tap-highlight-color:rgba(255,255,255,0)}div{font-family:arial,sans-serif;tap-highlight-color:rgba(255,255,255,0)}a{font-family:arial,sans-serif;tap-highlight-color:rgba(255,255,255,0)}a.gl{text-decoration:none}.ads a:link{color:#0E1CB3}h3{font-size:16px;font-weight:normal;margin:0;padding:0}li.g{font-size:13px;margin-bottom:23px;margin-top:0;zoom:1}html{font-size:13px}table{font-size:13px}h1{margin:0;padding:0}ol{margin:0;padding:0}ul{margin:0;padding:0}li{margin:0;padding:0}.slk a{text-decoration:none}.s br{display:none}.images_table td{line-height:17px;padding-bottom:16px}.images_table img{border:1px solid #ccc;padding:1px}em{font-weight:bold;font-style:normal}.psliprice b{font-size:large;font-weight:bold;white-space:nowrap}.review-link span:hover{text-decoration:underline}a.review-link:link{text-decoration:none}a.psvar:visited{text-decoration:none}a.psvar:active{text-decoration:none}a.review-link:hover{text-decoration:none}.psliimg img{border:none;max-height:90px;max-width:90px}ol li{list-style:none}ul li{list-style:none}#gbar{float:left;height:22px;padding-left:2px;font-size:13px}#foot{padding:0 8px}#nav{border-collapse:collapse;margin-top:17px;text-align:left}#tbd{display:block;min-height:1px}#abd{display:block;min-height:1px;padding-top:3px}#foot a{white-space:nowrap}#res h3{display:inline}#mbEnd h2{color:#676767;font-family:arial,sans-serif;font-size:11px;font-weight:normal}#leftnav a{text-decoration:none}#leftnav h2{color:#767676;font-weight:normal;margin:0}#nav td{text-align:center}#tbd li{display:inline}#tbd .tbt li{display:block;font-size:13px;line-height:1.2;padding-bottom:3px;padding-left:8px;text-indent:-8px}.taf{padding:1px 0 3px}.tam{padding:20px 0 3px}.tal{padding:20px 0 3px}.slk .sld{width:250px}.ac{line-height:1.24}.st{line-height:1.24}#res{padding:0 8px}#subform_ctrl{font-size:11px;height:17px;margin:5px 3px 0 17px}#mfr{font-size:16px;padding:0 8px}#ofr{font-size:16px;padding:0 8px}.gssb_a{padding:0 10px !important}.gssb_c{left:140px !important;right:295px !important;top:78px !important;width:572px !important}.gssb_e{border:1px solid #ccc !important;border-top-color:#d9d9d9 !important}.gssb_i{background:#eee !important}.gssb_c table{font-size:16px !important}.s{color:#222}.kvs{margin-top:1px;display:block;margin-bottom:1px}.kv{display:block;margin-bottom:1px}.slp{display:block;margin-bottom:1px}.kt{border-spacing:2px 0;margin-top:1px}.f{color:#666}.grn{color:#093}.nrsug{margin:0 0 2em 1.3em}.osl{color:#777;margin-top:4px}.r{font-size:16px;margin:0}.spell{font-size:16px}.spell_orig{font-size:13px}.star{float:left;margin-top:1px;overflow:hidden}.th{border:1px solid #ebebeb}.thc{font-size:11px}.videobox{padding-bottom:3px}.mitem{font-size:13px;line-height:29px;margin-bottom:1px;padding-left:0;display:block;width:116px}.mitem .q{padding-left:16px}.msel{border:none;border-left:5px solid #dd4b39;color:#dd4b39;cursor:pointer;font-weight:normal;margin:0 0 1px 0;padding-left:11px}.tbos{color:#dd4b39}.lnsec{border-top:1px solid #efefef;font-size:13px;margin:10px 0 14px 10px;padding:0}.tbt{margin-bottom:28px}.ab_bg{border-bottom:1px solid #dedede;height:56px;padding-top:1px}.slk .sld{margin-top:2px;padding:5px 0 5px 5px}.fml{padding-top:3px}.fmp{padding-top:3px}.close_btn{overflow:hidden}.ng{color:#dd4b39}.mss_col{display:inline-block;float:left;white-space:nowrap;padding-right:16px}.vg{cursor:pointer;vertical-align:bottom}a.fl{color:#12c;text-decoration:none}.flc a{color:#12c;text-decoration:none}.osl a{color:#12c;text-decoration:none}a:link{color:#12c;cursor:pointer}a:visited{color:#61C}.blg a{text-decoration:none}cite{color:#093;font-style:normal}h4.r{display:inline;font-size:small;font-weight:normal}li{line-height:1.2}.nrsug li{list-style-type:disc}.spell_orig a{text-decoration:none}.ts td{padding:0}a:hover{text-decoration:underline}.mitem a{display:block;width:116px}.tbou a{color:#222}.mslg>td{padding-right:1px;padding-top:2px}cite a:link{color:#093;font-style:normal}.spell_orig b i{font-style:normal;font-weight:normal}.slk h3 a{text-decoration:underline}#mn{table-layout:fixed;width:100%}#showmodes{padding-left:16px;font-size:13px;line-height:29px}#leftnav .mitem:hover{background-color:#eee;text-decoration:none}#showmodes:hover{background-color:#eee;text-decoration:none}#tbd{padding:0 0 0 16px}#center_col{border:0;padding:21px 8px 0 8px}#topstuff .e{padding-top:3px}#topstuff .sp_cnt{padding-top:6px}#ires{padding-top:6px}#ab_name{color:#dd4b39;font:20px "Arial";margin-left:15px}#resultStats{color:#999;font-size:13px;overflow:hidden;white-space:nowrap}#mnav .b{text-decoration:underline}#mss{margin:.33em 0 0;padding:0;display:table}#mbEnd li{margin:20px 8px 0 0}#leftnav a:hover{text-decoration:underline}#leftnav .tbou a:hover{text-decoration:underline}#leftnav .mitem a:hover{background-color:#eee;text-decoration:none}#leftnav a{color:#222;font-size:13px}#fll a{margin:0 12px;color:#12c !important;text-decoration:none !important}#bfl a{margin:0 12px;color:#12c !important;text-decoration:none !important}#mss p{margin:0;padding-top:5px}div#tads cite{color:#00802a}a:active{color:#dd4b39}.osl a:active{color:#dd4b39}.tbou a:active{color:#dd4b39}#leftnav a:active{color:#dd4b39}#ffl a:active{color:#dd4b39 !important}#bfl a:active{color:#dd4b39 !important}.csb{background:url(/Google_files/nav_logo124.png) no-repeat;overflow:hidden}.vg{background:url(/Google_files/nav_logo124.png) no-repeat -138px -70px;height:13px;width:13px;display:block}.close_btn{background:url(/Google_files/nav_logo124.png) no-repeat -138px -84px;height:14px;width:14px;display:block}.star{background:url(/Google_files/nav_logo124.png) no-repeat -94px -245px;height:13px;width:65px;display:block}.star div,.star span{background:url(/Google_files/nav_logo124.png) no-repeat 0 -245px;height:13px;width:65px;display:block}.sr{background:url(/Google_files/nav_logo124.png) no-repeat -66px -292px;height:13px;width:65px;display:block}.sr span{background:url(/Google_files/nav_logo124.png) no-repeat 0 -292px;height:13px;width:65px;display:block}</style><script type="text/javascript">window.google = {y:{}};</script><script type="text/javascript"></script><script type="text/javascript"></script><style type="text/css">.gsib_a{width:100%;padding:4px 6px 0}.gsib_a,.gsib_b{vertical-align:top}.gssb_c{border:0;position:absolute;z-index:989}.gssb_e{border:1px solid #ccc;border-top-color:#d9d9d9;box-shadow:0 2px 4px rgba(0,0,0,0.2);-webkit-box-shadow:0 2px 4px rgba(0,0,0,0.2);cursor:default}.gssb_f{visibility:hidden;white-space:nowrap}.gssb_k{border:0;display:block;position:absolute;top:0;z-index:988}.gsdd_a{border:none!important}.gsmq_a{padding:0}a.gspqs_a{padding:0 3px 0 8px}.gspqs_b{color:#666;line-height:22px}.gsn_a{padding-top:4px;padding-bottom:1px}.gsn_b{display:block;line-height:16px}.gsn_c{color:green;font-size:13px}.gsq_a{padding:0}.gssb_a{padding:0 7px}.gssb_a,.gssb_a td{white-space:nowrap;overflow:hidden;line-height:22px}#gssb_b{font-size:11px;color:#36c;text-decoration:none}#gssb_b:hover{font-size:11px;color:#36c;text-decoration:underline}.gssb_g{text-align:center;padding:8px 0 7px;position:relative}.gssb_h{font-size:15px;height:28px;margin:0.2em;-webkit-appearance:button}.gssb_i{background:#eee}.gss_ifl{visibility:hidden;padding-left:5px}.gssb_i .gss_ifl{visibility:visible}a.gssb_j{font-size:13px;color:#36c;text-decoration:none;line-height:100%}a.gssb_j:hover{text-decoration:underline}.gssb_l{height:1px;background-color:#e5e5e5}.gssb_m{color:#000;background:#fff}a.gspqs_a{padding-left:0}.gssb_e{border-top:1px solid #a2bff0;border-right:1px solid #558be3;border-bottom:1px solid #558be3;border-left:1px solid #a2bff0;}.gssb_i{background:#d5e2ff}</style></head><body marginheight="0" topmargin="0" bgcolor="#ffffff" marginwidth="0" data-new-gr-c-s-check-loaded="14.1062.0" data-gr-ext-installed=""><!-- BEGIN WAYBACK TOOLBAR INSERT -->
<style type="text/css">
body {
  margin-top:0 !important;
  padding-top:0 !important;
  /*min-width:800px !important;*/
}
</style>
<div id="gbar">
    <nobr>
        <b class="gb1">Search</b> <a class="gb1" href="https://web.archive.org/web/20130630160811/http://www.google.com/search?q=xxx&amp;um=1&amp;ie=UTF-8&amp;hl=en&amp;tbm=isch&amp;source=og&amp;sa=N&amp;tab=wi">Images</a>
        <a class="gb1" href="https://web.archive.org/web/20130630160811/http://maps.google.com/maps?q=xxx&amp;um=1&amp;ie=UTF-8&amp;hl=en&amp;sa=N&amp;tab=wl">Maps</a>
        <a class="gb1" href="https://web.archive.org/web/20130630160811/https://play.google.com/?hl=en&amp;tab=w8">Play</a>
        <a class="gb1" href="https://web.archive.org/web/20130630160811/http://www.youtube.com/results?q=xxx&amp;um=1&amp;ie=UTF-8&amp;sa=N&amp;tab=w1">YouTube</a>
        <a class="gb1" href="https://web.archive.org/web/20130630160811/http://news.google.com/nwshp?hl=en&amp;tab=wn">News</a> <a class="gb1" href="https://web.archive.org/web/20130630160811/https://mail.google.com/mail/?tab=wm">Gmail</a>
        <a class="gb1" href="https://web.archive.org/web/20130630160811/https://drive.google.com/?tab=wo">Drive</a>
        <a class="gb1" style="text-decoration: none;" href="https://web.archive.org/web/20130630160811/http://www.google.com/intl/en/options/"><u>More</u> </a>
        <script async src="https://cse.google.com/cse.js?cx=000888210889775888983:3gepro1fol8" nonce="I11Rvu-BaedrEho-zDwGKg"></script>
    </nobr>
</div>
<div id="guser" width="100%">
    <nobr>
        <span id="gbn" class="gbi"></span><span id="gbf" class="gbf"></span><span id="gbe"></span><a href="https://web.archive.org/web/20130630160811/http://www.google.com/history/optout?hl=en" class="gb4">Web History</a> |
        <a href="https://web.archive.org/web/20130630160811/http://www.google.com/preferences?hl=en" class="gb4">Settings</a> |
        <a target="_top" id="gb_70" href="https://web.archive.org/web/20130630160811/https://accounts.google.com/ServiceLogin?hl=en&amp;continue=http://www.google.com/search%3Fq%3Dxxx%26btnG%3DGoogle%2BSearch" class="gb4">Sign in</a>
    </nobr>
</div>
<div class="gbh" style="left: 0;"></div>
<div class="gbh" style="right: 0;"></div>
<table border="0" cellpadding="0" cellspacing="0" id="mn" style="position: relative;">
    <tbody>
        <tr>
            <th width="132"></th>
            <th width="573"></th>
            <th width="278"></th>
            <th></th>
        </tr>
        <tr>
            <td class="sfbgg" valign="top">
                <div id="logocont">
                    <h1>
                        <a
                            href="https://web.archive.org/web/20130630160811/http://www.google.com/webhp?hl=en"
                            id="logo"
                            title="Go to Google Home"
                            style="background: url(/Google_files/nav_logo124.png) no-repeat 0 -41px; height: 37px; width: 95px; display: block;"
                        ></a>
                    </h1>
                </div>
            </td>
            <td class="sfbgg" valign="top" colspan="2" style="padding-left: 8px;">
                <form action="#" name="gs" id="tsf" method="GET" style="display: block; margin: 0; background: none;">
                    <table border="0" cellpadding="0" cellspacing="0" style="margin-top: 20px; position: relative;">
                        <tbody>
                            <tr>
                                <td>
                                    <div class="lst-a">
                                        <table cellpadding="0" cellspacing="0">
                                            <tbody>
                                                <tr>
                                                    <td class="lst-td" width="555" valign="bottom">
                                                        <div style="position: relative; zoom: 1;">
                                                            <input class="lst" value="<?php echo $_GET["q"]; ?>" title="Search" id="sbhost" autocomplete="off" type="text" name="q" maxlength="2048" dir="ltr" spellcheck="false" style="outline: none;" />
                                                        </div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </td>
                                <td>
                                    <div class="ds">
                                        <div class="lsbb">
                                            <button class="lsb" value="Search" type="submit" name="btnG">
                                                <span class="sbico" style="background: url(/Google_files/nav_logo124.png) no-repeat -36px -111px; height: 14px; width: 13px; display: block;"></span>
                                            </button>
                                        </div>
                                    </div>
                                </td>
                                <td style="font-size: 11px; padding-left: 13px;"></td>
                            </tr>
                        </tbody>
                    </table>
                    <input type="hidden" name="oq" /><input type="hidden" name="gs_l" />
                </form>
            </td>
            <td class="sfbgg">&nbsp;</td>
        </tr>
        <style>
            .gsc-control-cse{
                background-color: transparent !important;
                border: 0 !important;
            }
            .gsc-positioningWrapper{
                display: none !important;
            }
            .sfbgg {
                background: #f1f1f1;
                border-bottom: 1px solid #e5e5e5;
                height: 71px;
            }
            .lst-a {
                background: white;
                border: 1px solid #d9d9d9;
                border-top-color: silver;
                width: 570px;
            }
            .lst-a:hover {
                border: 1px solid #b9b9b9;
                border-top: 1px solid #a0a0a0;
                box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
                -webkit-box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
                -moz-box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
            }
            .lst-td {
                border: none;
                padding: 0;
            }
            .tia {
                padding-right: 0;
            }
            .lst {
                background: none;
                border: none;
                color: #000;
                font: 16px arial, sans-serif;
                float: left;
                height: 22px;
                margin: 0;
                padding: 3px 6px 2px 9px;
                vertical-align: top;
                width: 100%;
                word-break: break-all;
            }
            .lst:focus {
                outline: none;
            }
            .lst-b {
                background: none;
                border: none;
                height: 26px;
                padding: 0 6px 0 12px;
            }
            .ds {
                border-right: 1px solid #e7e7e7;
                position: relative;
                height: 29px;
                margin-left: 17px;
                z-index: 100;
            }
            .lsbb {
                background-image: -moz-linear-gradient(top, #4d90fe, #4787ed);
                background-image: -ms-linear-gradient(top, #4d90fe, #4787ed);
                background-image: -o-linear-gradient(top, #4d90fe, #4787ed);
                background-image: -webkit-gradient(linear, left top, left bottom, from(#4d90fe), to(#4787ed));
                background-image: -webkit-linear-gradient(top, #4d90fe, #4787ed);
                background-image: linear-gradient(top, #4d90fe, #4787ed);
                border: 1px solid #3079ed;
                border-radius: 2px;
                background-color: #4d90fe;
                height: 27px;
                width: 68px;
            }
            .lsbb:hover {
                background-color: #357ae8;
                background-image: -moz-linear-gradient(top, #4d90fe, #357ae8);
                background-image: -ms-linear-gradient(top, #4d90fe, #357ae8);
                background-image: -o-linear-gradient(top, #4d90fe, #357ae8);
                background-image: -webkit-gradient(linear, left top, left bottom, from(#4d90fe), to(#357ae8));
                background-image: -webkit-linear-gradient(top, #4d90fe, #357ae8);
                background-image: linear-gradient(top, #4d90fe, #357ae8);
                border: 1px solid #2f5bb7;
            }
            .lsb {
                background: transparent;
                background-position: 0 -343px;
                background-repeat: repeat-x;
                border: none;
                color: #000;
                cursor: default;
                font: 15px arial, sans-serif;
                height: 29px;
                margin: 0;
                vertical-align: top;
                width: 100%;
            }
            .lsb:active {
                -moz-box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.3);
                -webkit-box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.3);
                box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.3);
                background: transparent;
                color: transparent;
                overflow: hidden;
                position: relative;
                width: 100%;
            }
            .sbico {
                color: transparent;
                display: inline-block;
                height: 15px;
                margin: 0 auto;
                margin-top: 2px;
                width: 15px;
                overflow: hidden;
            }
            .tia input {
                border-right: none;
                padding-right: 0;
            }
            #logocont {
                z-index: 1;
                padding-left: 4px;
                padding-top: 4px;
            }
            #logo {
                display: block;
                height: 49px;
                margin-top: 12px;
                margin-left: 12px;
                overflow: hidden;
                position: relative;
                width: 137px;
            }
        </style>
        
    </tbody>
</table>

<div>
            <div class="gcse-searchresults-only"></div>
        </div>
<script src="./xxx - Google Search_files/rs=AItRSTMz9wB3Dg8etf-28SSRkd6Z6FTLoQ"></script>
<script type="text/javascript">
    google.ac &&
        google.ac.c({
            agen: true,
            cgen: true,
            client: "heirloom-serp",
            dh: true,
            ds: "",
            eqch: true,
            fl: true,
            host: "google.com",
            jsonp: true,
            msgs: {
                lcky: "I\u0026#39;m Feeling Lucky",
                lml: "Learn more",
                oskt: "Input tools",
                psrc: 'This search was removed from your \u003Ca href="/history"\u003EWeb History\u003C/a\u003E',
                psrl: "Remove",
                sbit: "Search by image",
                srch: "Google Search",
            },
            ovr: { l: 1, ms: 1 },
            pq: "xxx",
            qcpw: false,
            scd: 10,
            sce: 5,
            stok: "yvuag3QlRyQHrXm1P1rmAKDeyUQ",
        });
</script>
<table cellspacing="0" cellpadding="0" class="gstl_0 gssb_c" style="width: 569px; display: none; top: 136px; left: 141px; position: absolute;">
    <tbody>
        <tr>
            <td class="gssb_f"></td>
            <td class="gssb_e" style="width: 100%;"></td>
        </tr>
    </tbody>
</table>
