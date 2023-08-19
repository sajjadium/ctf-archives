<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=utf-8">
<script language="JavaScript">
var temp_i_id=new Array;
var temp_ch=new Array;

function setup_temp_i_id(name) {
	temp_i_id=name.split(",");
}

function setup_temp_ch(name) {
	temp_ch=name.split(";");
}


function chara_make_view(total_point)
{
	temp_st=new Array("str","smart","life","agl");
	parent.message_cls();
	document.write('<form action="wog_act.php" method="post" target="mission">');
	document.write(parent.get_temp_table1());
	document.write('<tr><td class="b1">玩家帳號：<input type="text" name="id" size="10" maxlength="12" class="style1"><BR>　　　　　★請勿輸入{ } ; &lt; &gt; , " \' \\  等符號<</td></tr>');
	document.write('<tr><td class="b1">玩家密碼：<input type="password" name="pass" size="10" class=style1><BR>　　　　　★請輸入4～8字內的半形英數。</td></tr>');
	document.write('<tr><td class="b1">玩家email：<input type="text" name="email" size="50" class=style1><BR>　　　　　★忘記密碼時是用這個信箱補發密碼,此欄必填</td></tr>');
	document.write('<tr><td class="b1">首頁名稱：<input type="text" name="site" size="40" class=style1><BR>　　　　　★你可在此宣傳你的網站，若無網站就輸入你想推薦的網站吧！</td></tr>');
	document.write('<tr><td class="b1">首頁位置：<input type="text" name="url" size="50" value="http://" class=style1><BR>　　　　　★請輸入你的首頁位置，若無網站請隨便找個你喜歡的網站輸入</td></tr>');
	document.write('<tr><td class="b1">角色性別：<input type="radio" name="sex" value="2">女　<input type="radio" name="sex" value="1">男　★請選擇角色的性別。</td></tr>');
	document.write('<tr><td class="b1">角色屬性：<input type="radio" name="s" value="1">地　<input type="radio" name="s" value="2">水 <input type="radio" name="s" value="3">火　<input type="radio" name="s" value="4">木 <input type="radio" name="s" value="5">風　<input type="radio" name="s" value="6">毒 ★請選擇角色的屬性</td></tr>');
	document.write('<tr><td class="b1">出生地點：<input type="radio" name="birth" value="0">　中央大陸<input type="radio" name="birth" value="1">　魔法王國<input type="radio" name="birth" value="2">　熱帶雨林<input type="radio" name="birth" value="3">　末日王城</td></tr>');
	document.write('<tr><td class="b1">角色圖像：<select name="i_id">');
	for(var i=0;i<temp_i_id.length;i++)
	{
		document.write('<option value="'+temp_i_id[i]+'" >'+temp_i_id[i]);
	}
	document.write('</select>　<a href="javascript://" onClick="window.open(\'wog_etc.php?f=img\',\'\',\'menubar=no,status=no,scrollbars=yes,top=50,left=50,toolbar=no,width=400,height=400\')"><font size="2">★圖像預覽★</font></a><BR>　　　　★請選擇角色的圖片。(請慎選，選擇後就無法再更改囉！！)</td></tr>');
	document.write('<tr><td class="b1">角色職業：<select name=ch >');
	for(var i=0;i<temp_ch.length;i++)
	{
		temp_c=temp_ch[i].split(",");
		document.write('<option value="'+temp_c[0]+'" >'+temp_c[1]);
	}
	document.write('</select></td></tr>');
	document.write('<tr><td class="b1">角色能力： 基本值 8<table border="1" cellspacing="0" cellpadding="0"><tr><td class="b2" width="70">力量 8</td><td class="b2" width="70">智力 8</td><td class="b2" width="70">生命 8</td><td class="b2" width="70">敏捷 8</td></tr>');
	document.write('<tr>');
	for(var j=0;j<4;j++)
	{
		document.write('<td class="b1"><select name='+temp_st[j]+'>');
		for(var i=1;i<11;i++)
		{
			document.write('<option value="'+i+'">+'+i);
		}
		document.write('</select></td>');
	}
	document.write('</tr>');
	document.write('<tr><td colspan="4" class="b1">★你共有「<font color="#FF0000"><b>'+total_point+'</b></font>」點的加分點數可增加能力值，請自行分配。分配總和超出<font color="#FF0000"><b>'+total_point+'</b></font>以上則無法註冊。</td></tr></table>');
	document.write('</td></tr>');

	document.write('<tr><td class="b1">必殺技名稱：<input type="text" name="sat_name" size="40" maxlength="40" class="style1"><br>　　　　　★請輸入你必殺技的名稱。 請勿輸入{ } ; &lt; &gt; , " \' \\  等符號</td></tr>');
	document.write('<tr><td align="center"><input type="submit" value="角色作成" ></td></tr>');
	document.write(parent.get_temp_table1());
	document.write('<input type="hidden" name="f" value="chara">');
	document.write('<input type="hidden" name="act" value="save">');
	document.write('</form>');
}

</script>
