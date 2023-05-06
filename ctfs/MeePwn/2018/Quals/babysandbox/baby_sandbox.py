from __future__ import print_function
from flask import Flask, Response, render_template, session, request, jsonify, send_file
import os
from subprocess import run, STDOUT, PIPE, CalledProcessError
from base64 import b64decode, b64encode
from unicorn import *
from unicorn.x86_const import *
import codecs
import time

app = Flask(__name__)
app.secret_key = open('private/secret.txt').read()


ADDRESS = 0x1000000
sys_fork = 2
sys_read = 3
sys_write = 4
sys_open = 5
sys_close = 6
sys_execve = 11
sys_access = 33
sys_dup	= 41
sys_dup2 = 63
sys_mmap = 90
sys_munmap = 91
sys_mprotect = 125
sys_sendfile = 187
sys_sendfile64 = 239
BADSYSCALL = [sys_fork, sys_read, sys_write, sys_open, sys_close, sys_execve, sys_access, sys_dup, sys_dup2, sys_mmap, sys_munmap, sys_mprotect, sys_sendfile, sys_sendfile64]

# callback for tracing Linux interrupt
def hook_intr(uc, intno, user_data):
	if intno != 0x80:
		uc.emu_stop()
		return
	eax = uc.reg_read(UC_X86_REG_EAX)
	if eax in BADSYSCALL:
		session['ISBADSYSCALL'] = True
		uc.emu_stop()

def test_i386(mode, code):
	try:
		# Initialize emulator
		mu = Uc(UC_ARCH_X86, mode)

		# map 2MB memory for this emulation
		mu.mem_map(ADDRESS, 2 * 1024 * 1024)

		# write machine code to be emulated to memory
		mu.mem_write(ADDRESS, code)

		# initialize stack
		mu.reg_write(UC_X86_REG_ESP, ADDRESS + 0x200000)

		
		# handle interrupt ourself
		mu.hook_add(UC_HOOK_INTR, hook_intr)

		# emulate machine code in infinite time
		mu.emu_start(ADDRESS, ADDRESS + len(code))
	except UcError as e:
		print("ERROR: %s" % e)


@app.route('/')
def main():
	if session.get('ISBADSYSCALL') == None:
		session['ISBADSYSCALL'] = False
	return render_template('index.html', name="BABY")

	
@app.route('/source', methods=['GET'])
def resouce():
	return send_file("app.py")

@app.route('/bin', methods=['GET'])
def bin():
	return send_file("/home/babysandbox/babysandbox")

		
@app.route('/exploit', methods=['POST'])
def exploit():
	try:
		data = request.get_json(force=True)
	except Exception:
		return jsonify({'result': 'Wrong data!'})
	
	try:
		payload = b64decode(data['payload'].encode())
	except:
		return jsonify({'result': 'Wrong data!'})
	
	test_i386(UC_MODE_32, payload)
	if session['ISBADSYSCALL']:
		return jsonify({'result': 'Bad Syscall!'})
	try:
		run(['nc', 'localhost', '9999'], input=payload, timeout=2, check=True)
	except CalledProcessError:
		return jsonify({'result': 'Error run file!'})
		
	return jsonify({'result': "DONE!"})
		

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
