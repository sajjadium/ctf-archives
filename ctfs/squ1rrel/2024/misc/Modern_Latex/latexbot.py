#!/usr/bin/env python
import discord
import urllib.request
import random
import os
import json
import shutil
import asyncio
import sys

import chanrestrict

LATEX_TEMPLATE="template.tex"

blacklist = ["\\input", "\\include", "\\lstinputlisting", "\\usepackage", "\\verbatiminput", "\\openin",  "\\newread", "\\read", "\\open", "\\write18"]

HELP_MESSAGE = r"""
Hello! I'm the *LaTeX* math bot!

You can type mathematical *LaTeX* into the chat and I'll automatically render it!

Simply use the `!tex` command.

**Examples**

`!tex x = 7`

`!tex \sqrt{a^2 + b^2} = c`

`!tex \int_0^{2\pi} \sin{(4\theta)} \mathrm{d}\theta`

**Notes**

Using the `\begin` or `\end` in the *LaTeX* will probably result in something failing.

https://github.com/DXsmiley/LatexBot
"""


class LatexBot(discord.Client):
	#TODO: Check for bad token or login credentials using try catch
	def __init__(self):
		intents = discord.Intents.all() 
		super().__init__(intents=intents)

		self.check_for_config()
		self.settings = json.loads(open('settings.json').read())

		# Quick and dirty defaults of colour settings, if not already present in the settings
		if 'latex' not in self.settings:
			self.settings['latex'] = {
							'background-colour': '36393E',
							'text-colour': 'DBDBDB',
							'dpi': '200'
			}

		chanrestrict.setup(self.settings['channels']['whitelist'],
							self.settings['channels']['blacklist'])

		# Check if user is using a token or login
		if self.settings['login_method'] == 'token':
			self.run(self.settings['login']['token'])
		elif self.settings['login_method'] == 'account':
			self.login(self.settings['login']['email'], self.settings['login']['password'])
			self.run()
		else:
			raise Exception('Bad config: "login_method" should set to "login" or "token"')

	# Check that config exists
	def check_for_config(self):
		if not os.path.isfile('settings.json'):
			shutil.copyfile('settings_default.json', 'settings.json')
			print('Now you can go and edit `settings.json`.')
			print('See README.md for more information on these settings.')

	def vprint(self, *args, **kwargs):
		if self.settings.get('verbose', False):
			print(*args, **kwargs)

	# Outputs bot info to user
	@asyncio.coroutine
	def on_ready(self):
		print('------')
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')

	async def on_message(self, message):
		if chanrestrict.check(message):

			msg = message.content

			for c in self.settings['commands']['render']:
				if msg.startswith(c):
					latex = msg[len(c):].strip()
					for b in blacklist:
						if b in latex:
							await message.channel.send('Blacklisted command detected. :frowning:')
							return
					self.vprint('Latex:', latex)

					num = str(random.randint(0, 2 ** 31))
					fn = self.generate_image(latex, num)

					if fn and os.path.getsize(fn) > 0:
						await message.channel.send(file=discord.File(fn))
						self.cleanup_output_files(num)
						self.vprint('Success!')
					else:
						await message.channel.send('Something broke. Check the syntax of your message. :frowning:')
						self.cleanup_output_files(num)
						self.vprint('Failure.')

					break

			if msg in self.settings['commands']['help']:
				self.vprint('Showing help')
				await self.send_message(message.author, HELP_MESSAGE)

	# Generate LaTeX locally. Is there such things as rogue LaTeX code?
	def generate_image(self, latex, name):

		latex_file = name + '.tex'
		dvi_file = name + '.dvi'
		png_file = name + '1.png'

		with open(LATEX_TEMPLATE, 'r') as textemplatefile:
			textemplate = textemplatefile.read()

			with open(latex_file, 'w') as tex:
				backgroundcolour = self.settings['latex']['background-colour']
				textcolour = self.settings['latex']['text-colour']
				latex = textemplate.replace('__DATA__', latex).replace('__BGCOLOUR__', backgroundcolour).replace('__TEXTCOLOUR__', textcolour)

				tex.write(latex)
				tex.flush()
				tex.close()

		imagedpi = self.settings['latex']['dpi']
		latexsuccess = os.system('latex -quiet -interaction=nonstopmode ' + latex_file)
		if latexsuccess == 0:
			os.system('dvipng -q* -D {0} -T tight '.format(imagedpi) + dvi_file)
			return png_file
		else:
			return ''

	# Removes the generated output files for a given name
	def cleanup_output_files(self, outputnum):
		try:
			os.remove(outputnum + '.tex')
			os.remove(outputnum + '.dvi')
			os.remove(outputnum + '.aux')
			os.remove(outputnum + '.log')
			os.remove(outputnum + '1.png')
		except OSError:
			pass


if __name__ == "__main__":
	LatexBot()
