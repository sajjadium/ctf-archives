from flask import Flask, request
import re, random, os

app = Flask(__name__)
FL4G = os.environ.get('secret_flag')
fail = "???<br><img src='https://i.imgur.com/mUfnGmL.png' width='20%' />"
NewYearCategoryList = ["NewYearCommonList", "NewYearHealthList", "NewYearFamilyList", "NewYearWealthList"]
NewYearCommonList = ["Chúc Mừng Năm Mới!", "Happy New Year!", "Cheers to a new year and another chance for us to get it right!", "Let's make 2023 our best year yet.", "Năm mới Vui Vẻ", "New year! New Me!"]
NewYearHealthList = ["Sức Khoẻ Dồi Dào!", "Wishing you and yours health and prosperity in the new year", "May the new year bring you peace", "Joy, and happiness!", "Tết An Lành"]
NewYearFamilyList = ["Gia Đình Hạnh Phúc!", "Hoping that the new year will bring you and your family a year full of joy and serenity", "Together! Forever!", "Best wishes for your family"]
NewYearWealthList = ["Năm Mới Phát Tài!", "Have a sparkling New Year!", "Here's hoping you make the most of 2023!", "May the new year bless you with health, wealth, and happiness.", "An Khang Thịnh Vượng"]

# random greeting
def random_greet(s):
	return eval("%s[random.randint(0,len(%s)-1)]" % (s, s))+"</center>"

def botValidator(s):
	# Number only!
	for c in s:
		if (57 < ord(c) < 123):
			return False
	# The number should only within length of greeting list.
	n = "".join(x for x in re.findall(r'\d+', s))
	if n.isnumeric():
		ev = "max("
		for gl in NewYearCategoryList:
			ev += "len(%s)," % gl 
		l = eval(ev[:-1]+")")
		if int(n) > (l-1):
			return False
	return True

@app.route('/', methods=['GET', 'POST'])
def greeting():
	bot = ""
	css = """
	<br><br>
	<center>
		<strong><font size=5 color='purple'>Get New Year Quotes From Our New Year Bot!</font></strong>
		<br>_[<img src="https://i.imgur.com/uYBBhWn.gif" width="5%" />]_
	</center>
	<style>
	.centered {
	  position: fixed; /* or absolute */
	  top: 25%;
	  left: 35%;
	}
	</style>
	"""
	front = """
	<form action="/" method="POST" >
		<select name="type">
			<option value="greeting_all">All</option>
			<option value="NewYearCommonList">Common</option>
			<option value="NewYearHealthList">Health</option>
			<option value="NewYearFamilyList">Family</option>
			<option value="NewYearWealthList">Wealth</option>
		</select>
		<input type="text" hidden name="number" value="%s" />
		<input type="submit" value="Ask" /><br>
	</form>
	"""%random.randint(0,3)
	greeting = ""
	try:
		debug = request.args.get("debug")
		if request.method == 'POST':
			greetType = request.form["type"]
			greetNumber = request.form["number"]
			if greetType == "greeting_all":
				greeting = random_greet(random.choice(NewYearCategoryList))
			else:
				try:
					if greetType != None and greetNumber != None:
						greetNumber = re.sub(r'\s+', '', greetNumber)
						if greetType.isidentifier() == True and botValidator(greetNumber) == True:
							if len("%s[%s]" % (greetType, greetNumber)) > 20:
								greeting = fail
							else:
								greeting = eval("%s[%s]" % (greetType, greetNumber))
							try:
								if greeting != fail and debug != None:
									greeting += "<br>You're choosing %s, it has %s quotes"%(greetType, len(eval(greetType)))
							except:
								pass
						else:
							greeting = fail
					else:
						greeting = random_greet(random.choice(NewYearCategoryList))
				except:
					greeting = fail
					pass
		else:
			greeting = random_greet(random.choice(NewYearCategoryList))

		if fail not in greeting:
			bot_list = ["( ´ ∀ `)ノ～ ♡", "（✿◕ᴗ◕)つ━━✫・*。", "(๑˘ᵕ˘)"]
		else:
			bot_list = ["(≖ ︿ ≖ ✿)", "ᕙ(⇀‸↼‶)ᕗ", "(≖ ︿ ≖ ✿)ꐦꐦ", "┌( ಠ_ಠ )┘"]
		bot = random.choice(bot_list)
	except:
		pass
	return "%s<div class='centered'>%s<strong><font color='red'>%s<br>NewYearBot >> </font></strong>%s</div>"%(css, front, bot, greeting)

# Main
if __name__ == '__main__':
	app.run(debug=True)
