/*===================================================== 
 Copyright (C) ETERNAL<iqstar.tw@gmail.com>
 Modify : 2005/09/17
 URL : http://www.2233.idv.tw

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
===================================================== */

var p_name="";
var my_birth="";
var my_age="";
var m_name="";
var temp_table1='<table width="97%" border="1" cellspacing="0" cellpadding="2" align="center" bordercolor="#4B689E">';
var fight_temp_table1='<table width="600" border="1" cellspacing="0" cellpadding="2" align="center" bordercolor="#4B689E">';
var temp_table2='</table>';
var tr_bgcolor="#4B689E";
var hr='<hr width="95%" size="1" color="#238CBE">';
var vData="";
var online_temp_table1='<table width="90%" border="0" cellspacing="0" cellpadding="2" align="center">';
var temp_cp_table1='<table width="80%" border="0" cellspacing="0" cellpadding="0" class="b1">';
var view_name=parent.wog_view;
var cp_jmmoney=0;
var img="./img/"
var mimg="./img/monster/"
var mid_file="";
var bbs_id="";
var nosend="#392724";
var p_sat_name="",d_a_name="",d_body_name="",d_head_name="",d_hand_name="",d_foot_name="",d_item_name="",p_group="",d_p_url="",d_ch_name="",d_s_ch_name="",d_p_homename="";
var pet_pname="",pet_mname="",t_team="",p_support_name="",pet_img="",p_support_img="";
var fightrow = new Array;
var fight_num=0;
var shock_num=0,shock_s="";
var temp_obj="";
var gf="";
var gt="";
var temp_p_hp=0;
var temp_p_hpmax=0;
var temp_m_hp=0;
var temp_m_hpmax=0;
var	tmpNum="";
sec=new Array()
sec[0]="未知區域";
sec[1]="中央平原";
sec[2]="試鍊洞窟";
sec[3]="黑暗沼澤";
sec[4]="迷霧森林";
sec[5]="古代遺跡";
sec[6]="久遠戰場";
sec[7]="王者之路";
sec[8]="幻獸森林";
sec[9]="星河異界";
sec[10]="灼熱荒漠";
sec[11]="無淵洞窟";
sec[12]="天空之城";
sec[13]="水晶之間";
sec[14]="失落古船";
sec[15]="最果之島";
birth=new Array()
birth[0]="中央大陸";
birth[1]="魔法王國";
birth[2]="熱帶雨林";
birth[3]="末日王城";
function get_temp_table1() {return temp_table1;}
function get_temp_table2() {return temp_table2;}
function setup_name(name) 
{
	p_name=name;
}
function setup_bbsid(bbsid)
{
	if(bbs_id=="")
	{
		bbs_id=bbsid;
	}
}
function setup_sat_name(psat)
{
	if(bbs_id=="")
	{
		p_sat_name=psat;
	}
	
}
function setup_mname(name) {m_name=name;}
function setup_jmmoney(money) {cp_jmmoney=money;}
function get_name() {return p_name;}
function get_mname() {return m_name;}
function window_open(a,b,c)
{
	if(a!="")
	{
		alert(a);
	}
	window.open(b,c);
}

function datechk(s,f)
{
	var thisfrom=parent.foot.document.f1;
	var error="";
	if(thisfrom.ats1.disabled==true)
	{
		error="15秒內不能冒險";
	}
	if(f.f_count.value > 40)
	{
		error="戰鬥回合數不能大於"+f_count;
	}
	if(f.a_type[0].checked==true)
	{
		thisfrom.act.value=f.act1.value;
		thisfrom.temp_id.value=0;
	}
	if(f.a_type[1].checked==true)
	{
		thisfrom.act.value=f.act2.value;
		thisfrom.temp_id.value=1;
		if(f.act2.value=="20")
		{
			if(!confirm("挑戰冠軍需付3000元費用"))
			{
				error="結束挑戰";
			}
		}
		if(f.act2.value=="21")
		{
			if(thisfrom.towho.value=="")
			{
				error="沒有選擇對像不能PK";
			}
		}
		
	}
	if(thisfrom.act.value=="")
	{
		error="請選擇場地";
	}
	if(error != "")
	{
		alert(error);
	}else
	{
		if(f.a_mode[0].checked==true)
		{
			thisfrom.temp_id2.value=1;
		}
		if(f.a_mode[1].checked==true)
		{
			thisfrom.temp_id2.value=2;
		}
		Sookie("wog_set_cookie", thisfrom.temp_id.value+","+thisfrom.act.value+","+thisfrom.temp_id2.value+","+f.act_area.value)
		Sookie("wog_set_f_count", f.f_count.value)
		Sookie("wog_set_f_hp", f.f_hp.value)
		thisfrom.f.value="fire";
		thisfrom.action="wog_fight.php";
		thisfrom.at_type.value=s;
		thisfrom.sat_name.value=f.sat_name.value;
		thisfrom.temp_id3.value=f.f_count.value;
		thisfrom.temp_id4.value=f.f_hp.value;
		thisfrom.submit();
	}
}

function change_mission(s,f)
{
	var thisfrom=f;
	if(s==0)
	{
		thisfrom.a_type[0].checked=true;
	}else if(s==1)
	{
		thisfrom.a_type[1].checked=true;
	}
}

function foot_disabled()
{
	for(var i=0;i<parent.foot.document.f1.elements.length;i++)
		{  
			parent.foot.document.f1.elements[i].disabled=true;
		}
}


function foot_fire()
{
	for(var i=0;i<parent.foot.document.f1.elements.length;i++)
		{  
			parent.foot.document.f1.elements[i].disabled=false;
		}
}

//##### page head begin #####
function message_cls(a,bline) {
	var ff=parent.wog_view.document;
	if(a!=null)
	{
		ff=a;
	}
	if(bline==null)
	{
		bline=2;
	}
	ff.close();
    ff.write('<html>');
    ff.write('<head>');
    ff.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">');
    ff.write('<meta http-equiv=Cache-Control content="no-cache">');
	ff.write('<style type=text/css>');
    ff.write('td {font-family : verdana,Arial,Helvetica ;font-size : 10pt;	text-align : center;}');
    ff.write('.b1 {text-align : left;}');
    ff.write('</style>');
    ff.write('</head>');
    ff.write('<body bgcolor="#000000" text="#EFEFEF" link="#EFEFEF" vlink="#EFEFEF" alink="#EFEFEF" style="border: '+bline+' inset;" >');
}

//####### fight begin #######
function Sookie(name, value) { 
	document.cookie = name + "=" + value
} 

function Gookie(name) { 
	var arg = name + "=";
	var alen = arg.length; 
	var clen = document.cookie.length; 
	var i = 0; 
	while (i < clen) { 
		var j = i + alen; 
		if (document.cookie.substring(i, j) == arg) 
			return GookieVal (j); 
		i = document.cookie.indexOf(" ", i) + 1; 
		if (i == 0) break; 
	} 
	return null; 
}

function GookieVal(offset) { 
	var endstr = document.cookie.indexOf (";", offset); 
	if (endstr == -1) 
		endstr = document.cookie.length; 
	return document.cookie.substring(offset, endstr); 
}

function select_area(num,s)
{
	var ctr=0;
	s.act1.selectedIndex=0;
	s.act1.options[0]=new Option("請選擇場所","");
	if(num=="1") {	s.act1.options[ctr]=new Option("中央平原","1");ctr=ctr+1;}
	if(num=="1") {	s.act1.options[ctr]=new Option("黑暗沼澤","3");ctr=ctr+1;}
	if(num=="1") {	s.act1.options[ctr]=new Option("王者之路","7");ctr=ctr+1;}
	if(num=="1") {	s.act1.options[ctr]=new Option("水晶之間","13");ctr=ctr+1;}	
	if(num=="2") {	s.act1.options[ctr]=new Option("試鍊洞窟","2");ctr=ctr+1;}
	if(num=="2") {	s.act1.options[ctr]=new Option("幻獸森林","8");ctr=ctr+1;}
	if(num=="2") {	s.act1.options[ctr]=new Option("天空之城","12");ctr=ctr+1;}	
	if(num=="2") {	s.act1.options[ctr]=new Option("最果之島","15");ctr=ctr+1;}	
	if(num=="3") {	s.act1.options[ctr]=new Option("迷霧森林","4");ctr=ctr+1;}
	if(num=="3") {	s.act1.options[ctr]=new Option("無淵洞窟","11");ctr=ctr+1;}
	if(num=="3") {	s.act1.options[ctr]=new Option("星河異界","9");ctr=ctr+1;}
	if(num=="4") {	s.act1.options[ctr]=new Option("灼熱荒漠","10");ctr=ctr+1;}
	if(num=="4") {	s.act1.options[ctr]=new Option("古代遺跡","5");ctr=ctr+1;}
	if(num=="4") {	s.act1.options[ctr]=new Option("久遠戰場","6");ctr=ctr+1;}
	if(num=="4") {	s.act1.options[ctr]=new Option("失落古船","14");ctr=ctr+1;}
	if(ctr==0)
	{
		ctr=1;
	}
	s.act1.length=ctr;
	s.act1.options[0].selected=true;
}
function ad_view()
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1);
	f.write('<form name=f1>');
	f.write('<tr><td><input type="radio" name="a_type" value="1" checked>冒險修行 <select name="act_area" onChange="parent.select_area(this.options[this.options.selectedIndex].value,this.form)"><option value="" SELECTED>選擇場所</option><option value="1" >中央大陸</option><option value="2" >魔法王國</option><option value="3" >熱帶雨林</option><option value="4" >末日王城</option></select>');
	f.write(' <select name="act1" onChange="parent.change_mission(0,this.form)"><option value="" SELECTED>選擇場所</option></select></td></tr>');
	f.write('<tr><td><input type="radio" name="a_type" value="2" >武鬥競技 <select name="act2" onChange="parent.change_mission(1,this.form)"><option value="" SELECTED>選擇模式</option><option value="20" >挑戰冠軍</option><option value="21" > PK 挑戰</option></select></td></tr>');
	f.write('<tr><td ><input type="radio" name="a_mode" value="1" checked>快速模式  <input type="radio" name="a_mode" value="2" >一般模式</td></tr>');
	f.write('<tr><td >戰鬥回合數 <input type="text" name="f_count" value="20" size="3" maxlength="2"> (最大'+f_count+')</td></tr>');
	f.write('<tr><td >HP低於 <input type="text" name="f_hp" value="15" size="3" maxlength="2"> %自動使用HP恢復劑</td></tr>');
	f.write('<tr><td ><input type="button" value="物理攻擊" onClick="parent.datechk(1,document.forms[0])"> <input type="button" value="魔法攻擊" onClick="parent.datechk(2,document.forms[0])"></td></tr>');
	f.write('<tr><td><input type="button" value="攻打領土" onClick="parent.act_click(\'group\',\'fire_list_peo\')">--有加入公會才能使用</td></tr>');
	f.write('<tr><td>必殺技名稱 <input type="text" name="sat_name" size="40" maxlength="60" value="'+p_sat_name+'"></td></tr>');
	f.write('</form>');
	f.write(temp_table2);
	var temp_s=Gookie("wog_set_cookie");
	if(temp_s!=null)
	{
		var s1=temp_s.split(",");
		if(s1[0]==0)
		{
			f.write('<script>document.forms[0].a_type[0].checked=true;document.forms[0].a_type[1].checked=false;parent.select_area("'+s1[3]+'",document.forms[0]);document.forms[0].act_area.value='+s1[3]+';document.forms[0].act1.value='+s1[1]+';</script>');
		}else
		{
			f.write('<script>document.forms[0].a_type[1].checked=true;document.forms[0].a_type[0].checked=false;document.forms[0].act2.value='+s1[1]+';</script>');
		}
		if(s1[2]==1)
		{
			f.write('<script>document.forms[0].a_mode[0].checked=true;document.forms[0].a_mode[1].checked=false;</script>');
		}else
		{
			f.write('<script>document.forms[0].a_mode[0].checked=true;document.forms[0].a_mode[1].checked=false;</script>');
//			view_name.document.write('<script>document.forms[0].a_mode[1].checked=true;document.forms[0].a_mode[0].checked=false;</script>');
		}
	}
	var temp_s=Gookie("wog_set_f_count");
	if(temp_s!=null)
	{
		f.write('<script>document.f1.f_count.value='+temp_s+';</script>');
	}
	var temp_s=Gookie("wog_set_f_hp");
	if(temp_s!=null)
	{
		f.write('<script>document.f1.f_hp.value='+temp_s+';</script>');
	}
}

function fire_date(p_at,p_df,p_mat,p_mdf,p_hp,p_hpmax,p_s,p_img_set,i_img,m_at,m_df,m_mat,m_mdf,m_hp,m_hpmax,m_s,m_name,m_img,f_status)
{
	var f=parent.wog_view.document;
	var p_name=get_name();
	temp_p_hp=p_hp;
	temp_p_hpmax=p_hpmax;
	temp_m_hp=m_hp;
	temp_m_hpmax=m_hpmax;
	var temp_php_img=(temp_p_hp/temp_p_hpmax)*150;
	var temp_mhp_img=(temp_m_hp/temp_m_hpmax)*150;
	var p_img="";
	setup_mname(m_name);
	message_cls();
	p_s=s_status(p_s);
	m_s=s_status(m_s);
	if(m_img=="")
	{
		m_img="no_img.jpg";
	}
	if(f_status==1)
	{
		if(m_img.indexOf("http") == -1)
		{
			m_img=img+m_img+".gif";
		}		
		m_img='<img id=g2 src="'+m_img+'" border="0" style="position: absolute;left: 60%;top: 220;Z-INDEX: 1;visibility: visible">';
	}else
	{
		m_img=mimg+m_img;
		m_img='<img id=g2 src="'+m_img+'" border="0" style="position: absolute;left: 60%;top: 175;Z-INDEX: 1;visibility: visible">';
	}
	if(p_img_set==1)
	{
		p_img=i_img;
	}else
	{
		p_img=img+i_img+".gif";
	}
	f.write(fight_temp_table1+'<tr><td colspan="2">'+p_name+'</td><td colspan="2" >'+m_name+'</td></tr>');
	f.write('<tr><td width="150">HP</td><td class=b1 width="150"><img src='+img+'bar/bhg.gif border="0" width="'+temp_php_img+'" id="p_img"  height="9" alt=""></td><td width="150">HP</td><td class=b1 width="150"><img src='+img+'bar/bhg.gif border="0" width="150" id="m_img"  height="9" alt=""></td></tr>');
	f.write('<tr><td>物理攻擊</td><td>'+p_at+'</td><td>物理攻擊</td><td>'+m_at+'</td></tr>');
	f.write('<tr><td>物理防禦</td><td>'+p_df+'</td><td>物理防禦</td><td>'+m_df+'</td></tr>');	
	f.write('<tr><td>魔法攻擊</td><td>'+p_mat+'</td><td>魔法攻擊</td><td>'+m_mat+'</td></tr>');	
	f.write('<tr><td>魔法防禦</td><td>'+p_mdf+'</td><td>魔法防禦</td><td>'+m_mdf+'</td></tr>');	
	f.write('<tr><td>屬性</td><td>'+p_s+'</td><td>屬性</td><td>'+m_s+'</td></tr>');
	f.write(temp_table2);
	f.write('<table width="600" border="0" cellspacing="0" cellpadding="0" align="center" >');
	f.write('<tr><td width="50%" height="185" align="center"><img id=g1 src="'+p_img+'" border="0" style="position: absolute;left: 23%;top: 220;Z-INDEX: 1;visibility: visible"></td><td align="center" width="50%" height="170">'+m_img+'</td></tr>');
//	f.write('<tr><td colspan="2" align="center">'+hr+'<div align="center" id="a1"></td></tr>');
	f.write(temp_table2);
	f.write('<br><table width="97%" border="0" cellspacing="0" cellpadding="0" align="center" ><tr><td colspan="2" align="center">'+hr+'<div align="center" id="a1"></td></tr>');
	f.write(temp_table2);
	f.write('<img id=g3 border="0" style="position: absolute;left: 23%;top: 175;Z-INDEX: 1;visibility: hidden">');	
	if(p_support_name!="")
	{
		f.write('<img id=g4 src="'+img+p_support_img+'.gif" border="0" style="position: absolute;left: 23%;top: 220;Z-INDEX: 1;visibility: hidden">');	
	}	
}

function set_fight(temp_fightrow)
{
	fightrow=temp_fightrow;
	parent.show_fightrow();
}
function show_fightrow()
{
	var f=parent.wog_view.document;
	if(fight_num==0)
	{
		f.getElementById("a1").innerHTML=fightrow[fight_num];
	}else
	{
		eval(fightrow[fight_num]);
	}
	fight_num++;
	if(fight_num <= fightrow.length)
	{
		window.setTimeout("show_fightrow()",1000);
	}else
	{
		fight_num=0;
	}
}

function pact_date(temp_d,s,ss,support) 
{
	var f=parent.wog_view.document;
	temp_m_hp=temp_m_hp-temp_d;
	if(temp_m_hp<0){temp_m_hp=0;}
	var temp_mhp_img=(temp_m_hp/temp_m_hpmax)*150;
	f.getElementById("m_img").width=temp_mhp_img;
	f.getElementById("m_img").alt=temp_m_hp+"/"+temp_m_hpmax;
	if(support==0)
	{
		f.getElementById("g1").style.visibility="visible";
		if(f.getElementById("g3")!=null)
		{
			f.getElementById("g3").style.visibility="hidden";
		}		
		if(f.getElementById("g4")!=null)
		{
			f.getElementById("g4").style.visibility="hidden";
		}
		view_fight(temp_d,s,ss,p_name,m_name);
	}else
	{
		f.getElementById("g1").style.visibility="hidden";
		f.getElementById("g3").style.visibility="hidden";
		f.getElementById("g4").style.visibility="visible";
		view_fight(temp_d,s,ss,p_support_name,m_name);
	}

	gf=f.getElementById("g2").style.left;
	gf=gf.replace("%","");
	gt=f.getElementById("g2").style.top;
	shock_num=0;
	temp_obj=f.getElementById("g2").style;
	shock_s=s;
	shock_fight();

}
function mact_date(temp_d,s,ss)
{	

	var f=parent.wog_view.document;
	temp_p_hp=temp_p_hp-temp_d;
	if(temp_p_hp<0){temp_p_hp=0;}
	var temp_php_img=(temp_p_hp/temp_p_hpmax)*150;
	f.getElementById("p_img").width=temp_php_img;
	f.getElementById("p_img").alt=temp_p_hp+"/"+temp_p_hpmax;
	view_fight(temp_d,s,ss,m_name,p_name);	
	gf=f.getElementById("g1").style.left;
	gf=gf.replace("%","");
	gt=f.getElementById("g1").style.top;
	shock_num=0;
	temp_obj=f.getElementById("g1").style;
	shock_s=s;
	shock_fight();
}
function pet_act_date(temp_d,s,pet_img) 
{	

	var f=parent.wog_view.document;
	if(pet_img!="" && f.getElementById("g3").src=="")
	{
		f.getElementById("g3").src=mimg+pet_img;
	}else if(pet_img=="" && f.getElementById("g3").src=="")
	{
		f.getElementById("g3").src=mimg+"no_img.jpg";	
	}
	f.getElementById("g1").style.visibility="hidden";
	if(f.getElementById("g3")!=null)
	{
		f.getElementById("g3").style.visibility="visible";
	}
	if(f.getElementById("g4")!=null)
	{
		f.getElementById("g4").style.visibility="hidden";
	}
	temp_m_hp=temp_m_hp-temp_d;
	if(temp_m_hp<0){temp_m_hp=0;}
	var temp_mhp_img=(temp_m_hp/temp_m_hpmax)*150;
	f.getElementById("m_img").width=temp_mhp_img;
	f.getElementById("m_img").alt=temp_m_hp+"/"+temp_m_hpmax;
	view_fight(temp_d,s,"",pet_pname,m_name);
	gf=f.getElementById("g2").style.left;
	gf=gf.replace("%","");
	gt=f.getElementById("g2").style.top;
	shock_num=0;
	temp_obj=f.getElementById("g2").style;
	shock_s=s;
	shock_fight();
}
function pet_def_date(temp_d,s,pet_img,ss)
{	
	var f=parent.wog_view.document;
	if(pet_img!="" && f.getElementById("g3").src=="")
	{
		f.getElementById("g3").src=mimg+pet_img;
	}else if(pet_img=="" && f.getElementById("g3").src=="")
	{
		f.getElementById("g3").src=mimg+"no_img.jpg";	
	}
	f.getElementById("g1").style.visibility="hidden";
	f.getElementById("g3").style.visibility="visible";
	view_fight(temp_d,s,ss,m_name,pet_pname);
	gf=f.getElementById("g3").style.left;
	gf=gf.replace("%","");
	gt=f.getElementById("g3").style.top;
	shock_num=0;
	temp_obj=f.getElementById("g3").style;
	if(ss=="1")
	{
		f.getElementById("a1").innerHTML="<font color=#89C7F3>"+pet_pname+"</font> 戰敗";
	}
	shock_s=s;
	shock_fight();
}
function shock_fight()
{
	var shock_ss=1;
	if(shock_s!="")
	{
		shock_ss=3;
	}
	temp_obj.left=(parseInt(gf)+(Math.floor(Math.random()*3*shock_ss)))+"%";
	temp_obj.top=(parseInt(gt)+(Math.floor(Math.random()*10*shock_ss)));
	shock_num++;
	if(shock_num<15)
	{
		window.setTimeout("shock_fight()",30);
	}else
	{
		temp_obj.left=gf+"%";
		temp_obj.top=gt;
	}
}
function view_fight(temp_d,s,ss,f,d)
{
	var fv=parent.wog_view.document;
	temp_d=' <font color=red><b>'+temp_d+'<b></font>';
	(f==p_name)?f='<font color="#89C7F3">'+f+'</font>':f='<font color="#81D8A8">'+f+'</font>';
	(d==p_name)?d='<font color="#89C7F3">'+d+'</font>':d='<font color="#81D8A8">'+d+'</font>';
	if(ss!="")
	{
		ss='<img src="'+img+'ss.gif" border="0">';
	}
	if(s!="")
	{	
		fv.getElementById("a1").innerHTML=ss+f+' 發動 <b><font color="#FF0000" size="+2">'+s+'</b></font> 給予 '+d+temp_d+' 點傷害';
	}else
	{	
		fv.getElementById("a1").innerHTML=ss+f+' 給予 '+d+temp_d+' 傷害';
	}
}

function miss_date(f,d)
{	
	var fv=parent.wog_view.document;
	(f==p_name)?f='<font color="#89C7F3">'+f+'</font>':f='<font color="#81D8A8">'+f+'</font>';
	(d==p_name)?d='<font color="#89C7F3">'+d+'</font>':d='<font color="#81D8A8">'+d+'</font>';
	fv.getElementById("a1").innerHTML=f+' 展開攻擊 '+d+' 快速閃開攻擊';
}

function end_date(s,en,getexp,getmoney,p_hp)
{	
	var f=parent.wog_view.document;
	var enstr="";
	if(en=="0")
	{
		enstr="戰敗了!!!";
	}else if(en=="1")
	{
		enstr="獲得了勝利！！";
	}
	f.write(hr);
	f.write(temp_table1+'<tr><td ><b>'+s+' '+enstr+'</b></td></tr>');
	f.write('<tr><td class="b1"><b>HP剩下 '+p_hp+'</b></td></tr>');
	f.write('<tr><td class="b1"><b>獲得經驗值 '+getexp+'</b></td></tr>');
	f.write('<tr><td class="b1"><b>獲得金錢 '+getmoney+'</b></td></tr>');
	f.write(temp_table2);
}

function get_item(i,s)
{	
	var f=parent.wog_view.document;
	var enstr="";
	if(s==0)
	{
		enstr="裝備欄超過15樣物品無法裝入";
	}else if(s==1)
	{
		enstr="幸運撿到";
	}
	f.write(hr);
	f.write(temp_table1+'<tr><td ><b>'+enstr+' '+i+'</b></td></tr>');
	f.write(temp_table2);
}

function fight_event(s,temp_d)
{
	var f=parent.wog_view.document;	
	temp_p_hp=parseInt(temp_p_hp)+parseInt(temp_d);
	if(temp_p_hp>temp_p_hpmax)
	{
		temp_p_hp=temp_p_hpmax;
	}
	var temp_php_img=(temp_p_hp/temp_p_hpmax)*150;
	f.getElementById("p_img").width=temp_php_img;
	f.getElementById("p_img").alt=temp_p_hp+"/"+temp_p_hpmax;
	f.write(hr);
	f.write(temp_table1+'<tr><td ><b>'+p_name+' 使用 '+s+'</b></td></tr>');
	f.write(temp_table2);
}
function lv_up(str,agl,smart,life,vit,au,be,up_type)
{
	var f=parent.wog_view.document;
	if(up_type==null)
	{
		f.write(hr);
		f.write(temp_table1+'<tr><td class="b1"><b>'+p_name+' 等級上升 </b></td></tr>');
		parent.lv_up2(str,agl,smart,life,vit,au,be,null);
	}
}
function lv_up2(str,agl,smart,life,vit,au,be,p_exp)
{
	var f=parent.wog_view.document;
	if(p_exp!=null)
	{
		message_cls();
		f.write(temp_table1+'<tr><td class="b1"><b>'+p_name+' 能力上升 </b></td></tr>');
	}
	f.write('<tr><td class="b1"><b>力量上升 '+str+'</b></td></tr>');
	f.write('<tr><td class="b1"><b>速度上升 '+agl+'</b></td></tr>');
	f.write('<tr><td class="b1"><b>智力上升 '+smart+'</b></td></tr>');
	f.write('<tr><td class="b1"><b>生命上升 '+life+'</b></td></tr>');
	f.write('<tr><td class="b1"><b>體質上升 '+vit+'</b></td></tr>');
	f.write('<tr><td class="b1"><b>魅力上升 '+au+'</b></td></tr>');
	f.write('<tr><td class="b1"><b>信仰上升 '+be+'</b></td></tr>');
	if(p_exp!=null)
	{
		f.write('<tr><td class="b1"><b>經驗值上升 '+p_exp+'</b></td></tr>');
	}
	f.write(temp_table2);
}
function bag_up(str)
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1+'<tr><td class="b1"><b>道具欄增加 '+str+' 格</b></td></tr>');
	f.write(temp_table2);
}
function cont_fight(lv,p_id,win,s)
{	
	var f=parent.wog_view.document;
	f.write(hr);
	f.write(temp_table1);
	f.write('<form action="wog_fight.php" method="post" target="mission">');
	f.write('<tr><td>挑戰等級 LV'+lv+' <input type="submit" value="挑戰下一位">(對戰間隔時間3秒鐘)</td></tr>');
	f.write('<input type="hidden" name="f" value="fire">');
	f.write('<input type="hidden" name="act" value="22">');
	f.write('<input type="hidden" name="at_type" value="'+s+'">');
	f.write('<input type="hidden" name="p_id" value="'+p_id+'">');
	f.write('<input type="hidden" name="p_lv" value="'+lv+'">');
	f.write('<input type="hidden" name="win" value="'+win+'">');
	f.write('<input type="hidden" name="temp_id" value="1">');
//	f.write('<input type="hidden" name="sat_name" value="'+p_sat_name+'">');
	f.write('</form>');
	f.write(temp_table2);
}

function cp_end(p_name)
{
	var f=parent.wog_view.document;
	f.write(temp_table1);
	f.write('<tr><td  >'+p_name+' 順利當上冠軍 </td></tr>')
	f.write(temp_table2);
}

//##### shop begin #####
function select_store()
{
	message_cls();
	var f=parent.wog_view.document;
	f.write('<form action="wog_act.php" method="post" target="mission" name="f1" >');
	f.write(temp_table1);
	f.write('<tr><td colspan="2" >請選擇要進入的店</td></tr>')
	f.write('<tr><td >武器裝具</td><td><input type="button" value="LV1" onClick="parent.th_submit(document.f1,1,0)"> <input type="button" value="LV2" onClick="parent.th_submit(document.f1,2,0)"> <input type="button" value="LV3" onClick="parent.th_submit(document.f1,3,0)"> <input type="button" value="LV4" onClick="parent.th_submit(document.f1,4,0)"> <input type="button" value="LV5" onClick="parent.th_submit(document.f1,5,0)"> <input type="button" value="LV6" onClick="parent.th_submit(document.f1,6,0)"> <input type="button" value="LV7" onClick="parent.th_submit(document.f1,7,0)"></td></tr>');
	f.write('<tr><td >頭部裝具</td><td><input type="button" value="LV1" onClick="parent.th_submit(document.f1,1,1)"> <input type="button" value="LV2" onClick="parent.th_submit(document.f1,2,1)"> <input type="button" value="LV3" onClick="parent.th_submit(document.f1,3,1)"> <input type="button" value="LV4" onClick="parent.th_submit(document.f1,4,1)"> <input type="button" value="LV5" onClick="parent.th_submit(document.f1,5,1)"> <input type="button" value="LV6" onClick="parent.th_submit(document.f1,6,1)"></td></tr>');
	f.write('<tr><td >身體裝具</td><td><input type="button" value="LV1" onClick="parent.th_submit(document.f1,1,2)"> <input type="button" value="LV2" onClick="parent.th_submit(document.f1,2,2)"> <input type="button" value="LV3" onClick="parent.th_submit(document.f1,3,2)"> <input type="button" value="LV4" onClick="parent.th_submit(document.f1,4,2)"> <input type="button" value="LV5" onClick="parent.th_submit(document.f1,5,2)"> <input type="button" value="LV6" onClick="parent.th_submit(document.f1,6,2)"></td></tr>');
	f.write('<tr><td >手部裝具</td><td><input type="button" value="LV1" onClick="parent.th_submit(document.f1,1,3)"> <input type="button" value="LV2" onClick="parent.th_submit(document.f1,2,3)"> <input type="button" value="LV3" onClick="parent.th_submit(document.f1,3,3)"> <input type="button" value="LV4" onClick="parent.th_submit(document.f1,4,3)"> <input type="button" value="LV5" onClick="parent.th_submit(document.f1,5,3)"> <input type="button" value="LV6" onClick="parent.th_submit(document.f1,6,3)"></td></tr>');
	f.write('<tr><td >腳部裝具</td><td><input type="button" value="LV1" onClick="parent.th_submit(document.f1,1,4)"> <input type="button" value="LV2" onClick="parent.th_submit(document.f1,2,4)"> <input type="button" value="LV3" onClick="parent.th_submit(document.f1,3,4)"> <input type="button" value="LV4" onClick="parent.th_submit(document.f1,4,4)"> <input type="button" value="LV5" onClick="parent.th_submit(document.f1,5,4)"> <input type="button" value="LV6" onClick="parent.th_submit(document.f1,6,4)"></td></tr>');
	f.write('<tr><td >其他商店</td><td><input type="button" value="道具屋" onClick="parent.th_submit(document.f1,1,\'5,6\')"> <input type="button" value="銀行中心" onClick=parent.act_click("bank","view")> <input type="button" value="手術室" onClick=parent.black_shop()> <input type="button" value="復活房" onClick=if(confirm("復活會減少經驗值1/5，確定是否復活")){parent.act_click(\'chara\',\'revive\')}></td></tr>');
	f.write('<tr><td >其他商店</td><td><input type="button" value="職業中心" onClick="parent.act_click(\'job\',\'view\')" accesskey="j"> <input type="button" value="牧　場" name="ats2" onClick="parent.act_click(\'pet\',\'index\')"> <input type="button" value="合成大師" onClick="parent.act_click(\'syn\',\'list\')"></tr>');
	f.write('<tr><td >其他商店</td><td ><input type="button" value="老鼠牙子仕事所" onClick="parent.act_click(\'mission\',\'1\')"> <input type="button" value="黑街仕事所" onClick="parent.act_click(\'mission\',\'2\')"></td></tr>');
	f.write('<tr><td >其他商店</td><td ><input type="button" value="銀鯨仕事所" onClick="parent.act_click(\'mission\',\'3\')"> <input type="button" value="孤貓仕事所" onClick="parent.act_click(\'mission\',\'4\')"></td></tr>');
	f.write(temp_table2);
	f.write('<input type="hidden" name="f" value="shop">');
	f.write('<input type="hidden" name="act" value="view">');
	f.write('<input type="hidden" name="temp_id" value="">');
	f.write('<input type="hidden" name="temp_id2" value="">');
	f.write('</form>');
}
function shop_home_view(s,a,temp_id,ss,temp_id2,df_total,page)
{
	message_cls();
	var f=parent.wog_view.document;
	f.write('<form action="wog_act.php" method="post" name=pageform target="mission">');
	pagesplit(df_total,page);
	f.write('<input type="hidden" name="page" value="">');	
	f.write('<input type="hidden" name="f" value="shop">');	
	f.write('<input type="hidden" name="act" value="view">');
	f.write('<input type="hidden" name="temp_id" value="'+temp_id+'">');
	f.write('<input type="hidden" name="temp_id2" value="'+temp_id2+'">');
	f.write('</form>');
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write(temp_table1);
	f.write('<tr><td></td><td>物攻擊力</td><td>魔攻擊力</td><td>物防禦力</td><td>魔防禦力</td><td>速度</td><td>職業</td><td>能力限制</td><td>名稱</td><td>價格</td></tr>');
	if(s!="")
	{
		var s1=s.split(";");
		for(var i=0;i<s1.length;i++)
		{
			var s2=s1[i].split(",");
			f.write('<tr><td ><input type="radio" name="adds" value="'+s2[0]+'"></td><td>'+s2[6]+'</td><td>'+s2[7]+'</td><td>'+s2[1]+'</td><td>'+s2[2]+'</td><td>'+s2[3]+'</td><td>'+s2[11]+'</td><td>力:'+s2[8]+' 速:'+s2[9]+' 智:'+s2[10]+'</td><td>'+s2[5]+'</td><td>'+s2[4]+'</td></tr>');
		}
	}else
	{
		f.write('<tr><td colspan="10" >沒有可以使用的裝具</td></tr>');	
	}
	var s1=ss.split(",");
	f.write('<tr bgcolor="#777779"><td ><font color="#FF0000">E</font></td><td>'+s1[4]+'</td><td>'+s1[5]+'</td><td>'+s1[0]+'</td><td>'+s1[1]+'</td><td>'+s1[2]+'</td><td>-----</td><td>-------</td><td>'+s1[3]+'</td><td>-------</td></tr>');
	if(temp_id=="5,6")
	{	
		f.write('<tr><td colspan="10" >請選擇數量 <select name="buy_num" size="1">');
		for(var i=1;i<10;i++)
		{
			f.write('<option value="'+i+'">'+i+'</option>');
		}
		f.write('</select></td></tr>');
	}
	f.write('<tr><td colspan="10" ><input type="submit" value="確定購買"></td></tr>');
	f.write('<tr><td colspan="10" >身上金額 '+s1[6]+'</td></tr>');
	f.write(temp_table2);
	f.write('<input type="hidden" name="f" value="shop">');	
	f.write('<input type="hidden" name="act" value="buy">');
	f.write('<input type="hidden" name="temp_id" value="'+temp_id+'">');
	f.write('</form>');
}

function black_shop()
{
	message_cls();
	var f=parent.wog_view.document;
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write('<input type="hidden" name="f" value="store">');	
	f.write('<input type="hidden" name="act" value="img">');
	f.write(temp_table1);
	f.write('<tr><td>變更角色圖像</td></tr>');
	f.write('<tr><td>輸入圖像編號 <input type="text" name="num" size="2"> <a href="javascript://" onClick="window.open(\'wog_etc.php?f=img\',\'\',\'menubar=no,status=no,scrollbars=yes,top=50,left=50,toolbar=no,width=400,height=400\')">圖像預覽</a></td></tr>');
	f.write('<tr><td><input type="submit" value="使用系統圖像"></td></tr>');
	f.write('<tr><td>變臉手術需花30萬</td></tr>');
	f.write(temp_table2);
	f.write('</form>');
	f.write('<p>');
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write('<input type="hidden" name="f" value="store">');	
	f.write('<input type="hidden" name="act" value="img2">');
	f.write(temp_table1);
	f.write('<tr><td>輸入圖像連結 <input type="text" name="url" value="http://" size="45" maxlength="150"> </td></tr>');
	f.write('<tr><td>(最佳size請勿超過 120*120)</td></tr>');
	f.write('<tr><td><input type="submit" value="使用自訂圖像"></td></tr>');
	f.write('<tr><td>變臉手術需花30萬</td></tr>');
	f.write(temp_table2);
	f.write('</form>');
/*
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write('<input type="hidden" name="f" value="store">');	
	f.write('<input type="hidden" name="act" value="sex">');
	f.write(temp_table1);
	f.write('<tr><td>變更角色性別</td></tr>');
	f.write('<tr><td>男 <input type="radio" name="num" value="1"> 女 <input type="radio" name="num" value="2"></td></tr>');
	f.write('<tr><td><input type="submit" value="改變性別"></td></tr>');
	f.write('<tr><td>變性手術需花100萬</td></tr>');
	f.write(temp_table2);
	f.write('</form>');
*/
}

function sale_item(s)
{
	var temp_s="";
	if(s!=null)
	{
		if(s.length!=undefined)
		{
			for(var i=0;i<s.length;i++)
			{
				if(s[i].checked==true)
				{
					temp_s+=","+s[i].value;
				}			
			}
			temp_s=temp_s.substr(1,temp_s.length);
		}else
		{
			temp_s=s.value;
		}
	}
	var s1=temp_s.split(",");
	message_cls();
	var f=parent.wog_view.document;
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write(temp_table1);
	f.write('<tr><td colspan="3">拍賣商品</td></tr>');
	f.write('<tr><td colspan="3">拍賣時間單位為天數,時間到期自動下架</td></tr>');
	f.write('<tr><td>'+s1[1]+'</td><td>價格 <input type="text" name="money" size="9" maxlength="9">元</td><td>拍賣時間 <input type="text" name="day" size="2" maxlength="2">天 </td></tr>');
	f.write('<tr><td colspan="3"><input type="submit" value="開始拍賣"></td></tr>');
	f.write('<tr><td colspan="3">拍賣時間不能超過10天,一人拍賣的商品不能超過5種</td></tr>');
	f.write(temp_table2);
	f.write('<input type="hidden" name="f" value="sale">');	
	f.write('<input type="hidden" name="act" value="sale">');
	f.write('<input type="hidden" name="item_id" value="'+s1[0]+'">');
	f.write('</form>');
}

function sale_view(saletotal,page,s,type)
{
	message_cls();
	var f=parent.wog_view.document;
	f.write('<form action="wog_etc.php" method="get" name="pageform" target="mission">');
	pagesplit(saletotal,page);
	f.write('<input type="hidden" name="page" value="1">');
	f.write('<input type="hidden" name="type" value="'+type+'">');
	f.write('<input type="hidden" name="f" value="sale">');	
	f.write('<input type="hidden" name="act" value="view">');
	f.write('</form>');
	f.write('<form action="wog_act.php" method="post" target="mission" name=f1>');
	f.write(temp_table1);
	f.write('<tr><td colspan="13"><a href=javascript:parent.sel_type("0");>武器</a> <a href=javascript:parent.sel_type("1");>頭部</a>  <a href=javascript:parent.sel_type("2");>身體</a> <a href=javascript:parent.sel_type("3");>手套</a> <a href=javascript:parent.sel_type("4");>鞋子</a> <a href=javascript:parent.sel_type("5");>道具</a> <a href=javascript:parent.sel_type("6");>寵物</a></td></tr>');
	f.write('<tr><td colspan="13">拍賣商品</td></tr>');
	if(type < 6)
	{	
		f.write('<tr><td></td><td>拍賣者</td><td>商品</td><td>物攻</td><td>魔攻</td><td>物防</td><td>魔防</td><td>速度</td><td>職業</td><td>能力限制</td><td>金額</td><td>原價</td><td>剩餘日</td></tr>');
		if(s!="")
		{
			var s1=s.split(";");
			for(var i=0;i<s1.length;i++)
			{
				var s2=s1[i].split(",");
				var now_date=new Date();
				var sale_day=Math.ceil((s2[13]-(now_date.getTime()/1000))/(60*60*24));
				f.write('<tr><td><input type="radio" name="s_id" value="'+s2[11]+'"></td><td>'+s2[0]+'</td><td>'+s2[1]+'</td><td>'+s2[2]+'</td><td>'+s2[3]+'</td><td>'+s2[4]+'</td><td>'+s2[5]+'</td><td>'+s2[6]+'</td><td>'+s2[14]+'</td><td>力:'+s2[7]+' 速:'+s2[8]+' 智:'+s2[9]+'</td><td>'+s2[12]+'</td><td>'+s2[10]+'</td><td>'+sale_day+'</td></tr>');
			}
		}
		f.write('<input type="hidden" name="stype" value="0">');
	}else
	{
		f.write('<tr><td>拍賣者</td><td>商品</td><td>AT</td><td>MT</td><td>DEF</td><td>個性</td><td>年紀</td><td>出擊值</td><td>金額</td><td>剩餘日</td><td></td></tr>');
		if(s!="")
		{
			var s1=s.split(";");
			for(var i=0;i<s1.length;i++)
			{
				var s2=s1[i].split(",");
				var now_date=new Date();
				var sale_day=Math.ceil((s2[11]-(now_date.getTime()/1000))/(60*60*24));
				f.write('<tr><td>'+s2[0]+'</td><td>'+s2[2]+'-'+s2[3]+'</td><td>'+s2[4]+'</td><td>'+s2[5]+'</td><td>'+s2[6]+'</td><td>'+pet_type(s2[7])+'</td><td>'+s2[8]+'</td><td>'+s2[9]+'</td><td>'+s2[10]+'</td><td>'+sale_day+'</td><td><input type="radio" name="s_id" value="'+s2[1]+'"></td></tr>');
			}
		}	
		f.write('<input type="hidden" name="stype" value="1">');
	}
	f.write('<tr><td colspan="13"><input type="submit" value="購買"></td></tr>');
	f.write(temp_table2);
	f.write('<input type="hidden" name="f" value="sale">');
	f.write('<input type="hidden" name="act" value="buy">');
	f.write('</form>');
}

//###### 分頁 begin #####
function pagesplit(saletotal,page)
{
	var view_name=parent.wog_view;
	view_name.document.write(temp_table1);
	view_name.document.write('<tr><td>');
	var totalpage=0;
	if(saletotal%8==0)
	{
		totalpage=saletotal/8;
	}else
	{
		totalpage=(saletotal/8)+1;
	}
	for(var i=1;i<=totalpage;i++)
	{
		if(i==page)
		{
			view_name.document.write(' '+i+' ');
		}else
		{
			view_name.document.write(' <a href=javascript:parent.page_jump("'+i+'")>'+i+'</a> ');
		}
	}
	view_name.document.write('</td></tr>');
	view_name.document.write(temp_table2);
}
function page_jump(s)
{
	wog_view.document.pageform.page.value=s;
	wog_view.document.pageform.submit();
}
function sel_type(s)
{
	wog_view.document.pageform.type.value=s;
	wog_view.document.pageform.submit();
}
//#### view begin ####
function login_view(p_win,p_lost,p_img_set,i_img,p_name,p_sex,ch_name,p_s,p_lv,p_exp,p_nextexp,p_money,p_hp,p_hpmax,p_str,p_smart,p_agl,p_life,p_vit,p_au,p_be,p_at,p_mat,p_df,p_mdf,a_name,body_name,head_name,hand_name,foot_name,item_name,p_url,p_homename,s_ch_name,p_sat_name,p_place,p_birth,p_cdate,bbsid)
{
	message_cls();
	setup_name(p_name);
	setup_sat_name(p_sat_name);
	setup_bbsid(bbsid);
	d_ch_name=ch_name;
	d_s_ch_name=s_ch_name;
	d_a_name=a_name;
	d_body_name=body_name;
	d_head_name=head_name;
	d_hand_name=hand_name;
	d_foot_name=foot_name;
	d_item_name=item_name;
	d_p_url=p_url;
	d_p_homename=p_homename;
	my_birth=birth[p_birth];
	my_age=p_cdate;
	status_view(p_win,p_lost,p_img_set,i_img,p_sex,p_s,p_lv,p_exp,p_nextexp,p_money,p_hp,p_hpmax,p_str,p_smart,p_agl,p_life,p_vit,p_au,p_be,p_at,p_mat,p_df,p_mdf,p_place);
	foot_fire();
}
function show_status(p_win,p_lost,p_img_set,i_img,p_sex,p_s,p_lv,p_exp,p_nextexp,p_money,p_hp,p_hpmax,p_str,p_smart,p_agl,p_life,p_vit,p_au,p_be,p_at,p_mat,p_df,p_mdf,p_place)
{
	message_cls();
	status_view(p_win,p_lost,p_img_set,i_img,p_sex,p_s,p_lv,p_exp,p_nextexp,p_money,p_hp,p_hpmax,p_str,p_smart,p_agl,p_life,p_vit,p_au,p_be,p_at,p_mat,p_df,p_mdf,p_place);
}
/*
function systeam_view2(p_win,p_lost,i_img,p_name,p_sex,ch_name,p_s,p_lv,p_exp,p_nextexp,p_money,p_hp,p_hpmax,p_str,p_smart,p_agl,p_life,p_au,p_be,p_at,p_mat,p_df,p_mdf,a_name,d_name,e_name,dd_name,c_name,item_name,p_url,p_homename,s_ch_name,p_sat_name)
{
	message_cls();
	status_view2(p_win,p_lost,i_img,p_name,p_sex,ch_name,p_s,p_lv,p_exp,p_nextexp,p_money,p_hp,p_hpmax,p_str,p_smart,p_agl,p_life,p_au,p_be,p_at,p_mat,p_df,p_mdf,a_name,d_name,e_name,dd_name,c_name,item_name,p_url,p_homename,s_ch_name);
}
*/
function well_view(p_win,p_lost,p_img_set,i_img,p_name,p_sex,ch_name,p_s,p_lv,p_exp,p_nextexp,p_money,p_hp,p_hpmax,p_str,p_smart,p_agl,p_life,p_vit,p_au,p_be,p_at,p_mat,p_df,p_mdf,a_name,d_name,e_name,dd_name,c_name,item_name,p_place,p_birth,p_cdate,del_day,f_time,p_url,p_homename,s_ch_name,win_num,cp_mmoney,a_win)
{
	message_cls();
	var f=parent.wog_view.document;
	f.write('<table width="100%" border="0" cellspacing="0" cellpadding="0">');
	f.write('<tr>');
	f.write('<td  width="63%" valign="top">');
	status_view2(p_win,p_lost,p_img_set,i_img,p_name,p_sex,ch_name,p_s,p_lv,p_exp,p_nextexp,p_money,p_hp,p_hpmax,p_str,p_smart,p_agl,p_life,p_vit,p_au,p_be,p_at,p_mat,p_df,p_mdf,a_name,d_name,e_name,dd_name,c_name,item_name,p_place,p_birth,p_cdate,p_url,p_homename,s_ch_name,win_num);
	f.write('</td>');
	f.write('<td valign="top" class="b1">');
	chara_make(del_day,f_time);
	f.write('</td>');
	f.write('</tr>');
	f.write('</table>');
	setup_jmmoney(cp_mmoney);
}

function cp_view(p_win,p_lost,p_img_set,i_img,p_name,p_sex,ch_name,p_s,p_lv,p_exp,p_nextexp,p_money,p_hp,p_hpmax,p_str,p_smart,p_agl,p_life,p_vit,p_au,p_be,p_at,p_mat,p_df,p_mdf,a_name,d_name,e_name,dd_name,c_name,item_name,p_place,p_birth,p_cdate,p_url,p_homename,s_ch_name,win_num,a_win)
{
	var cp_name=parent.wog_view;
	message_cls();
	status_view2(p_win,p_lost,p_img_set,i_img,p_name,p_sex,ch_name,p_s,p_lv,p_exp,p_nextexp,p_money,p_hp,p_hpmax,p_str,p_smart,p_agl,p_life,p_vit,p_au,p_be,p_at,p_mat,p_df,p_mdf,a_name,d_name,e_name,dd_name,c_name,item_name,p_place,p_birth,p_cdate,p_url,p_homename,s_ch_name,win_num);
}

function a_view(a_win)
{
	var view_name=parent.wog_view;
	view_name.document.write('<tr><td width="100%" colspan="2" valign="top">比武大會前三名</td></tr>');
	view_name.document.write('<tr><td width="100%" colspan="2" valign="top">');
	var s1=a_win.split(";");
	var temp_s="";
	for(var i=0;i<s1.length;i++)
	{	
		var s2=s1[i].split(",");
		temp_s+=' | '+s2[0]+' 連勝 <font color=red>'+s2[1]+'</font> 人';
	}
	temp_s=temp_s.substr(3,temp_s.length);
	view_name.document.write(temp_s+'</td></tr>');
}

function status_view(p_win,p_lost,p_img_set,i_img,p_sex,p_s,p_lv,p_exp,p_nextexp,p_money,p_hp,p_hpmax,p_str,p_smart,p_agl,p_life,p_vit,p_au,p_be,p_at,p_mat,p_df,p_mdf,p_place)
{
	var f=parent.wog_view.document;
	var p_img="";
	if(p_img_set==1)
	{
		p_img=i_img;
	}else
	{
		p_img=img+i_img+".gif";
	}
	f.write(temp_table1);
	f.write('<tr><td colspan="5"  >WIN '+p_win+' / LOST '+p_lost+'</td></tr>')
	f.write('<tr><td  >英雄檔案</td><td colspan="4"  ><a href="'+d_p_url+'" target="_blank">'+d_p_homename+'</a></td></tr>')
	f.write('<tr><td  rowspan="8" >'+p_group+'<br><img src="'+p_img+'" border="0" ><br>')
	if((p_win+p_lost)==0 || p_win==0)
	{
		f.write('獲勝率:<b>0</b>')
	}else
	{
		f.write('獲勝率:<b>'+Math.floor((p_win/(p_win+p_lost))*100)+'%</b>');
		if(d_s_ch_name != '')
		{
			f.write('<br>'+d_s_ch_name+'奧義');
		}
	}
	f.write('</td>');
	var sex="";
	(p_sex=="1")?sex="男":sex="女";
	f.write('<td  >暱稱</td><td ><b>'+p_name+'</b></td><td  >性別</td><td ><b>'+sex+' '+my_age+'歲</b></td></tr>')
	p_s=s_status(p_s);
	var p_strf=get_f(p_str,4500);
	var p_smartf=get_f(p_smart,4500);
	var p_aglf=get_f(p_agl,4500);
	var p_lifef=get_f(p_life,4500);
	var p_auf=get_f(p_au,4500);
	var p_bef=get_f(p_be,4500);
	var p_vitf=get_f(p_vit,4500);
	var p_atf=get_f(p_at,7500);
	var p_matf=get_f(p_mat,7500);
	var p_dff=get_f(p_df,7500);
	var p_mdff=get_f(p_mdf,7500);
	f.write('<tr><td  >職業</td><td ><b>'+d_ch_name+'</b></td><td  >屬性</td><td ><b>'+p_s+'</b></td></tr>')
	f.write('<tr><td  >等級</td><td ><b>'+p_lv+'</b></td><td  >經驗值</td><td ><b>'+p_exp+'/'+p_nextexp+'</b></td></tr>')
	f.write('<tr><td  >金錢</td><td ><b>'+p_money+'</b></td><td  >HP</td><td ><b>'+p_hp+'/'+p_hpmax+'</b></td></tr>')
	f.write('<tr><td  >冒險地</td><td ><b>'+sec[p_place]+'</b></td><td  >出生地</td><td ><b>'+my_birth+'</b></td></tr>')

	f.write('<tr><td  >武器</td><td ><b>'+d_a_name+'</b></td><td  >身體</td><td ><b>'+d_body_name+'</b></td></tr>')
	f.write('<tr><td  >手部</td><td ><b>'+d_hand_name+'</b></td><td  >頭部</td><td ><b>'+d_head_name+'</b></td></tr>')
	f.write('<tr><td  >腳部</td><td ><b>'+d_foot_name+'</b></td><td  >道具</td><td ><b>'+d_item_name+'</b></td></tr>')
	f.write(temp_table2);
	f.write(hr);
	f.write(temp_table1);
	f.write('<tr><td >力量</td><td class="b1" ><img src="'+img+'bar/bxg.gif" width="'+p_strf+'%" height="9"><b>'+p_str+'</b></td><td  >智力</td><td class="b1" ><img src="'+img+'bar/bxg.gif" width="'+p_smartf+'%" height="9"><b>'+p_smart+'</b></td></tr>')
	f.write('<tr><td >敏捷</td><td class="b1" ><img src="'+img+'bar/bxg.gif" width="'+p_aglf+'%" height="9"><b>'+p_agl+'</b></td><td  >生命</td><td class="b1" ><img src="'+img+'bar/bxg.gif" width="'+p_lifef+'%" height="9"><b>'+p_life+'</b></td></tr>')
	f.write('<tr><td >魅力</td><td class="b1" ><img src="'+img+'bar/bxg.gif" width="'+p_auf+'%" height="9"><b>'+p_au+'</b></td><td  >信仰</td><td class="b1" ><img src="'+img+'bar/bxg.gif" width="'+p_bef+'%" height="9"><b>'+p_be+'</b></td></tr>')
	f.write('<tr><td >體質</td><td class="b1" ><img src="'+img+'bar/bxg.gif" width="'+p_vitf+'%" height="9"><b>'+p_vit+'</b></td><td  >--</td><td align="center" class="b1" >---</td></tr>')
	f.write('<tr><td >物攻</td><td class="b1" ><img src="'+img+'bar/bmg.gif" width="'+p_atf+'%" height="9"><b>'+p_at+'</b></td><td  >魔攻</td><td class="b1" ><img src="'+img+'bar/bmg.gif" width="'+p_matf+'%" height="9"><b>'+p_mat+'</b></td></tr>')
	f.write('<tr><td >物防</td><td class="b1" ><img src="'+img+'bar/bmg.gif" width="'+p_dff+'%" height="9"><b>'+p_df+'</b></td><td  >魔防</td><td class="b1" ><img src="'+img+'bar/bmg.gif" width="'+p_mdff+'%" height="9"><b>'+p_mdf+'</b></td></tr>')
	f.write(temp_table2);
}

function status_view2(p_win,p_lost,p_img_set,i_img,p_name,p_sex,ch_name,p_s,p_lv,p_exp,p_nextexp,p_money,p_hp,p_hpmax,p_str,p_smart,p_agl,p_life,p_vit,p_au,p_be,p_at,p_mat,p_df,p_mdf,a_name,d_name,e_name,dd_name,c_name,item_name,p_place,p_birth,p_cdate,p_url,p_homename,s_ch_name,win_num)
{
	var f=parent.wog_view.document;
	var p_img="";
	if(p_img_set==1)
	{
		p_img=i_img;
	}else
	{
		p_img=img+i_img+".gif";
	}
	f.write(temp_table1);
	f.write('<tr><td colspan="5"  >WIN '+p_win+' / LOST '+p_lost+'</td></tr>')
	f.write('<tr><td  >英雄檔案</td><td colspan="4"  ><a href="'+p_url+'" target="_blank">'+p_homename+'</a></td></tr>')
	f.write('<tr><td   rowspan="8" >'+p_group+'<br><img src="'+p_img+'" border="0" ><br>')
	if((p_win+p_lost)==0 || p_win==0)
	{
		f.write('獲勝率:<b>0</b>')
	}else
	{
		f.write('獲勝率:<b>'+Math.floor((p_win/(p_win+p_lost))*100)+'%</b>');
		if(s_ch_name != '')
		{
			f.write('<br>'+s_ch_name+'奧義');
		}
	}
	f.write('</td>');
	var sex="";
	(p_sex=="1")?sex="男":sex="女";
	f.write('<td  >暱稱</td><td ><b>'+p_name+'</b></td><td  >性別</td><td ><b>'+sex+' '+p_cdate+'歲</b></td></tr>')
	p_s=s_status(p_s);
	var p_strf=get_f(p_str,4500);
	var p_smartf=get_f(p_smart,4500);
	var p_aglf=get_f(p_agl,4500);
	var p_lifef=get_f(p_life,4500);
	var p_auf=get_f(p_au,4500);
	var p_bef=get_f(p_be,4500);
	var p_vitf=get_f(p_vit,4500);
	var p_atf=get_f(p_at,7500);
	var p_matf=get_f(p_mat,7500);
	var p_dff=get_f(p_df,7500);
	var p_mdff=get_f(p_mdf,7500);
	f.write('<tr><td  >職業</td><td ><b>'+ch_name+'</b></td><td  >屬性</td><td ><b>'+p_s+'</b></td></tr>')
	f.write('<tr><td  >等級</td><td ><b>'+p_lv+'</b></td><td  >經驗值</td><td ><b>'+p_exp+'/'+p_nextexp+'</b></td></tr>')
	f.write('<tr><td  >金錢</td><td ><b>'+p_money+'</b></td><td  >HP</td><td ><b>'+p_hp+'/'+p_hpmax+'</b></td></tr>')
	f.write('<tr><td  >冒險地</td><td  ><b>'+sec[p_place]+'</b></td><td  >出生地</td><td  ><b>'+birth[p_birth]+'</b></td></tr>')
	f.write('<tr><td  >武器</td><td ><b>'+a_name+'</b></td><td  >身體</td><td ><b>'+d_name+'</b></td></tr>')
	f.write('<tr><td  >手部</td><td ><b>'+dd_name+'</b></td><td  >頭部</td><td ><b>'+e_name+'</b></td></tr>')
	f.write('<tr><td  >腳部</td><td ><b>'+c_name+'</b></td><td  >道具</td><td ><b>'+item_name+'</b></td></tr>')
	if(win_num != undefined)
	{
		f.write('<tr><td  >連勝紀錄</td><td colspan="4"  >'+win_num+' 連勝中</td></tr>')	
	}

	f.write(temp_table2);
	f.write(hr);
	f.write(temp_table1);

	f.write('<tr><td  >力量</td><td class="b1"><img src="'+img+'bar/bxg.gif" width="'+p_strf+'%" height="9"><b>'+p_str+'</b></td><td  >智力</td><td class="b1"><img src="'+img+'bar/bxg.gif" width="'+p_smartf+'%" height="9"><b>'+p_smart+'</b></td></tr>')
	f.write('<tr><td  >敏捷</td><td class="b1"><img src="'+img+'bar/bxg.gif" width="'+p_aglf+'%" height="9"><b>'+p_agl+'</b></td><td  >生命</td><td class="b1"><img src="'+img+'bar/bxg.gif" width="'+p_lifef+'%" height="9"><b>'+p_life+'</b></td></tr>')
	f.write('<tr><td  >魅力</td><td class="b1"><img src="'+img+'bar/bxg.gif" width="'+p_auf+'%" height="9"><b>'+p_au+'</b></td><td  >信仰</td><td class="b1"><img src="'+img+'bar/bxg.gif" width="'+p_bef+'%" height="9"><b>'+p_be+'</b></td></tr>')
	f.write('<tr><td  >體質</td><td class="b1"><img src="'+img+'bar/bxg.gif" width="'+p_vitf+'%" height="9"><b>'+p_vit+'</b></td><td  >--</td><td class="b1">---</td></tr>')
	f.write('<tr><td  >物攻</td><td class="b1"><img src="'+img+'bar/bmg.gif" width="'+p_atf+'%" height="9"><b>'+p_at+'</b></td><td  >魔攻</td><td class="b1"><img src="'+img+'bar/bmg.gif" width="'+p_matf+'%" height="9"><b>'+p_mat+'</b></td></tr>')
	f.write('<tr><td  >物防</td><td class="b1"><img src="'+img+'bar/bmg.gif" width="'+p_dff+'%" height="9"><b>'+p_df+'</b></td><td  >魔防</td><td class="b1"><img src="'+img+'bar/bmg.gif" width="'+p_mdff+'%" height="9"><b>'+p_mdf+'</b></td></tr>')
	f.write(temp_table2);
}

function no_cp(del_day,f_time)
{
	message_cls();
	var f=parent.wog_view.document;
	f.write('<table border=0 width="100%">');
	f.write('<tr>');
	f.write('<td valign="top">');
	chara_make(del_day,f_time);
	f.write('</td>');
	f.write('</tr>');
	f.write('</table>');
}

function s_status(s)
{
	switch(s)
	{
		case "1":
		 s="地";
		break;
		case "2":
		 s="水";
		break;
		case "3":
		 s="火";
		break;
		case "4":
		 s="木";
		break;
		case "5":
		 s="風";
		break;
		case "6":
		 s="毒";
		break;
		case "7":
		 s="無";
		break;
	}
	return s;
}

function get_f(p,s)
{
	p=(p/4500)*100;
	if(p>100){p=100;}
	return p;
}

function chara_make(del_day,f_time)
{
	var f=parent.wog_view.document;
	f.write('<form action="wog_act.php" method="POST" target="wog_view">');
	f.write('<center>WOG-遊戲方式 <font color="#FF0000">看玩遊戲說明再創造角色</font></center>');
	f.write('<OL>');
	f.write('<LI>首先必須先加入論壇會員以及登入論壇才能創造角色。');
	f.write('<LI>點選「角色作成」按鈕，作成新角色。');
	f.write('<LI>角色作成之後，便可利用設定的帳號和密碼進入遊戲。');
	f.write('<LI>角色作成完成後，從頁面右上角登入，即可進入你個人的專屬舞台。');
	f.write('<LI>在個人專屬舞台裡，你可以進行動作選擇。');
	f.write('<LI>玩家可利用限定的加分點數增加自己的能力值。(能力值的設定和人物的今後的職業有相當大的關聯，請慎重考量!!)');
	f.write('<LI>每人限制最多只能創造<FONT COLOR="#FF0000"><b>3</b></FONT>位角色。');
	f.write('<LI>每場戰役結束後，必須經過<FONT COLOR="#FF0000"><b>'+f_time+'</b></FONT>秒才可以再進行下一場戰役!!');
	f.write('<INPUT TYPE="hidden" NAME="act" VALUE="make">');
	f.write('<INPUT TYPE="hidden" NAME="f" VALUE="chara">');
	f.write('<center><INPUT TYPE="submit" VALUE=" 創造新角色 " ></form></center>');
	f.write('</OL>');
}

function king_view(sname,s)
{
	var view_name=parent.wog_view;
	view_name.document.write(temp_table1);
	view_name.document.write('<tr><td height="0" colspan="3" rowspan="0" >'+sname+'</td></tr>')
	var s1=s.split(";");
	for(var i=0;i<s1.length;i++)
	{	
		var s2=s1[i].split(",");
		var p_img_url=s2[0];
		if(p_img_url.indexOf("http") == -1)
		{
			p_img_url='<img src="'+img+p_img_url+'.gif" border="0">';
		}else
		{
			p_img_url='<img src="'+p_img_url+'" border="0">';
		}

		view_name.document.write('<tr><td  width="110">'+p_img_url+'</td><td >'+s2[1]+'</td><td >'+s2[2]+'</td></tr>');
	}
	view_name.document.write(temp_table2);
}

function system_view(s)
{
	message_cls();
	var view_name=parent.wog_view;
	view_name.document.write(temp_table1);
	view_name.document.write('<tr><td>內容</td><td>發生時間</td></tr>');
	if(s!="")
	{
		var s1=s.split(";");
		for(var i=0;i<s1.length;i++)
		{	
			var s2=s1[i].split(",");
			view_name.document.write('<tr><td>'+s2[0]+'</td><td>'+s2[1]+'</td></tr>');
		}
	}else
	{
		view_name.document.write('<tr><td colspan="8" >尚未發生任何事件</td></tr>');	
	}
	view_name.document.write(temp_table2);
}

//##### bank #####
function bank(a,b)
{
	message_cls();
	var f=parent.wog_view.document;
	f.write(temp_table1);
	f.write('<tr><td  >身上現金 : '+a+'</td><td >銀行存款 : '+b+'</td></tr>')
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write('<tr><td  >金額 <input type="text" name="money" size="5"></td><td ><input type="submit" value="存款"></td></tr>')
	f.write('<input type="hidden" name="f" value="bank">');
	f.write('<input type="hidden" name="act" value="save">');
	f.write('</form>');
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write('<tr><td  >金額 <input type="text" name="money" size="5"></td><td ><input type="submit" value="提款"></td></tr>')
	f.write('<input type="hidden" name="f" value="bank">');
	f.write('<input type="hidden" name="act" value="get">');
	f.write('</form>');
	f.write('<form name=f1>');
	f.write('<tr><td  >金額 <input type="text" name="money" size="5"> ,對像帳號 <input type="text" name="pay_id" size="6"></td><td ><input type="button" value="轉帳" onclick="parent.foot_trun(\'bank\',\'pay\',document.f1.pay_id.value,document.f1.money.value,null)"></td></tr>')
	f.write('</form>');
	f.write(temp_table2);
}

//#### arm begin ####
function arm_view(a,d,temp_id)
{
	var f=parent.wog_view.document;
	vData=d;
	message_cls();
	f.write('<form action="wog_act.php" method="post" target="mission" name=f1 >');
	f.write(temp_table1);
	f.write('<tr><td>裝備/轉移</td><td>物攻</td><td>魔攻</td><td>物防</td><td>魔防</td><td>速度</td><td>職業</td><td>屬性</td><td>能力限制</td><td>名稱</td><td>價格</td><td>販賣/拍賣</td></tr>');
	var s1=a.split(";");
	for(var i=0;i<s1.length;i++)
	{	
		var s2=s1[i].split(",");
		var temps=srhCount(s2[0]);
		var s3=null;
		if(tmpNum != "")
		{
			s3=tmpNum.split(",");
		}
		for(var j=0;j<temps;j++)
		{
			if(s3!=null)
			{
				var temp_num="*"+s3[j];
			}else
			{
				var temp_num="";
			}
			var arm_view_color="";
			if(s2[12]=="1"){arm_view_color="bgcolor="+nosend;}
			f.write('<tr '+arm_view_color+'><td><input type="radio" name="adds" value="'+s2[0]+'"></td><td>'+s2[6]+'</td><td>'+s2[7]+'</td><td>'+s2[1]+'</td><td>'+s2[2]+'</td><td>'+s2[3]+'</td><td>'+s2[11]+'</td><td>'+s_status(s2[13])+'</td><td>力:'+s2[8]+' 速:'+s2[9]+' 智:'+s2[10]+'</td><td>'+s2[5]+temp_num+'</td><td>'+s2[4]+'</td><td><input type="radio" name="items" value="'+s2[0]+','+s2[5]+'"></td></tr>');
		}
	}
	f.write('<tr><td colspan="12" ><input type="submit" value="裝備"> <input type="button" value="轉移" onClick="parent.foot_trun(\'arm\',\'move\',document.f1.pay_id.value,document.f1.item_num.value,document.f1.adds)"> <input type="button" value="販賣" onClick="parent.foot_trun(\'arm\',\'sale\',document.f1.pay_id.value,document.f1.item_num.value,document.f1.items)"> <input type="button" value="拍賣" onClick="parent.sale_item(document.f1.items)"></td></tr>');
	f.write('<tr><td colspan="12" >請選擇數量:<select name="item_num">');
	for(var j=1;j<10;j++)
	{
		f.write('<option value="'+j+'" >'+j+'</option>');
	}
	f.write('</select>(使用轉移及販賣記得選擇道具數量)</td></tr>');
	f.write('<tr><td colspan="12" >欲轉移需輸入對方遊戲的帳號 <input type="text" name="pay_id" size="16"></td></tr>');
	f.write(temp_table2);
	f.write('<input type="hidden" name="f" value="arm">');	
	f.write('<input type="hidden" name="act" value="setup">');
//	f.write('<input type="hidden" name="temp_id" value="'+temp_id+'">');
	f.write('</form>');
}

function arm_setup(a,b)
{
	switch(a)
	{
		case "a_id":
			d_a_name=b;
			return;
			break;
		case "d_head_id":
			d_head_name=b;
			return;
			break;
		case "d_body_id":
			d_body_name=b;
			return;
			break;
		case "d_hand_id":
			d_hand_name=b;
			return;
			break;
		case "d_foot_id":
			d_foot_name=b;
			return;
			break;
		case "d_item_id":
			d_item_name=b;
			return;
			break;
	}
	return;
}
function arm_end(s)
{
	var view_name=parent.wog_view;
	message_cls();
	view_name.document.write(temp_table1);
	if(s==1)
	{
		view_name.document.write('<tr><td>裝備完成</td></tr>')
	}
	if(s==2)
	{
		view_name.document.write('<tr><td>轉移完成</td></tr>')
	}
	view_name.document.write(temp_table2);
}
function srhCount(srhStr)
{
	var tmpData=vData.split(",");
	var tmpResult=0;
	tmpNum="";
	var tempvdata="";
	for(var i=0;i<tmpData.length;i++)
	{
		if(tmpData[i].indexOf("*") > 0)
		{
			var s1=tmpData[i].split("*");
			if(s1[0]==srhStr)
			{
				tmpResult=tmpResult+1;
				tmpNum=tmpNum+","+s1[1];
			}else
			{
				tempvdata=tempvdata+","+tmpData[i];
			}
		}else
		{
			if(tmpData[i]==srhStr)
			{
				tmpResult=tmpResult+1;
			}else
			{
				tempvdata=tempvdata+","+tmpData[i];
			}		
		}
	}
	vData=tempvdata.substr(1,tempvdata.length);
	if(tmpNum != "")
	{
		tmpNum=tmpNum.substr(1,tmpNum.length);
	}
	return tmpResult;
}

//##########----------syn_system_start----------########## 
function syn_view(a,d) 
{ 
	var f=parent.wog_view.document;
	vData=d; 
	message_cls();
	f.write('<form action="wog_act.php" method="post" target="mission" name=f1 >'); 
	f.write(temp_table1); 
	f.write('<tr><td>合成選擇</td><td>物理攻擊力</td><td>魔力攻擊力</td><td>物理防禦力</td><td>魔力防禦力</td><td>提升速度</td><td>名稱</td><td>價格</td></tr>'); 
	var s1=a.split(";"); 
	for(var i=0;i<s1.length;i++) 
	{    
		var s2=s1[i].split(","); 
		var temps=srhCount(s2[0]); 
		var s3=null;
		if(tmpNum != "")
		{
			s3=tmpNum.split(",");
		}
		for(var j=0;j<temps;j++) 
		{
			if(s3!=null)
			{
				var temp_num="*"+s3[j];
			}else
			{
				var temp_num="";
			}
			f.write('<tr><td><input type="checkbox" name="syn[]" value="'+s2[0]+'"></td><td>'+s2[6]+'</td><td>'+s2[7]+'</td><td>'+s2[1]+'</td><td>'+s2[2]+'</td><td>'+s2[3]+'</td><td>'+s2[5]+temp_num+'</td><td>'+s2[4]+'</td></tr>'); 
		} 
	} 
	f.write('<tr><td colspan="10" >選擇合成方式：<select name="syn_way">'); 
	var syn_option=new Array(); 
	syn_option[0]="<option value=1 CHECKED>普通合成</option>"; 
	syn_option[1]="<option value=2>隨機合成</option>"; 
//	syn_option[2]="<option value=3>限定合成</option>"; 
	for(var a=0;a<syn_option.length;a++) 
	{ 
		f.write(syn_option[a]); 
	}
	f.write('</select></tr>'); 
	f.write('<tr><td colspan="10" ><input type="submit" value="送入合成爐"></tr>'); 
	f.write(temp_table2); 
	f.write('<input type="hidden" name="f" value="syn">');    
	f.write('<input type="hidden" name="act" value="purify">'); 
	f.write('</form>'); 
} 
function syn_end(s,end) 
{ 
	var f=parent.wog_view.document; 
	message_cls(); 
	f.write(temp_table1); 
	f.write('<tr><td>在合成的途中合成爐突然發出閃閃的白光！<BR><p align=center><font size=7><b>轟隆隆隆隆隆隆隆隆隆隆！</b></p></font>'); 
	var timerID=setTimeout('syn_end_view("'+s+'","'+end+'")',1000); 
	f.write('</td></tr>'+temp_table2+"<br>"); 
} 
function syn_end_view(s,end) 
{ 
	var f=parent.wog_view.document; 
	f.write(temp_table1+'<tr><td>'); 
	if(end==1)//合成成功 
	{f.write('你的眼前出現了一個閃閃發亮的物品，這次的合成似乎是成功了！<br><br>合成結果： <font color=#ffffaf>'+s+'</font> 入手！');} 
	if(end==2)//編號錯誤 
	{f.write('你合出了一團無法辨識的東西，或許是一團垃圾....');} 
	if(end==3)//合成失敗 
	{f.write('你的眼前出現了一團灰燼....。');} 
	if(end==4)//裝備過多 
	{f.write('合成成功！但因為裝備欄已滿，所以裝備掉下被不明人士撿走，請自認倒楣。');}
	f.write('</td></tr>'+temp_table2); 
} 
function syn_view_special(syntotal,page,s,type)
{
	message_cls();
	var f=parent.wog_view.document;
	f.write('<form action="wog_act.php" method="post" name="pageform" target="mission">');
	pagesplit(syntotal,page);
	f.write('<input type="hidden" name="page" value="1">');
	f.write('<input type="hidden" name="type" value="'+type+'">');
	f.write('<input type="hidden" name="f" value="syn">');
	f.write('<input type="hidden" name="act" value="list">');
	f.write('</form>');
	f.write('<form action="wog_act.php" method="post" target="mission" name=f1>');
	f.write(temp_table1);
	f.write('<tr><td colspan="13"><a href=javascript:parent.sel_type("0");>武器</a> <a href=javascript:parent.sel_type("1");>頭部</a>  <a href=javascript:parent.sel_type("2");>身體</a> <a href=javascript:parent.sel_type("3");>手套</a> <a href=javascript:parent.sel_type("4");>鞋子</a> <a href=javascript:parent.sel_type("5");>道具</a></td></tr>');
	f.write('<tr><td colspan="13" class=b1>我是合成大師,專門替冒險者合成一般商店沒有販賣的物品,我的合成是要收費的,每樣物品手續費2000元,但是先提醒合成是有風險的。我的師父愛德華是傳說中的合成天才,能合成稀有物品,目前他四處雲遊冒險,有緣您會遇到他</td></tr>');
	f.write('<tr><td colspan="13">請選擇想製作的物品</td></tr>');
	f.write('<tr><td></td><td>名稱</td><td>物攻</td><td>魔攻</td><td>物防</td><td>魔防</td><td>速度</td><td>職業</td><td>屬性</td><td>能力限制</td><td>限制熟練度</td></tr>');
	if(s!="")
	{
		var s1=s.split(";");
		for(var i=0;i<s1.length;i++)
		{
			var s2=s1[i].split(",");
			var arm_view_color="";
			if(s2[13]=="1"){arm_view_color="bgcolor="+nosend;}
			f.write('<tr '+arm_view_color+'><td><input type="radio" name="syn_id" value="'+s2[9]+'"></td><td>'+s2[0]+'</td><td>'+s2[1]+'</td><td>'+s2[2]+'</td><td>'+s2[3]+'</td><td>'+s2[4]+'</td><td>'+s2[5]+'</td><td>'+s2[10]+'</td><td>'+s_status(s2[11])+'</td><td>力:'+s2[6]+' 速:'+s2[7]+' 智:'+s2[8]+'</td><td>'+job_pro(s2[12])+'%</td></tr>');
		}
	}
	f.write('<tr><td colspan="11"><input type="submit" value="確定"></td></tr>'); 
	f.write(temp_table2);
	f.write('<input type="hidden" name="f" value="syn">');    
	f.write('<input type="hidden" name="act" value="detail">'); 
	f.write('</form>'); 	
}
function syn_detail(s,syn_id,d_name)
{
	message_cls();
	var f=parent.wog_view.document;
	f.write('<form action="wog_act.php" method="post" target="mission" name=f1>');
	f.write(temp_table1);
	f.write('<tr><td >製作'+d_name+'需要下列物品</td></tr>'); 
	f.write('<tr><td >'+s+'</td></tr>'); 
	f.write('<tr><td ><input type="submit" value="確定合成"></td></tr>'); 
	f.write(temp_table2);
	f.write('<input type="hidden" name="f" value="syn">');    
	f.write('<input type="hidden" name="act" value="special">'); 
	f.write('<input type="hidden" name="syn_id" value="'+syn_id+'">');
	f.write('</form>'); 	
}
//##########----------syn_system_end----------##########
function arm_select()
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1);
	f.write('<form method="post" target="mission">');
	f.write('<tr><td><input type="button" value="武器裝具" onClick="parent.act_click(\'arm\',\'view\',\'a_id\')"> <input type="button" value="頭部裝具" onClick="parent.act_click(\'arm\',\'view\',\'d_head_id\')"> <input type="button" value="身體裝具" onClick="parent.act_click(\'arm\',\'view\',\'d_body_id\')"> <input type="button" value="手部裝具" onClick="parent.act_click(\'arm\',\'view\',\'d_hand_id\')"> <input type="button" value="腳部裝具" onClick="parent.act_click(\'arm\',\'view\',\'d_foot_id\')"> <input type="button" value="道具裝具" onClick="parent.act_click(\'arm\',\'view\',\'d_item_id\')"></tr>');
//##########----------syn_system_start----------########## 
	f.write('<tr><td><input type="button" value="武器合成" onClick="parent.act_click(\'syn\',\'view\',\'a_id\')"> <input type="button" value="頭盔合成" onClick="parent.act_click(\'syn\',\'view\',\'d_head_id\')"> <input type="button" value="鎧甲合成" onClick="parent.act_click(\'syn\',\'view\',\'d_body_id\')"> <input type="button" value="護手合成" onClick="parent.act_click(\'syn\',\'view\',\'d_hand_id\')"> <input type="button" value="長靴合成" onClick="parent.act_click(\'syn\',\'view\',\'d_foot_id\')"> <input type="button" value="道具合成" onClick="parent.act_click(\'syn\',\'view\',\'d_item_id\')"></tr>'); 
//##########----------syn_system_end----------##########
	f.write('</form>');
	f.write(temp_table2);
}

//########## online peo begin ###########
function onlinelist(peo)
{
	var f=parent.wog_peo.document;
	message_cls(f,0);
	f.write(online_temp_table1);
	var boy=0;
	var girl=0;
	if(peo!="")
	{
		f.write('<tr bgcolor="#2B4686"><td  >名稱</td><td  >LV</td><td  >PK</td></tr>');
		var s1=peo.split(";");
		for(var temp_p=0;temp_p<sec.length;temp_p++)
		{
			for(var i=0;i<s1.length;i++)
			{	
				var s2=s1[i].split(",");
				if(temp_p==s2[5])
				{
					var fcolor=psex(s2[1]);
					(s2[1]=="1")?boy++:girl++;
					(s2[3]==1)?s2[3]="Y":s2[3]="N";
					f.write('<tr><td ><a href=javascript:parent.yesname("'+s2[0]+'") target="foot" title="'+s2[4]+'"><b><font color="'+fcolor+'">'+s2[0]+'</font></b></a></td><td >'+s2[2]+'</td><td >'+s2[3]+'</td></tr>');
				}
			}
			f.write('<tr><td  bgcolor="#2B4686" colspan="3">↑'+sec[temp_p]+'練功↑</td></tr>');
		}
		f.write('<tr><td  bgcolor="#2B4686" colspan="3"><font color="#66ccff">男生</font> '+boy+' 人</td></tr>');
		f.write('<tr><td  bgcolor="#2B4686" colspan="3"><font color="#ff99cc">女生</font> '+girl+' 人</td></tr>');
		f.write('<tr><td  bgcolor="#2B4686" colspan="3">線上人數 '+s1.length+' 人</td></tr>');
	}else
	{
		f.write('<tr><td colspan="3"  bgcolor="#2B4686">線上人數 0 人</td></tr>');
	}
	f.write(temp_table2);
}

//########## no_online peo begin ###########
function no_onlinelist(peo)
{
	var f=parent.wog_peo.document;
	message_cls(f,0);
	f.write(online_temp_table1);
	f.write('<tr><td colspan="3"  bgcolor="#2B4686">2分鐘後自動更新</td></tr>');
	f.write(temp_table2);
}

function yesname(s)
{
	parent.foot.document.f1.towho.options[0].value=s;
	parent.foot.document.f1.towho.options[0].text=s;
}

function noname() {
	parent.foot.document.f1.towho.options[0].value='';
	parent.foot.document.f1.towho.options[0].text='';
}

function psex(s)
{
	if(s=="1")
	{
		return "#66ccff";
	}else
	{
		return "#ff99cc";
	}
}

//##### ect,job,pk ######
function job_view(s)
{
	message_cls();
	var f=parent.wog_view.document;
	f.write('<form action="wog_act.php" method="post" target="mission" name=f1 >');
	f.write(temp_table1);
	f.write('<tr><td></td><td>名稱</td><td>力量</td><td>智慧</td><td>生命</td><td>體質</td><td>速度</td><td>魅力</td><td>信仰</td> <td>熟練度</td></tr>')
	var s1=s.split(";");
	for(var i=0;i<s1.length;i++)
	{		
		var s2=s1[i].split("|");
		for(var j=0;j<(s2.length-1);j++)
		{
			s2[j]=s2[j].replace(",","-");
		}
		f.write('<tr><td  ><input type="radio" name="job_id" value="'+s2[0]+'"></td><td >'+s2[1]+'</td><td  >'+s2[2]+'</td><td >'+s2[3]+'</td><td >'+s2[4]+'</td><td >'+s2[5]+'</td><td >'+s2[6]+'</td><td>'+s2[7]+'</td><td>'+s2[8]+'</td><td>'+job_pro(s2[9])+'%</td></tr>');
	}
	f.write('<tr><td colspan="10" ><input type="button" value="變更職業" onClick="parent.foot_trun(\'job\',\'setup\',null,null,document.f1.job_id)"> <input type="button" value="裝備奧義" onClick="parent.foot_trun(\'job\',\'get_skill\',null,null,document.f1.job_id)"></td></tr>');
	f.write(temp_table2);
	f.write('</form>');
}
function job_pro(s)
{
	s=parseInt(s);
	s=Math.floor((s/3500)*100);
	return s;
}
function job_end(a,message)
{
	message_cls();
	var f=parent.wog_view.document;
	var s=new Array;
	s[0]="";
	s[1]="刪除成功";
	s[2]="轉職成功";
	s[3]="設定成功";
	s[4]="感謝你使用本銀行";
	s[5]="休息了一晚後,HP回復精神飽滿";
	s[6]="購買完成";
	s[7]="訊息成功發出";
	s[8]="成功取得以及裝備奧義";
	s[9]="開始拍賣";
	s[10]="建立成功";
	s[11]="改變成功";
	s[12]="";
	s[13]="";
	s[14]="手續完成,請等待核可";
	s[15]="手續完成";
	s[16]="過度疲勞寵物死亡";
	s[17]="寵物逃跑";
	s[18]="放生成功";
	s[19]="復活成功,經驗值下降1/5";
	s[20]="任務接受成功";
	s[21]="恭喜完成任務";
	s[22]="取消任務成功";
	if(a==2)
	{
		d_a_name="";d_body_name="";d_head_name="";d_hand_name="";d_foot_name="";d_item_name="";
	}
	f.write(temp_table1);
	f.write('<tr><td >'+s[a]+'!!</td></tr>')
	if(message)
	{
		while(message.indexOf("&n") > 0)
		{
			message=message.replace("&n","<br>");
		}
		f.write('<tr><td class=b1>'+message+'</td></tr>')
	}
	f.write(temp_table2);
}

function pk_view(s,money,win,lost)
{
	message_cls();
	var f=parent.wog_view.document;
	if(s==1)
	{
		var pk_yes="checked";
		var pk_no="";
	}else
	{
		var pk_yes="";
		var pk_no="checked";	
	}
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write(temp_table1);
	f.write('<tr><td >參加PK</td><td >PK金額</td></tr>');
	f.write('<tr><td ><input type="radio" name="pk_setup" value="1" '+pk_yes+'>YES <input type="radio" name="pk_setup" value="0" '+pk_no+'>NO </td><td ><input type="text" name="pk_money" value="'+money+'" size="7" maxlength="7"></td></tr>');
	f.write('<tr><td colspan="2" ><input type="submit" value="確定"></td></tr>');
	f.write('<tr><td colspan="2" >PK戰果紀錄 : WIN '+win+' / LOST '+lost+'</td></tr>');
	f.write('<tr><td colspan="2" >PK金額設定最高100000最低1000,身上現金低於最低金額不能參加PK,系統會自動設定不參加PK賽</td></tr>');
	f.write(temp_table2);
	f.write('<input type="hidden" name="f" value="pk">');	
	f.write('<input type="hidden" name="act" value="setup">');
	f.write('</form>');
}

function id_admin()
{
	message_cls();
	var f=parent.wog_view.document;
	f.write(temp_table1);
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write('<tr><td colspan="2" >角色自殺</td></tr>');
	f.write('<tr><td >帳號</td><td >密碼</td></tr>');
	f.write('<tr><td ><input type="text" size="12" maxlength="12" name="id" ></td><td ><input type="password" size="12" name="password"></td></tr>');
	f.write('<tr><td colspan="2" ><input type="submit" value="送出"></td></tr>');
	f.write('<input type="hidden" name="f" value="chara">');
	f.write('<input type="hidden" name="act" value="kill">');
	f.write('</form>');
	f.write('<form action="wog_etc.php" target="mission">');
	f.write('<tr><td colspan="2" >補發密碼 <input type="text" size="25"  name="email">(請輸入你註冊的EMAIL) <input type="submit" value="送出"></td></tr>');
	f.write('<input type="hidden" name="f" value="password">');
	f.write('</form>');
	f.write(temp_table2);
}

//####### act tool #########
function act_click(f,a,b)
{
	var thisfrom="";
	thisfrom=parent.foot.document.f1;
	thisfrom.act.value=a;
	thisfrom.f.value=f;
	thisfrom.temp_id.value=b;
	thisfrom.action="wog_act.php";
	thisfrom.submit();
}

function foot_trun(a,b,c,d,e)
{
	var thisfrom=parent.foot.document.f1;
	var temp_s="";
	thisfrom.action="wog_act.php";
	thisfrom.temp_id2.value="";
	thisfrom.act.value="";
	thisfrom.f.value="";
	thisfrom.pay_id.value="";
	thisfrom.temp_id.value="";
	thisfrom.act.value=b;
	thisfrom.f.value=a;
	thisfrom.pay_id.value=c;
	thisfrom.temp_id.value=d;
//	alert(thisfrom.temp_id.value);
	if(e!=null)
	{
		if(e.length!=undefined)
		{
			for(var i=0;i<e.length;i++)
			{
				if(e[i].checked==true)
				{
					temp_s+=","+e[i].value;
				}			
			}
			temp_s=temp_s.substr(1,temp_s.length);
		}else
		{
			temp_s=e.value;
		}
		thisfrom.temp_id2.value=temp_s;
	}
	thisfrom.submit();
}

function th_submit(b,s,a)
{
	var thisfrom=b;
	thisfrom.temp_id2.value=s;
	thisfrom.temp_id.value=a;
	thisfrom.submit();
}

var start_time=new Date();
start_time=Date.parse(start_time)/1000;
var pet_start_time=new Date(); 
pet_start_time=Date.parse(pet_start_time)/1000; 

var counts=0;
var x=0;
function CountDown(){
	var now=new Date();
	now=Date.parse(now)/1000;
	x=parseInt(counts-(now-start_time),10);
	if(parent.foot.document.f1){		
		parent.foot.document.f1.ats1.value = "離冒險"+x+"秒";		
	}
	if(x>0){
		timerID=setTimeout("CountDown()", 100);
		parent.foot.document.f1.ats1.disabled=true;
	}else{
		parent.foot.document.f1.ats1.disabled=false;
		parent.foot.document.f1.ats1.value = "開始冒險";
		counts=0;
		x=0;
	}
}
function cd_add(s)
{
	counts=x+s;
	start_time=new Date();
	start_time=Date.parse(start_time)/1000;
	setup_time(start_time);
	window.setTimeout('CountDown()',100);
}
function cd(s)
{
	start_time=new Date();
	start_time=Date.parse(start_time)/1000;
	setup_time(start_time);
	setup_cs(s);
	window.setTimeout('CountDown()',100);
}
function inCountDown(){
	var now=new Date();
	now=Date.parse(now)/1000;
	var x=parseInt(counts-(now-start_time),10);
	if(parent.top_view.document.f1){		
		parent.top_view.document.f1.ppp.value = "請等待"+x+"秒";		
	}
	if(x>0){
		timerID=setTimeout("inCountDown()", 100);
		parent.top_view.document.f1.ppp.disabled=true;
	}else{
		parent.top_view.document.f1.ppp.disabled=false;
		parent.top_view.document.f1.ppp.value = "開始冒險";
	}
}
function incd(s)
{
	alert("線上人數額滿,請稍後進入");
	start_time=new Date();
	start_time=Date.parse(start_time)/1000;
	setup_cs(s);
	window.setTimeout('inCountDown()',100);
}
function pet_CountDown(){
	var now_pet=new Date();
	now_pet=Date.parse(now_pet)/1000;
	var y=parseInt(pet_counts-(now_pet-pet_start_time),10);
	if(parent.foot.document.f1){		
		parent.foot.document.f1.ats2.value = y+"秒";
	}
	if(y>0){
		timerID=setTimeout("pet_CountDown()", 100);
		parent.foot.document.f1.ats2.disabled=true;
	}else{
		parent.foot.document.f1.ats2.disabled=false;
		parent.foot.document.f1.ats2.value = "牧　場";
	}
}
function pet_cd(s)
{
	pet_start_time=new Date();
	pet_start_time=Date.parse(pet_start_time)/1000;
	setup_pet_cs(s);
	window.setTimeout('pet_CountDown()',100);
}
function setup_time(time) {star_timet=time;}
function setup_cs(time) {counts=time;}
function setup_pet_cs(time) {pet_counts=time;}
//##### team  #######
function team_view()
{
//	alert("功能尚未開放");

	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1);
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write('<tr><td><input type="button" value="隊伍列表" onClick="parent.act_click(\'team\',\'list\')"> </td></tr>');
	f.write('<tr><td><input type="button" value="隊員狀態" onClick="parent.act_click(\'team\',\'status\')"></td></tr>');
	f.write('<tr><td><input type="button" value="創立隊伍" onClick="parent.team_creat();"></td></tr>');
	f.write('<tr><td><input type="button" value="離開隊伍" onClick="parent.act_click(\'team\',\'leave\')"></td></tr>');
	f.write('<tr><td><input type="button" value="認領隊員" onClick="parent.act_click(\'team\',\'get_member\')"></td></tr>');
	f.write('</form>');
	f.write(temp_table2);

}
function team_list(saletotal,page,s)
{
	var f=parent.wog_view.document;
	message_cls();
	f.write('<form action="wog_act.php" method="post" name=pageform target="mission">');
	pagesplit(saletotal,page);
	f.write('<input type="hidden" name="page" value="">');	
	f.write('<input type="hidden" name="f" value="team">');
	f.write('<input type="hidden" name="act" value="list">');
	f.write('</form>');
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write(temp_table1);
	if(s!="")
	{
		f.write('<tr><td></td><td>隊長暱稱</td><td>隊長等級</td><td>隊伍名稱</td><td>人數</td></tr>');
		var s1=s.split(";");
		for(var i=0;i<s1.length;i++)
		{	
			var s2=s1[i].split(",");
			f.write('<tr><td ><input type="radio" name="t_id" value="'+s2[0]+'" ></td><td >'+s2[3]+'</td><td >'+s2[4]+'</td><td >'+s2[1]+'</td><td >'+s2[2]+'</td></tr>');
		}
		var dbsts_join="";
		var dbsts_leave="";
		if(t_team!="")
		{
			dbsts_join="disabled";
		}else
		{
			f.write('<input type="hidden" name="f" value="team"><input type="hidden" name="act" value="join">');
		}
		f.write('<tr><td colspan="5" align="center"><input type="submit" value="加入隊伍"  '+dbsts_join+' ></td></tr>');
	}else
	{
		f.write('<tr><td colspan="4" align="center">目前無隊伍</td></tr>');
	}
	f.write(temp_table2);
	f.write('</form>');
}
function team_creat()
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1);
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write('<tr><td>隊伍名稱 <input type="text" name="t_name" size="16" maxlength="20"> <input type="button" value="決定" onClick="parent.act_click(\'team\',\'creat\',this.form.t_name.value)"> </td></tr>');
	f.write('</form>');
	f.write(temp_table2);
}

function team_status(s,time_line,support,my_id,adm)
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1);
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write(temp_table1);
	f.write('<tr><td>選擇支援</td><td>名稱</td><td>等級</td><td>狀態</td></tr>');
	var s1=s.split(";");
	if(s!="")
	{
		for(var i=0;i<s1.length;i++)
		{	
			var s2=s1[i].split(",");
			var chk="";
			var dis="";
			var dis2="";
			if(s2[0]==support)
			{
				chk="checked";
			}
			if(s2[0]==my_id)
			{
				dis="disabled";
			}
			if(adm=="0")
			{
				dis2="disabled";
			}
			if( (time_line-parseInt(s2[3])) < 600 )
			{
				f.write('<tr><td ><input type="radio" name="p_id" value="'+s2[0]+'" '+chk+' '+dis+'></td><td >'+s2[1]+'</td><td >'+s2[2]+'</td><td >在線</td></tr>');
			}else
			{
				f.write('<tr bgcolor="#474747"><td ><input type="radio" name="p_id" value="'+s2[0]+'" '+chk+' '+dis+'></td><td >'+s2[1]+'</td><td >'+s2[2]+'</td><td >離線</td></tr>');
			}
		}
		f.write('<tr><td colspan="4" align="center"><input type="button" value="支援隊員" onClick="parent.foot_trun(\'team\',\'support\',null,null,this.form.p_id)" > <input type="button" value="不支援" onClick="parent.act_click(\'team\',\'nosupport\')"> <input type="button" value="踢除隊員" onClick="parent.foot_trun(\'team\',\'del\',null,null,this.form.p_id)" '+dis2+'></td></tr>');
	}
	f.write('</form>');
	f.write(temp_table2);
}

function team_join_list(s)
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1);
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write('<tr><td></td><td>內容</td><td>等級</td><td>職業</td></tr>')
	if(s!="")
	{
		var s1=s.split(";");
		for(var i=0;i<s1.length;i++)
		{  
			var s2=s1[i].split(",");
			f.write('<tr><td><input type="radio" name="t_j_id" value="'+s2[0]+'" ></td><td>'+s2[1]+' 提出加入隊伍申請</td><td>'+s2[2]+'</td><td>'+s2[3]+'</td></tr>');
		}
		f.write('<tr><td colspan="4" align="center"><input type="button" value="邀請加入" onClick="parent.foot_trun(\'team\',\'get_save_member\',null,null,this.form.t_j_id)" ></td></tr>');
	}else
	{
		f.write('<tr><td colspan="5" align="center">沒有玩家申請加入隊伍</td></tr>');	
	}
	f.write('</form>');
	f.write(temp_table2);
}

//##### group  #######
function group_view()
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1);
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write('<tr><td><input type="button" value="公會列表" onClick="parent.act_click(\'group\',\'join\')"> </td><td class=b1><--觀看所有公會狀態,加入公會,離開公會</td></tr>');
	f.write('<tr><td><input type="button" value="創立公會" onClick="parent.group_creat();"></td><td class=b1><--創立公會</td></tr>');
	f.write('<tr><td colspan="2">'+hr+'</td></tr>');
	f.write('<tr><td><input type="button" value="會員狀態" onClick="parent.act_click(\'group\',\'p_list\')"> </td><td class=b1><--觀看會員狀態,會員管理<會員專用></td></tr>');
	f.write('<tr><td><input type="button" value="領地狀態" onClick="parent.act_click(\'group\',\'center\')"> </td><td class=b1><--觀看領地狀態,領地管理<會員專用></td></tr>');
	f.write('<tr><td><input type="button" value="會戰狀況" onClick="parent.act_click(\'group\',\'news\')"> </td><td class=b1><--觀看10天內前10次會戰狀況<會員專用></td></tr>');
	f.write('<tr><td><input type="button" value="佈告欄" onClick="parent.act_click(\'group\',\'book\')"> </td><td class=b1><--公會佈告欄<會員專用></td></tr>');
	f.write('<tr><td><input type="button" value="認領會員" onClick="parent.act_click(\'group\',\'get_member\')"></td><td class=b1><--核准入會申請<會長專用></td></tr>');
	f.write('</form>');
	f.write(temp_table2);
}
function group_book_view(temp)
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1);
	if(temp.length<=0)
	{
		f.write('<tr><td>沒有資料</td></tr>');	
	}else
	{
		while(temp.indexOf("&n") > 0)
		{
			temp=temp.replace("&n","<br>");
		}
		f.write('<tr><td>'+temp+'</td></tr>');	
	}	
	f.write(temp_table2);
	f.write(hr);
	f.write(temp_table1);
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write('<tr><td><textarea cols="30" rows="5" name="g_book"></textarea></td></tr>');
	f.write('<tr><td><input type="button" value="確定送出" onClick="parent.act_click(\'group\',\'save_book\',this.form.g_book.value)"></td></tr>');
	f.write('<tr><td><會長專用></td></tr>');
	f.write('</form>');
	f.write(temp_table2);
}

function group_p_act(temp_d,morale,number)
{
	temp_d=' <font color=red><b>'+temp_d+'<b></font>'
	group_view_fight(temp_d,morale,number,p_name,m_name);
}
function group_m_act(temp_d,morale,number)
{
	temp_d=' <font color=red><b>'+temp_d+'<b></font>'
	group_view_fight(temp_d,morale,number,m_name,p_name);
}
function group_exm_act(temp_d,morale,number)
{
	temp_d=' <font color=red><b>'+temp_d+'<b></font>'
	group_view_fight(temp_d,morale,number,'城堡',p_name);
}
function group_exm2_act(temp_d)
{
	temp_d=' <font color=red><b>'+temp_d+'<b></font>'
	var f=parent.wog_view.document;
	f.write(hr);
	f.write(temp_table1+'<tr><td colspan="2" ><font color="#81D8A8">城堡</font>受到 '+temp_d+' 傷害 </td></tr>');
	f.write(temp_table2);
}
function group_view_fight(temp_d,morale,number,f,d)
{
	var ff=parent.wog_view.document;
	(f==p_name)?f='<font color="#89C7F3">'+f+'</font>':f='<font color="#81D8A8">'+f+'</font>';
	(d==p_name)?d='<font color="#89C7F3">'+d+'</font>':d='<font color="#81D8A8">'+d+'</font>';
	ff.write(hr);
	ff.write(temp_table1+'<tr><td colspan="2" >'+f+' 給予 '+d+temp_d+' 傷害 | '+d+' 士氣'+morale+' 兵力'+number+'</td></tr>');
	ff.write(temp_table2);
}
function group_fire_title(a,de_hp,me_s,de_s)
{
	var f=parent.wog_view.document;
	message_cls();
	var p_name=get_name();
	f.write(temp_table1);
	f.write('<tr><td colspan="3">'+s_status(a)+'領-----防禦度 : '+de_hp+'</td></tr>');
	f.write('<tr><td colspan="3">'+hr+'</td></tr>');
	f.write('<tr><td colspan="3">攻擊方</td></tr>');
	var s2=me_s.split(",");
	f.write('<tr><td>名稱</td><td>兵力</td><td>士氣</td></tr>');
	f.write('<tr><td>'+s2[0]+'</td><td>'+s2[1]+'</td><td>'+s2[2]+'</td></tr>');
	f.write('<tr><td colspan="3">'+hr+'</td></tr>');
	if(de_s!="")
	{
		f.write('<tr><td colspan="3">守備方</td></tr>');
		var s2=de_s.split(",");
		setup_mname(s2[0]);
		f.write('<tr><td>名稱</td><td>兵力</td><td>士氣</td></tr>');
		f.write('<tr><td>'+s2[0]+'</td><td>'+s2[1]+'</td><td>'+s2[2]+'</td></tr>');
	}
	f.write(temp_table2);
}
function group_join_list(s)
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1);
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write('<tr><td></td><td>內容</td><td>等級</td><td>職業</td></tr>')
	if(s!="")
	{
		var s1=s.split(";");
		for(var i=0;i<s1.length;i++)
		{  
			var s2=s1[i].split(",");
			f.write('<tr><td><input type="radio" name="g_j_id" value="'+s2[0]+'" ></td><td>'+s2[1]+' 提出加入公會申請</td><td>'+s2[2]+'</td><td>'+s2[3]+'</td></tr>');
		}
		f.write('<tr><td colspan="4" align="center"><input type="button" value="邀請加入" onClick="parent.foot_trun(\'group\',\'get_save_member\',null,null,this.form.g_j_id)" ></td></tr>');
	}else
	{
		f.write('<tr><td colspan="5" align="center">沒有玩家申請加入會員</td></tr>');	
	}
	f.write('</form>');
	f.write(temp_table2);
}

function group_fire_list_peo(s,gs)
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1);
	f.write('<form action="wog_fight.php" method="post" target="mission">');
	f.write('<tr><td>名稱</td><td>士氣</td><td>兵力</td><td>駐守地</td></tr>');
	if(s!="")
	{
		var s1=s.split(";");
		for(var i=0;i<s1.length;i++)
		{
			var s2=s1[i].split(",");
			f.write('<tr><td>'+s2[0]+'</td><td>'+s2[1]+'</td><td>'+s2[2]+'</td><td>'+s_status(s2[3])+'</td></tr>');
		}

	}
	f.write('<tr><td colspan="5" align="center"><select name="to_group" size="1">');
	f.write('<option value="">請選擇敵方公會</option>');
	if(gs!="")
	{
		var s1=gs.split(";");
		for(var i=0;i<s1.length;i++)
		{		
			var s2=s1[i].split(",");
			f.write('<option value='+s2[0]+'>'+s2[1]+'</option>');
		}

	}
	f.write('</select> <input type="radio" name="g_a_type" value="1">地 <input type="radio" name="g_a_type" value="2">水 <input type="radio" name="g_a_type" value="3">火 <input type="radio" name="g_a_type" value="4">木 <input type="radio" name="g_a_type" value="5">風 <input type="radio" name="g_a_type" value="6">毒</td></tr>');
	f.write('<tr><td colspan="5" align="center"><input type="submit" value="戰鼓宣揚~~出擊!!"></td></tr>');
	f.write('<input type="hidden" name="f" value="fire"><input type="hidden" name="temp_id" value="2">');
	f.write('</form>');
	f.write(temp_table2);
}

function group_peolist(s,g_name)
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1);
	f.write('<tr><td colspan="6">'+g_name+'</td></tr>');
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write('<tr><td></td><td>名稱</td><td>士氣</td><td>兵力</td><td>等級</td><td>駐守領土</td></tr>');
	if(s!="")
	{
		var s1=s.split(";");
		for(var i=0;i<s1.length;i++)
		{	
			var s2=s1[i].split(",");
			if(s2[3]=="")
			{s2[3]="0";}
			f.write('<tr><td><input type="radio" name="p_id" value="'+s2[0]+'" ></td><td >'+s2[1]+'</td><td >'+s2[2]+'</td><td >'+s2[3]+'</td><td >'+s2[4]+'</td><td >'+s_status(s2[5])+'領</td></tr>');
		}
		f.write('<tr><td colspan="6"><input type="radio" name="g_a_type" value="7" >取消駐守</td></tr>');
		f.write('<tr><td colspan="6">變更駐守點</td></tr>');
		f.write('<tr><td colspan="6"><input type="radio" name="g_a_type" value="1">地 <input type="radio" name="g_a_type" value="2">水 <input type="radio" name="g_a_type" value="3">火 <input type="radio" name="g_a_type" value="4">木 <input type="radio" name="g_a_type" value="5">風 <input type="radio" name="g_a_type" value="6">毒</td></tr>');
		f.write('<tr><td colspan="6"><input type="checkbox" name="g_del" value="1">取消會員資格</td></tr>');
		f.write('<tr><td colspan="6"><input type="submit" value="確定"><br>只有會長才能改變會員駐守地點以及取消會員資格<br>若會長取消自身的會員資格視同解散公會</td></tr>');
	}
	f.write('<input type="hidden" name="f" value="group">');
	f.write('<input type="hidden" name="act" value="number">');
	f.write('</form>');
	f.write(temp_table2);
}
function group_center(s,g_name,temp_s,fire)
{
	var f=parent.wog_view.document;
	message_cls();
	if(fire==1)
	{
		var yes="checked";
		var no="";
	}else
	{
		var yes="";
		var no="checked";	
	}
	f.write(temp_table1);
	f.write('<tr><td>'+g_name+'</td></tr>');
	f.write(temp_table2);
	f.write(hr);
	f.write(temp_table1);
	f.write('<tr><td colspan="5">領土情況</td></tr>');
	f.write('<tr><td>領土</td><td>總兵力</td><td>平均士氣</td><td>防禦度</td><td>人數</td></tr>');
	if(s!="")
	{
		var s1=s.split(";");
		for(var i=0;i<s1.length;i++)
		{	
			var s2=s1[i].split(",");
			if(s2[1]=="")
			{s2[1]="0";}
			f.write('<tr><td >'+s_status(s2[0])+'領</td><td >'+s2[1]+'</td><td >'+s2[2]+'</td><td >'+s2[3]+'</td><td >'+s2[4]+'</td></tr>');
		}
	}
	f.write(temp_table2);
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write(temp_table1);
	if(temp_s!="")
	{
		var s1=temp_s.split(",");
		f.write(hr);
		f.write('<tr><td colspan="4">駐守領土--'+s_status(s1[0])+'</td></tr>');
		f.write('<tr><td>領土</td><td>兵力</td><td>士氣</td></tr>');
		f.write('<tr><td >'+s_status(s1[0])+'領</td><td >'+s1[1]+'</td><td >'+s1[2]+'</td></tr>');
		f.write('<tr><td colspan="4"><input type="button" value="提升士氣" onClick="parent.act_click(\'group\',\'up_morale\')"><br><input type="button" value="修補城牆" onClick="parent.act_click(\'group\',\'up_hp\')"><br><input type="button" value="補充兵力" onClick="parent.act_click(\'group\',\'up_number\',document.forms[0].number.value)"><select name="number" size="1">');
		for(var i=1;i<=9;i++)
		{
			f.write('<option value='+(1000*i)+'>'+(1000*i)+'</option>');
		}
		f.write('<option value=15000>補滿</option></select></td></tr>');
		f.write('<tr><td colspan="4">提升士氣要100元</td></tr>');
		f.write('<tr><td colspan="4">修補城牆要花費公款1000</td></tr>');
		f.write('<tr><td colspan="4">每補充1兵力要1元,多退少補</td></tr>');
	}
	f.write('<tr><td colspan="4"><input type="button" value="貢獻" onClick="parent.act_click(\'group\',\'up_money\',document.forms[0].g_money.value)"><input type="text" name="g_money" size="10"> 捐獻公款</td></tr>');
	f.write('<tr><td colspan="4"><input type="button" value="開戰設定" onClick="parent.foot_trun(\'group\',\'fire_set\',\'\',\'\',document.forms[0].f_set)"> <input type="radio" name="f_set" value="0" '+no+'>關 <input type="radio" name="f_set" value="1" '+yes+'>開 只有會長才能設定</td></tr>');
	f.write(temp_table2);
	f.write('</form>');
}
function group_creat()
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1);
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write('<tr><td>公會名稱 <input type="text" name="g_name" size="16" maxlength="20"> <input type="button" value="決定" onClick="parent.act_click(\'group\',\'creat\',this.form.g_name.value)"> </td></tr>');
	f.write('<tr><td>創立公會需要 20萬元</td></tr>');
	f.write('</form>');
	f.write(temp_table2);
}
function group_join(saletotal,page,s)
{
	var f=parent.wog_view.document;
	message_cls();
	f.write('<form action="wog_act.php" method="post" name=pageform target="mission">');
	pagesplit(saletotal,page);
	f.write('<input type="hidden" name="page" value="">');	
	f.write('<input type="hidden" name="f" value="group">');	
	f.write('<input type="hidden" name="act" value="join">');
	f.write('</form>');
	f.write(temp_table1);
	f.write('<form action="wog_act.php" method="post" target="mission">');
	if(s!="")
	{
		f.write('<tr><td></td><td>名稱</td><td>兵力</td><td>平均士氣</td><td>總人數</td><td>WIN / LOST</td><td>公款</td><td>會長</td></tr>');
		var s1=s.split(";");
		for(var i=0;i<s1.length;i++)
		{	
			var s2=s1[i].split(",");
			f.write('<tr><td ><input type="radio" name="g_id" value="'+s2[0]+'" ></td><td >'+s2[1]+'</td><td >'+s2[2]+'</td><td >'+s2[3]+'</td><td >'+s2[4]+'</td><td >'+s2[6]+' / '+s2[7]+'</td><td >'+s2[5]+'</td><td>'+s2[8]+'</td></tr>');
		}
		var dbsts_join="";
		var dbsts_leave="";
		if(p_group!="")
		{
			dbsts_join="disabled";
			f.write('<input type="hidden" name="f" value="group"><input type="hidden" name="act" value="del">');
		}else
		{
			dbsts_leave="disabled";
			f.write('<input type="hidden" name="f" value="group"><input type="hidden" name="act" value="add">');
		}
		f.write('<tr><td colspan="8" align="center"><input type="submit" value="加入公會"  '+dbsts_join+' > <input type="submit" value="退出公會"  '+dbsts_leave+' ></td></tr>');
	}else
	{
		f.write('<tr><td colspan="8" align="center">目前無公會</td></tr>');
	}
	f.write('</form>');
	f.write(temp_table2);
}
//##### pet #######
function pet_break()
{
	var f=parent.wog_view.document;
	f.write(temp_table1);
	f.write('<tr><td>捕捉器損壞</td></tr>');
	f.write(temp_table2);
}
function pet_get(s)
{
	var f=parent.wog_view.document;
	f.write(temp_table1);
	f.write('<tr><td>捕捉到 '+s+'</td></tr>');
	f.write(temp_table2);
}
function pet_index(name,mname,id,s,pe_list)
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1);
	f.write('<form action="wog_act.php" method="post" target="mission" name=f1>');
	f.write('<tr bgcolor="'+tr_bgcolor+'"><td>名稱</td><td>AT</td><td>MT</td><td>DEF</td><td>飽腹</td></tr>');
	var s1=s.split(",");
	f.write('<tr><td >'+name+'-'+mname+'</td><td>'+s1[0]+'</td><td>'+s1[1]+'</td><td>'+s1[2]+'</td><td>'+s1[3]+'</td></tr>');
	f.write('<tr bgcolor="'+tr_bgcolor+'"><td>疲勞</td><td>個性</td><td>年紀</td><td>親密度</td><td>出擊值</td></tr>');
	f.write('<tr><td>'+s1[4]+'</td><td>'+pet_type(s1[5])+'</td><td>'+s1[6]+'</td><td>'+s1[7]+'</td><td>'+s1[8]+'</td></tr>');
	f.write('<tr><td colspan="5">狀態：<input type="radio" name="pe_st" value="0" onclick="parent.foot_trun(\'pet\',\'chg_st\','+id+',0);">攜帶 <input type="radio" name="pe_st" value="2" onclick="parent.foot_trun(\'pet\',\'chg_st\','+id+',2);">獸欄</td></tr>');
	f.write('<tr><td colspan="5"><select name="act" ><option value="1" SELECTED>AT修行</option><option value="2" >MT修行</option><option value="3" >DEF修行</option><option value="4" >FI修行</option></select> <input type="button" value="特訓" onclick="parent.foot_trun(\'pet\',\'ac\','+id+',document.f1.act.value);"> <select name="act1" ><option value="1" SELECTED>活力果實</option><option value="2" >香氣果實</option><option value="3" >甜味果實</option><option value="4" >野性果實</option></select> <input type="button" value="餵食" onclick="parent.foot_trun(\'pet\',\'eat\','+id+',document.f1.act1.value);"></td></tr>');
	f.write('<tr><td colspan="5"><input type="text" value="'+name+'" size="20" maxlength="30" name=rename> <input type="button" value="改名" onclick="parent.foot_trun(\'pet\',\'rename\','+id+',document.f1.rename.value);"></td></tr>');
	f.write('<tr><td colspan="5"><input type="text" size="15" name=money> <input type="button" value="拍賣" onclick="parent.foot_trun(\'pet\',\'sale\','+id+',document.f1.money.value);"></td></tr>');
	f.write('<tr><td colspan="5"><input type="button" value="寵物競技場" onclick="parent.pet_fight();"></td></tr>');
	f.write('<tr><td colspan="5">選擇寵物：');
	var s2=pe_list.split(";");
	for(var i=0;i<s2.length;i++)
	{
		var s3=s2[i].split(",");
		f.write(' <a href=javascript:parent.act_click(\'pet\',\'index\',\''+s3[1]+'\')>'+s3[0]+'</a>');
	}
	f.write('</td></tr>');
	f.write('<tr><td colspan="5"><input type="button" value="放生" onclick="parent.pet_leave('+id+');"></td></tr>');
	f.write('<input type="hidden" name="pet_id" value="'+id+'">');
	f.write('</form>');
	f.write(temp_table2);
	if(s1[9]=="0")
	{
		f.f1.pe_st[0].checked=true;
	}else
	{
		f.f1.pe_st[1].checked=true;
	}
}
function pet_fight()
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1);
	f.write('<form action="wog_act.php" method="post" target="mission" name=f1>');
	f.write('<tr><td><input type="radio" name="temp_id2" value="1"></td><td>幼年級組</td><td>限3歲以下寵物參加</td></tr>');
	f.write('<tr><td><input type="radio" name="temp_id2" value="2"></td><td>中年級組</td><td>限4-7歲寵物參加</td></tr>');
	f.write('<tr><td><input type="radio" name="temp_id2" value="3"></td><td>高年級組</td><td>限8-12歲寵物參加</td></tr>');
	f.write('<tr><td><input type="radio" name="temp_id2" value="4"></td><td>老年級組</td><td>限13-18歲寵物參加</td></tr>');
	f.write('<tr><td colspan="3"><input type="radio" name="a_mode" value="1" checked>快速模式  <input type="radio" name="a_mode" value="2" >一般模式</td></tr>');
	f.write('<tr><td colspan="3">押注金額 : <input type="text" name="pay_id" ></td></tr>');
	f.write('<tr><td colspan="3">賠率 1 : 2 | 最小賭注 500 最大賭注 5000</td></tr>');
	f.write('<tr><td colspan="5"><input type="submit" value="開始比賽"></td></tr>');
	f.write('<input type="hidden" name="f" value="pet">');
	f.write('<input type="hidden" name="act" value="fight">');
	f.write('</form>');
	f.write(temp_table2);
}

function pet_fview(p,m)
{
	var f=parent.wog_view.document;
	var p1=p.split(",");
	var m1=m.split(",");
	pet_pname=p1[0]+"-"+p1[1];
	pet_mname=m1[0]+"-"+m1[1];
	message_cls();
	f.write(temp_table1+'<tr ><td colspan="2" >'+pet_pname+'</td><td colspan="2" >'+pet_mname+'</td></tr>');
	f.write('<tr bgcolor="'+tr_bgcolor+'"><td>HP</td><td>個性</td><td>HP</td><td>個性</td></tr>');
	f.write('<tr><td>'+p1[7]+'</td><td>'+pet_type(p1[6])+'</td><td>'+p1[7]+'</td><td>'+pet_type(m1[6])+'</td></tr>');
	f.write('<tr bgcolor="'+tr_bgcolor+'"><td>AT</td><td>MT</td><td>AT</td><td>MT</td></tr>');
	f.write('<tr><td>'+p1[2]+'</td><td>'+p1[3]+'</td><td>'+m1[2]+'</td><td>'+m1[3]+'</td></tr>');
	f.write('<tr bgcolor="'+tr_bgcolor+'"><td>DEF</td><td>出擊值</td><td>DEF</td><td>出擊值</td></tr>');
	f.write('<tr><td>'+p1[4]+'</td><td>'+p1[5]+'</td><td>'+m1[4]+'</td><td>'+m1[5]+'</td></tr>');
	f.write(temp_table2);
}

function pet_fdetial(dmg)
{
	var f=parent.wog_view.document;
	var p1=p.split(",");
	var m1=m.split(",");
	pet_pname=p1[0]+"-"+p1[1];
	pet_mname=m1[0]+"-"+m1[1];
	message_cls();
	f.write(temp_table1+'<tr ><td colspan="2" >'+pet_pname+'</td><td colspan="2" >'+pet_mname+'</td></tr>');
	f.write('<tr bgcolor="'+tr_bgcolor+'"><td>HP</td><td>個性</td><td>HP</td><td>個性</td></tr>');
	f.write('<tr><td>'+p1[6]+'</td><td>'+pet_type(p1[6])+'</td><td>'+m1[6]+'</td><td>'+pet_type(m1[6])+'</td></tr>');
	f.write('<tr bgcolor="'+tr_bgcolor+'"><td>AT</td><td>MT</td><td>AT</td><td>MT</td></tr>');
	f.write('<tr><td>'+p1[2]+'</td><td>'+p1[3]+'</td><td>'+m1[2]+'</td><td>'+m1[3]+'</td></tr>');
	f.write('<tr bgcolor="'+tr_bgcolor+'"><td>DEF</td><td>出擊值</td><td>DEF</td><td>出擊值</td></tr>');
	f.write('<tr><td>'+p1[4]+'</td><td>'+p1[5]+'</td><td>'+m1[4]+'</td><td>'+m1[5]+'</td></tr>');
	f.write(temp_table2);
}

function pet_pact(temp_d,s) 
{	
	temp_d=' <font color=red><b>'+temp_d+'<b></font>'
	pet_view_fight(temp_d,s,pet_pname,pet_mname);
}

function pet_mact(temp_d,s) 
{	
	temp_d=' <font color=red><b>'+temp_d+'<b></font>'
	pet_view_fight(temp_d,s,pet_mname,pet_pname);	
}
function pet_view_fight(temp_d,s,f,d)
{
	var ff=parent.wog_view.document;
	var fstr="";
	(f==pet_pname)?f='<font color="#89C7F3">'+f+'</font>':f='<font color="#81D8A8">'+f+'</font>';
	(d==pet_pname)?d='<font color="#89C7F3">'+d+'</font>':d='<font color="#81D8A8">'+d+'</font>';
	if(s=="1")
	{
		fstr="物理";
	}else if(s=="2")
	{
		fstr="魔力";
	}else if(s=="3")
	{
		fstr="複合";
	}
	ff.write(hr);
	ff.write(temp_table1+'<tr><td colspan="2" >'+f+' 發動'+fstr+'攻擊 給予 '+d+temp_d+' 點傷害</td></tr>');
	ff.write('</table>');
}
function pet_miss_date(f,d)
{	
	var ff=parent.wog_view.document;
	(f==pet_pname)?f='<font color="#89C7F3">'+f+'</font>':f='<font color="#81D8A8">'+f+'</font>';
	var s=new Array;
	s[0]=" 沒有擊中目標";
	s[1]=" 發呆";
	s[2]=" 東張西望";
	s[3]=" 失去鬥志";
	ff.write(hr);
	ff.write(temp_table1+'<tr><td colspan="2" >'+f+s[d]+'</td></tr>');
	ff.write(temp_table2);
}
function pet_end_date(s,en)
{	
	var f=parent.wog_view.document;
	var enstr="";
	if(en=="0")
	{
		enstr="戰敗了!!!";
	}else if(en=="1")
	{
		enstr="獲得了勝利！！";
	}
	f.write(hr);
	f.write(temp_table1+'<tr><td ><b>'+s+' '+enstr+'</b></td></tr>');
	f.write(temp_table2);
}
function pet_leave(id)
{
	if(confirm("確定放生?"))
	{
		foot_trun('pet','leave',id);
	}
}

function pet_detail(at,mt,def,hu,fu,he,fi)
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1);
	f.write('<tr><td>AT</td><td>MT</td><td>DEF</td><td>疲勞</td><td>飽腹</td><td>親密度</td><td>出擊值</td></tr>');
	f.write('<tr><td>'+at+'</td><td>'+mt+'</td><td>'+def+'</td><td>'+hu+'</td><td>'+fu+'</td><td>'+he+'</td><td>'+fi+'</td></tr>');
	f.write(temp_table2);
}

function pet_type(a)
{
	var s=new Array;
	s[0]="";
	s[1]="積極";
	s[2]="冷酷";
	s[3]="鐵壁";
	s[4]="危急";
	return s[a];
}
//###### mission #######
function mission_list(saletotal,page,s,store_id)
{
	var f=parent.wog_view.document;
	message_cls();
	f.write('<form action="wog_act.php" method="post" name=pageform target="mission">');
	pagesplit(saletotal,page);
	f.write('<input type="hidden" name="page" value="">');	
	f.write('<input type="hidden" name="f" value="mission">');	
	f.write('<input type="hidden" name="act" value="'+store_id+'">');
	f.write('</form>');
	f.write(temp_table1);

	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write(temp_table1);
	f.write('<tr><td></td><td>委託者</td><td>任務主題</td></tr>');
	if(s!="")
	{
		var s1=s.split(";");
		var temp_s="";
		for(var i=0;i<s1.length;i++)
		{	
			var s2=s1[i].split(",");
			f.write('<tr><td><input type="radio" name="m_id" value="'+s2[0]+'"></td><td>'+s2[1]+'</td><td>'+s2[2]+'</td></tr>');
		}
		f.write('<tr><td colspan="4"><input type="submit" value="接受任務"></td></tr>');
		f.write(temp_table2);
		f.write('<input type="hidden" name="f" value="mission">');    
		f.write('<input type="hidden" name="act" value="detail">'); 
	}else
	{
		f.write('<tr><td colspan="4" align="center">目前無任務</td></tr>');
		f.write(temp_table2);
	}
	f.write('</form>');
}

function mission_detail(s,m_id)
{
	message_cls();
	var f=parent.wog_view.document;
	f.write('<form action="wog_act.php" method="post" target="mission" name=f1>');
	if(s!="")
	{
		f.write(temp_table1);
		var s1=s.split(",");
		f.write('<tr><td >'+s1[0]+'</td></tr>'); 
		f.write('<tr><td >委託者：'+s1[1]+'</td></tr>');
		var temp=s1[2];
		while(temp.indexOf("&n") > 0)
		{
			temp=temp.replace("&n","<br>");
		}
		f.write('<tr><td class=b1>'+temp+'</td></tr>'); 
		f.write('<tr><td ><input type="submit" value="確定接受"></td></tr>'); 
		f.write(temp_table2);
		f.write('<input type="hidden" name="f" value="mission">');
		f.write('<input type="hidden" name="act" value="get">'); 
		f.write('<input type="hidden" name="m_id" value="'+m_id+'">');
	}
	f.write('</form>'); 	
}
function mission_book(s,m_id)
{
	message_cls();
	var f=parent.wog_view.document;
	f.write('<form action="wog_act.php" method="post" target="mission" name=f1>');
	if(s!="")
	{
		f.write(temp_table1);
		var s1=s.split(",");
		f.write('<tr><td >'+s1[0]+'</td></tr>'); 
		f.write('<tr><td >委託者：'+s1[1]+'</td></tr>');
		var temp=s1[2];
		while(temp.indexOf("&n") > 0)
		{
			temp=temp.replace("&n","<br>");
		}
		f.write('<tr><td class=b1>'+temp+'</td></tr>'); 
		f.write('<tr><td ><input type="button" value="完成任務" onClick="parent.foot_trun(\'mission\',\'end\',\'\',document.f1.m_id.value,\'\')"> <input type="button" value="放棄任務" onClick="parent.foot_trun(\'mission\',\'break\',\'\',document.f1.m_id.value,\'\')"></td></tr>'); 
		f.write(temp_table2);
		f.write('<input type="hidden" name="m_id" value="'+m_id+'">');
	}
	f.write('</form>'); 	
}
function mission_achieve(a,b)
{
	var f=parent.wog_view.document;
	f.write(hr);
	f.write(temp_table1+'<tr><td ><b>任務進度：'+m_name+' '+a+'/'+b+'</b></td></tr>');
	f.write(temp_table2);
}
function npc_message(message,a,b)
{
	var f=parent.wog_view.document;
	f.write(hr);
	while(message.indexOf("&n") > 0)
	{
		message=message.replace("&n","<br>");
	}
	f.write(temp_table1+'<tr><td ><b>發現：'+m_name+' '+a+'/'+b+'</b></td></tr><tr><td class=b1>'+message+'</td></tr>');
	f.write(temp_table2);
}
function mission_paper(saletotal,page,s)
{
	var f=parent.wog_view.document;
	message_cls();
	f.write('<form action="wog_act.php" method="post" name=pageform target="mission">');
	pagesplit(saletotal,page);
	f.write('<input type="hidden" name="page" value="">');	
	f.write('<input type="hidden" name="f" value="mission">');	
	f.write('<input type="hidden" name="act" value="paper">');
	f.write('</form>');
	f.write(temp_table1);

	f.write(temp_table1);
	f.write('<tr><td>委託者</td><td>任務主題</td></tr>');
	if(s!="")
	{
		var s1=s.split(";");
		for(var i=0;i<s1.length;i++)
		{  
			var s2=s1[i].split(",");
			f.write('<tr><td>'+s2[0]+'</td><td>'+s2[1]+'</td></tr>');
		}
	}
	f.write(temp_table2);
}
function mission_ed()
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1+'<tr><td><input type="button" value="查看未完成任務" onClick="parent.act_click(\'mission\',\'book\')"></td><td> <input type="button" value="查看已完成任務" onClick="parent.act_click(\'mission\',\'paper\')"></td></tr>'+temp_table2);
}

//###### event begin ######
function event() 
{ 
	var f=parent.wog_view.document;
	message_cls(); 
	var now_time=new Date();
	f.write(temp_table1); 
	f.write('<form action="wog_act.php" method="post" target="mission">'); 
	f.write('<tr><td>站長要考驗大家是否有認真在玩</td></tr>'); 
	f.write('<tr><td colspan="2"><img src="wog_etc.php?f=confirm&time='+now_time.getTime()+'"></td></tr>'); 
	f.write('<tr><td>請輸入安全驗證碼:<input type="text" name="sec_code" size="8"></td></tr>'); 
	f.write('<tr><td colspan="2"><input class="text" type="button" value="填好答案了,放我過關吧!!" onClick="parent.foot_trun(\'event\',\'\',this.form.sec_code.value,\'\')"></td></tr>'); 
	f.write('</form>'); 
	f.write(temp_table2); 
} 

//###### message #######
function message()
{
	var f=parent.wog_view.document;
	message_cls();
	f.write(temp_table1);
	f.write('<form action="wog_act.php" method="post" target="mission">');
	f.write('<tr><td>遊戲中的帳號</td><td class="b1"><input type="text" name="name" size="12"></td></tr>');
	f.write('<tr><td>內容</td><td class="b1"><textarea cols="30" rows="7" name="body"></textarea></td></tr>');
	f.write('<tr><td colspan="2"><input type="button" value="送出" onClick="parent.foot_trun(\'message\',\'\',this.form.name.value,this.form.body.value)"></td></tr>');
	f.write('<tr><td colspan="2">訊息是發到論壇上對方需到論壇上才能收到訊息</td></tr>');
	f.write('</form>');
	f.write(temp_table2);
}

//###### race begin ######
function race_view(s,p_name,p_money)
{
	message_cls();
	var f=parent.wog_view.document;
	f.write('<form action="wog_etc.php?f=race&act=end" method="post" target="mission" name="f1" >');
	f.write(temp_table1);
	f.write('<tr><td >'+p_name+'</td><td colspan="4" >現金 '+p_money+' | 賠率 1 : 5 | 最小賭注 100 最大賭注 100000</td></tr>');
	f.write('<tr><td >閘位</td><td >照片</td><td >鳥名</td><td >必殺技</td><td >選擇</td></tr>');
	var s1=s.split(";");
	var temp_s="";
	for(var i=0;i<s1.length;i++)
	{	
		var s2=s1[i].split(",");
		temp_s+=","+s2[2];
		f.write('<tr><td ><b>'+(i+1)+'</b></td><td ><IMG src="'+img+'horse/cho'+(i+1)+'.gif" ></td><td >'+s2[0]+'</td><td >'+s2[1]+'</td><td ><input type="radio" name="yourchoose" value="'+s2[2]+'" ></td></tr>');
	}
	f.write('<tr><td  colspan="5" >下注金額 <input type="text" name="money" size="8" maxlength="8"> <input type="submit" value="確定"> </td></tr>');
	f.write(temp_table2);
	temp_s=temp_s.substr(1,temp_s.length);
	f.write('<input type="hidden" name="temp_id" value="'+temp_s+'">');
	f.write('</form>');
}

function race_end(s,a,b,f,winer)
{
	message_cls();
	var ff=parent.wog_view.document;
	ff.write('<br>');
	ff.write('<table width=100% border=0 cellspacing=1 cellpadding=5 bgcolor=#4B689E>');
	var s1=s.split(",");
	for(var i=0;i<s1.length;i++)
	{	
		ff.write('<div id=h'+(i+1)+' style=position:absolute;top:'+(35+(i*40))+'px><img src='+img+'horse/cho'+(i+1)+'.gif></div>');
		ff.write('<tr bgcolor=#000000 align=right><td height=39 width=10>'+(i+1)+'</td><td width='+f+'></td><td>'+s1[i]+'</td></tr>');
	}
	ff.write(temp_table2);
	ff.write('<div id=sysMsg style=position:absolute;width:250;height:30%;left:40%;>');
	ff.write('<table width="100%" border="0" cellspacing="1" cellpadding="3" ><tr><td colspan=2  align=center>比賽結果公佈 --- '+b+'</td></tr><tr> <td width="40%" align=center>第１名：</td><td width="60%" align=center>'+winer+'</td> </tr></table></div>');
	Horse_timelinePlay('horse',null,a);
}

function Horse_timelinePlay(tmLnName, myID,a) {
var view_name=parent.wog_view.document;
if (view_name.Horse_Time == null) Horse_initTimelines(a);
tmLn = view_name.Horse_Time[tmLnName];
if(myID == null) { myID = ++tmLn.ID; firstTime=true;}
setTimeout('Horse_timelinePlay("'+tmLnName+'",'+myID+')',tmLn.delay);
fNew = ++tmLn.curFrame;
for (i=0; i<tmLn.length; i++) {
sprite = tmLn[i];
if (sprite.obj) {
numKeyFr = sprite.keyFrames.length; firstKeyFr = sprite.keyFrames[0];
if (fNew >= firstKeyFr && fNew <= sprite.keyFrames[numKeyFr-1]) {
keyFrm=1;
for (j=0; j<sprite.values.length; j++) {
props = sprite.values[j];
if (numKeyFr != props.length) {
if (props.prop2 == null) sprite.obj[props.prop] = props[fNew-firstKeyFr];
else sprite.obj[props.prop2][props.prop] = props[fNew-firstKeyFr];
}else{
while (keyFrm<numKeyFr && fNew>=sprite.keyFrames[keyFrm]) keyFrm++;
if (firstTime || fNew==sprite.keyFrames[keyFrm-1]) {
if (props.prop2 == null) sprite.obj[props.prop] = props[keyFrm-1];
else sprite.obj[props.prop2][props.prop] = props[keyFrm-1];
}}}}
}}
}

function Horse_initTimelines(a) {
var view_name=parent.wog_view.document;
view_name.Horse_Time = new Array();
view_name.Horse_Time[0] = new Array();
view_name.Horse_Time["horse"] = view_name.Horse_Time[0];
var s1=a.split(";");
for(var i=0;i<s1.length;i++)
{	
	view_name.Horse_Time[0][i]=new String("sprite");
	view_name.Horse_Time[0][i].obj=view_name.all ? view_name.all["h"+(i+1)] : null;
	view_name.Horse_Time[0][i].keyFrames=new Array(1,30);
	view_name.Horse_Time[0][i].values=new Array(2);
	view_name.Horse_Time[0][i].values[0]=new Array();
	var s2=s1[i].split(",");
	for(var j=0;j<s2.length;j++)
	{
		view_name.Horse_Time[0][i].values[0][j]=parseInt(s2[j]);
	}
	view_name.Horse_Time[0][i].values[0].prop="left";
	view_name.Horse_Time[0][i].values[1]=new Array();
	view_name.Horse_Time[0][i].values[0].prop2="style";
}
view_name.Horse_Time[0][s1.length]=new String("sprite");
view_name.Horse_Time[0][s1.length].obj = view_name.all ? view_name.all["sysMsg"] : null;
view_name.Horse_Time[0][s1.length].keyFrames=new Array(1,30);
view_name.Horse_Time[0][s1.length].values=new Array();
view_name.Horse_Time[0][s1.length].values[0]=new Array();
view_name.Horse_Time[0][s1.length].values[0].prop="left";
view_name.Horse_Time[0][s1.length].values[1]=new Array();
view_name.Horse_Time[0][s1.length].values[0]=new Array("hidden","inherit");
view_name.Horse_Time[0][s1.length].values[0].prop="visibility";
view_name.Horse_Time[0][s1.length].values[0].prop2="style";
for(i=0;i<view_name.Horse_Time.length;i++){view_name.Horse_Time[i].curFrame=0;view_name.Horse_Time[i].delay=200;}
}

function p1()
{
	parent.peolist.document.location.reload();
	window.setTimeout("p1()",300000); 
}
window.setTimeout("p1()",300000);
