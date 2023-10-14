<html>
 <head>
  <title> Debug Page...</title>

  <meta charset="utf-8">

  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>

</head>
<body>
    <div class="container">
    <?php
    error_reporting(0);
    $conn = mysqli_connect('db', 'user', 'test', "dockerExample");


    $query = 'SELECT * From Person';
    $result = mysqli_query($conn, $query);

    echo '<table class="table table-striped">';
    echo '<thead><tr><th></th><th>id</th><th>name</th></tr></thead>';
    while($value = $result->fetch_array(MYSQLI_ASSOC)){
        echo '<tr>';
        echo '<td><a href="#"><span class="glyphicon glyphicon-search"></span></a></td>';
        foreach($value as $element){
            echo '<td>' . $element . '</td>';
        }

        echo '</tr>';
    }
    echo '</table>';

    $result->close();

    mysqli_close($conn);

    $blacklists = ["chgrp","mknod","run-parts","vdir","bunzip2","chmod","fgrep","mktemp","sed","wdctl","bzcat","chown","findmnt","more","bzcmp","cp","grep","mount","sleep","zcat","bzdiff","bash","gunzip","mountpoint","stty","zcmp","bzegrep","date","gzexe","mv","su","zdiff","bzexe","dd","gzip","nisdomainname","sync","zegrep","bzfgrep","df","hostname","pidof","tar","zfgrep","bzgrep","dir","kill","ps","tempfile","zforce","bzip2","dmesg","ln","pwd","touch","zgrep","bzip2recover","dnsdomainname","login","rbash","true","zless","bzless","domainname","ls","readlink","umount","zmore","bzmore","echo","lsblk","rm","uname","znew","cat","egrep","mkdir","rmdir","uncompress","m4","ab","make","addpart","make-first-existing-target","addr2line","mawk","apt","mcookie","apt-cache","md5sum","apt-cdrom","md5sum.textutils","apt-config","mesg","apt-get","mkfifo","apt-key","namei","apt-mark","nawk","ar","newgrp","arch","nice","as","nl","autoconf","nm","autoheader","nohup","autom4te","nproc","autoreconf","nsenter","autoscan","numfmt","autoupdate","objcopy","awk","objdump","b2sum","od","base32","open","base64","openssl","basename","pager","basenc","partx","bashbug","passwd","paste","patch","c89","pathchk","c89-gcc","perl","c99","c99-gcc","perl5.32.1","c_rehash","perlbug","captoinfo","perldoc","catchsegv","perlivp","cc","perlthanks","chage","pgrep","chattr","piconv","chcon","pidwait","checkgid","pinky","chfn","pkg-config","choom","pkill","chrt","pl2pm","chsh","pldd","cksum","pmap","clear","pod2html","clear_console","pod2man","cmp","pod2text","comm","pod2usage","compose","podchecker","corelist","cpan","printenv","cpp","cpp-10","prlimit","csplit","prove","curl","ptar","cut","ptardiff","deb-systemd-helper","ptargrep","deb-systemd-invoke","ptx","debconf","pwdx","debconf-apt-progress","ranlib","debconf-communicate","re2c","debconf-copydb","re2go","debconf-escape","readelf","debconf-set-selections","realpath","debconf-show","renice","delpart","reset","diff","resizepart","diff3","rev","dircolors","rgrep","dirname","rotatelogs","dpkg","rpcgen","dpkg-architecture","run-mailcap","dpkg-buildflags","runcon","dpkg-buildpackage","savelog","dpkg-checkbuilddeps","script","dpkg-deb","scriptlive","dpkg-distaddfile","scriptreplay","dpkg-divert","sdiff","dpkg-genbuildinfo","see","dpkg-genchanges","seq","dpkg-gencontrol","setarch","dpkg-gensymbols","setpriv","dpkg-maintscript-helper","setsid","dpkg-mergechangelogs","setterm","dpkg-name","sg","dpkg-parsechangelog","sha1sum","dpkg-query","sha224sum","dpkg-realpath","sha256sum","dpkg-scanpackages","sha384sum","dpkg-scansources","sha512sum","dpkg-shlibdeps","shasum","dpkg-source","shred","dpkg-split","shuf","dpkg-statoverride","size","dpkg-trigger","skill","dpkg-vendor","slabtop","du","snice","dwp","sort","edit","splain","elfedit","split","enc2xs","stat","encguess","stdbuf","env","streamzip","expand","strings","expiry","strip","expr","sum","factor","tabs","faillog","tac","fallocate","tail","fcgistarter","taskset","file","tee","fincore","test","find","tic","flock","timeout","fmt","tload","fold","toe","free","top","touch","tput","gcc","tr","gcc-10","truncate","gcc-ar","tset","gcc-ar-10","tsort","gcc-nm","tty","gcc-nm-10","tzselect","gcc-ranlib","unexpand","gcc-ranlib-10","uniq","gcov","unlink","gcov-10","unlzma","gcov-dump","unshare","gcov-dump-10","unxz","gcov-tool","update-alternatives","gcov-tool-10","uptime","gencat","users","getconf","utmpdump","getent","vmstat","getopt","w","gmake","wall","gold","watch","gpasswd","wc","gpgv","whereis","gprof","which","groups","who","h2ph","whoami","h2xs","head","hostid","htcacheclean","htdbm","htdigest","htpasswd","i386","iconv","id","ifnames","infocmp","infotocap","install","instmodsh","ionice","ipcmk","ipcrm","ipcs","ischroot","join","json_pp","last","lastb","lastlog","ld","ld.bfd","ld.gold","ldd","libnetcfg","link","linux32","linux64","locale","localedef","logger","logname","logresolve","lsattr","lscpu","lsipc","lslocks","xargs","lslogins","xsubpp","lsmem","xz","lsns","xzcat","lto-dump-10","xzcmp","lzcat","xzdiff","lzcmp","xzegrep","lzdiff","xzfgrep","lzegrep","xzgrep","lzfgrep","xzless","lzgrep","xzmore","lzless","yes","lzma","zdump","lzmainfo","zipdetails","lzmore","a2disconf","dpkg-reconfigure","policy-rc.d","a2dismod","e2freefrag","pwck","a2dissite","e4crypt","pwconv","a2enconf","e4defrag","pwunconv","a2enmod","faillock","readprofile","a2ensite","fdformat","remove-shell","a2query","filefrag","rmt","add-shell","groupadd","rmt-tar","addgroup","groupdel","rtcwake","adduser","groupmems","service","apache2","groupmod","split-logfile","apache2ctl","grpck","tarcat","apachectl","grpconv","tzconfig","check_forensic","grpunconv","update-ca-certificates","chgpasswd","httxt2dbm","update-mime","chmem","iconvconfig","update-passwd","chpasswd","invoke-rc.d","update-rc.d","chroot","ldattach","useradd","cpgr","userdel","cppw","newusers","usermod","delgroup","nologin","vigr","deluser","pam-auth-update","vipw","dpkg-fsys-usrunmess","pam_getenv","zic","dpkg-preconfigure","pam_timestamp_check","apache2-foreground","docker-php-ext-install","peardev","php","docker-php-entrypoint","docker-php-source","pecl","php-config","docker-php-ext-configure","freetype-config","phar","phpize","docker-php-ext-enable","pear","phar.phar","agetty","e2mmpstatus","fstrim","mkfs.ext2","swaplabel","badblocks","e2scrub","getty","mkfs.ext3","swapoff","blkdiscard","e2scrub_all","hwclock","mkfs.ext4","swapon","blkid","e2undo","installkernel","mkfs.minix","switch_root","blkzone","findfs","isosize","mkhomedir_helper","sysctl","blockdev","fsck","killall5","mkswap","tune2fs","chcpu","fsck.cramfs","ldconfig","pivot_root","unix_chkpwd","ctrlaltdel","fsck.ext2","logsave","raw","unix_update","debugfs","fsck.ext3","losetup","resize2fs","wipefs","dumpe2fs","fsck.ext4","mke2fs","runuser","zramctl","e2fsck","fsck.minix","mkfs","shadowconfig","e2image","fsfreeze","mkfs.bfs","start-stop-daemon","e2label","fstab-decode","mkfs.cramfs","sulogin"];
 
	$cmd = $_GET['cmd']; 
    foreach ($blacklists as $blacklist) {
    	$pattern = "/$blacklist/";
		if (preg_match($pattern, $cmd)) {
			die("Blacklist");
		}
	}

    system(escapeshellcmd($cmd));

    ?>
    </div>
</body>
</html>
