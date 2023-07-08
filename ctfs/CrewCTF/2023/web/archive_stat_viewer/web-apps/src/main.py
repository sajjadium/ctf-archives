from pathlib import Path
from uuid import uuid4
from secrets import token_hex
from datetime import datetime
import os
import tarfile
import json
import shutil

from flask import Flask, request, session, send_file, render_template, redirect, make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = open('./secret').read()
app.config['MAX_CONTENT_LENGTH'] = 1024 * 128

UPLOAD_DIR = Path('./archives')

class HackingException(Exception):
	pass

def extract_archive(archive_path, extract_folder):
	with tarfile.open(archive_path) as archive:
		for member in archive.getmembers():
			if member.name[0] == '/' or '..' in member.name:
				raise HackingException('Malicious archive')
		archive.extractall(extract_folder)

def get_folder_info(extract_folder):
	data = {}
	for file in extract_folder.iterdir():
		stat = file.lstat()
		name = file.name
		size = stat.st_size
		last_updated = datetime.utcfromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

		data[file.name] = {}
		data[file.name]['Size'] = size
		data[file.name]['Last updated'] = last_updated
	return data

@app.get('/')
def index():
	if 'archives' not in session:
		session['archives'] = []
	return render_template('index.html', archives = session['archives'])

@app.get('/results/<archive_id>')
def download_result(archive_id):
	if 'archives' not in session:
		session['archives'] = []
	archive_id = Path(archive_id).name
	return send_file(UPLOAD_DIR / archive_id / 'result.json')

@app.get('/clean')
def clean_results():
	if 'archives' not in session:
		session['archives'] = []
	for archive in session['archives']:
		shutil.rmtree(UPLOAD_DIR / archive['id'])
	session['archives'] = []
	return redirect('/')


@app.post('/analyze')
def analyze_archive():
	if 'archives' not in session:
		session['archives'] = []
	
	archive_id = str(uuid4())
	
	archive_folder = UPLOAD_DIR / archive_id
	extract_folder = archive_folder / 'files/'
	archive_path = archive_folder / 'archive.tar'
	result_path = archive_folder / 'result.json'

	extract_folder.mkdir(parents=True)
	
	archive = request.files['archive']
	archive_name = archive.filename
	archive.save(archive_path)

	try:
		extract_archive(archive_path, extract_folder)
	except HackingException:
		return make_response("Don't hack me!", 400)

	data = get_folder_info(extract_folder)
	with open(result_path, 'w') as f:
		json.dump(data, f, indent=2)

	session['archives'] = session['archives'] + [{
		'id': archive_id,
		'name': archive_name
	}]

	return redirect('/')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
