from flask import Flask, render_template, render_template_string, request, redirect, url_for, session, send_from_directory
import os
import uuid
import re
import sys
from waitress import serve

app = Flask(__name__)
app.secret_key = os.environ['secret_key']
UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def get_fileext(filename):
    fileext = filename.rsplit('.', 1)[1].lower()
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return fileext
    return None

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method != 'POST':
        return redirect(url_for('profile'))
    
    # check if the post request has the file part
    if 'file' not in request.files:
            return redirect(url_for('profile'))
    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename.
    if file.filename == '':
        return redirect(url_for('profile'))
    
    fileext = get_fileext(file.filename)

    file.seek(0, 2) # seeks the end of the file
    filesize = file.tell() # tell at which byte we are
    file.seek(0, 0) # go back to the beginning of the file

    if fileext and filesize < 10*1024*1024:
        if session['ext'] and os.path.exists(os.path.join(UPLOAD_FOLDER, session['uuid']+"."+session['ext'])):
            os.remove(os.path.join(UPLOAD_FOLDER, session['uuid']+"."+session['ext']))
        session['ext'] = fileext
        filename = session['uuid']+"."+session['ext']
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return redirect(url_for('profile'))
    else:
        template = f"""
            {file.filename} is not valid because it is too big or has the wrong extension
        """
        l1 = ['+', '{{', '}}', '[2]', 'flask', 'os','config', 'subprocess', 'debug', 'read', 'write', 'exec', 'popen', 'import', 'request', '|', 'join', 'attr', 'globals', '\\'] 

        l2 = ['aa-exec', 'agetty', 'alpine', 'ansible-playbook', 'ansible-test', 'aoss', 'apt', 'apt-get', 'aria2c', 'arj', 'arp', 'ascii-xfr', 'ascii85', 'ash', 'aspell', 'atobm', 'awk', 'aws', 'base', 'base32', 'base58', 'base64', 'basenc', 'basez', 'bash', 'batcat', 'bconsole', 'bpftrace', 'bridge', 'bundle', 'bundler', 'busctl', 'busybox', 'byebug', 'bzip2', 'c89', 'c99', 'cabal', 'cancel', 'capsh', 'cat', 'cdist', 'certbot', 'check_by_ssh', 'check_cups', 'check_log', 'check_memory', 'check_raid', 'check_ssl_cert', 'check_statusfile', 'chmod', 'choom', 'chown', 'chroot', 'cmp', 'cobc', 'column', 'comm', 'comm ', 'composer', 'cowsay', 'cowthink', 'cpan', 'cpio', 'cpulimit', 'crash', 'crontab', 'csh', 'csplit', 'csvtool', 'cupsfilter', 'curl', 'cut', 'dash', 'date', 'debug', 'debugfs', 'dialog', 'diff', 'dig', 'dir', 'distcc', 'dmesg', 'dmidecode', 'dmsetup', 'dnf', 'docker', 'dos2unix', 'dosbox', 'dotnet', 'dpkg', 'dstat', 'dvips', 'easy_install', 'echo', 'efax', 'elvish', 'emacs', 'env', 'eqn', 'espeak', 'exiftool', 'expand', 'expect', 'facter', 'file', 'find', 'finger', 'fish', 'flock', 'fmt', 'fold', 'fping', 'ftp', 'gawk', 'gcc', 'gcloud', 'gcore', 'gdb', 'gem', 'genie', 'genisoimage', 'ghc', 'ghci', 'gimp', 'ginsh', 'git', 'grc', 'grep', 'gtester', 'gzip', 'head', 'hexdump', 'highlight', 'hping3', 'iconv', 'ifconfig', 'iftop', 'install', 'ionice', 'irb', 'ispell', 'jjs', 'joe', 'join', 'journalctl', 'jrunscript', 'jtag', 'julia', 'knife', 'ksh', 'ksshell', 'ksu', 'kubectl', 'latex', 'latexmk', 'ld.so', 'ldconfig', 'less', 'less ', 'lftp', 'loginctl', 'logsave', 'look', 'ltrace', 'lua', 'lualatex', 'luatex', 'lwp-download', 'lwp-request', 'mail', 'make', 'man', 'mawk', 'more', 'mosquitto', 'mount', 'msfconsole', 'msgattrib', 'msgcat', 'msgconv', 'msgfilter', 'msgmerge', 'msguniq', 'mtr', 'multitime', 'mysql', 'nano', 'nasm', 'nawk', 'ncftp', 'neofetch', 'netstat', 'nft', 'nice', 'nmap', 'node', 'nohup', 'npm', 'nroff', 'nsenter', 'nslookup', 'octave', 'openssl', 'openvpn', 'openvt', 'opkg', 'pandoc', 'paste', 'pax', 'pdb', 'pdflatex', 'pdftex', 'perf', 'perl', 'perlbug', 'pexec', 'php', 'pic', 'pico', 'pidstat', 'ping', 'pip', 'pkexec', 'pkg', 'posh', 'pry', 'psftp', 'psql', 'ptx', 'puppet', 'pwsh', 'rake', 'readelf', 'red', 'redcarpet', 'redis', 'restic', 'rev', 'rlogin', 'rlwrap', 'route', 'rpm', 'rpmdb', 'rpmquery', 'rpmverify', 'rsync', 'rtorrent', 'ruby', 'run-mailcap', 'run-parts', 'rview', 'rvim', 'sash', 'scanmem', 'scp', 'screen', 'script', 'scrot', 'sed', 'service', 'setarch', 'setfacl', 'setlock', 'sftp', 'shuf', 'slsh', 'smbclient', 'snap', 'socat', 'socket', 'soelim', 'softlimit', 'sort', 'split', 'sqlite3', 'sqlmap', 'ssh', 'ssh-agent', 'ssh-keygen', 'ssh-keyscan', 'sshpass', 'start-stop-daemon', 'stdbuf', 'strace', 'strings', 'sysctl', 'systemctl', 'systemd-resolve', 'tac', 'tail', 'tar', 'task', 'taskset', 'tasksh', 'tbl', 'tclsh', 'tcpdump', 'tdbtool', 'tee', 'telnet', 'tex', 'tftp', 'time', 'timedatectl', 'timeout', 'tmate', 'tmux', 'top', 'torify', 'torsocks', 'touch', 'traceroute', 'troff', 'truncate', 'tshark', 'unexpand', 'uniq', 'unshare', 'unzip', 'update-alternatives', 'uudecode', 'uuencode', 'vagrant', 'valgrind', 'view', 'vigr', 'vim', 'vimdiff', 'vipw', 'virsh', 'volatility', 'w3m', 'wall', 'watch', 'wget', 'whiptail', 'whois', 'wireshark', 'wish', 'xargs', 'xdotool', 'xelatex', 'xetex', 'xmodmap', 'xmore', 'xpad', 'xxd', 'yarn', 'yash', 'yelp', 'yum', 'zathura', 'zip', 'zsh', 'zsoelim', 'zypper']
        

        for i in l1:
            if i in template.lower():
                print(template, i, file=sys.stderr)
                template = "nice try"
                break
        matches = re.findall(r"['\"](.*?)['\"]", template)
        for match in matches:
            print(match, file=sys.stderr)
            if not re.match(r'^[a-zA-Z0-9 \/\.\-]+$', match):
                template = "nice try"
                break
            for i in l2:
                if i in match.lower():
                    print(i, file=sys.stderr)
                    template = "nice try"
                    break
        return render_template_string(template)
        
@app.route('/')
def profile():
    if 'uuid' in session:
        uuuid = session['uuid']
        ext = session['ext']
        if not ext:
            return render_template('profile.html')
        else:
            return render_template('profile.html', file_link="./uploads/"+uuuid+"."+ext)
    else:
        session['uuid'] = str(uuid.uuid4())
        session['ext'] = None
        return(render_template('profile.html'))

if __name__ == '__main__':
	serve(app, host='0.0.0.0', port=5000)
